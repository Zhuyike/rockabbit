from nonebot_local import on_command, CommandSession
import utils as u
import datetime


@on_command('fans', aliases=('查询小妹粉丝数', '粉丝数', '小妹粉丝'), only_to_me=False)
async def weather(session: CommandSession):
    if not u.check_1st_control(session):
        return
    data = await u.web_get('https://api.bilibili.com/x/relation/stat?vmid=364225566')
    follower = str(data['data']['follower'])
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await session.send('截止到{}，粉丝数为{}'.format(now, follower))
