from nonebot import on_command, CommandSession, permission as perm
import nonebot
import utils as u
import datetime


@on_command('test', only_to_me=False, permission=perm.SUPERUSER)
async def weather(session: CommandSession):
    print(session.ctx)
    print(session.args)
    data = await u.web_get('https://api.bilibili.com/x/relation/stat?vmid=364225566')
    follower = str(data['data']['follower'])
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await session.send('截止到{}，粉丝数为{}'.format(now, follower))
