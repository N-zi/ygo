from hoshino import Service, priv, MessageSegment
import nonebot
import aiohttp
import re

sv_help = '''
游戏王查卡
查卡 卡名
'''.strip()

sv = Service(
    name='游戏王查卡',  # 功能名
    use_priv=priv.NORMAL,  # 使用权限
    manage_priv=priv.ADMIN,  # 管理权限
    visible=True,  # 可见性
    enable_on_default=True,  # 默认启用
    # bundle = '娱乐', #分组归类
    help_=sv_help  # 帮助说明
)

ygo_max = 5

@sv.on_prefix('查卡')
async def ygoMethod(bot, ev):
    key = ev.message.extract_plain_text().strip()
    imgs = (await main(key))[:ygo_max]
    msg = None
    if len(imgs) == 0:
        await bot.finish(ev,f"没有查找到关键字卡片")
    else:
        mes_list = []
        for img in imgs:
            msg = f'[CQ:image,file={img}]' 
            data = {
                "type": "node",
                "data": {
                    "name": "看什么看！",
                    "uin": "1768195747",
                    "content":msg
                        }
                    }
            mes_list.append(data)
    await bot.send_group_forward_msg(group_id=ev['group_id'], messages=mes_list)



async def main(key: str):
    url = f"https://ygocdb.com/?search={key}"
    headers = {
        'user-agent': 'nonebot-plugin-ygo',
        'referer': 'https://ygocdb.com/',
    }
    imgs = []
    async with aiohttp.ClientSession() as session:
        c = await session.get(url=url, headers=headers)
        text = (await c.content.read()).decode()
        imgs = re.findall('<img data-original="(.*?)!half">', text)
    return imgs

