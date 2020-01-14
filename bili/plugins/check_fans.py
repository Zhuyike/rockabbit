from nonebot import on_command, CommandSession
import nonebot
import utils as u
import datetime


@on_command('fans', aliases=('查询小妹粉丝数', '粉丝数', '小妹粉丝'), only_to_me=False)
async def weather(session: CommandSession):
    bot = nonebot.get_bot()
    if session.ctx['group_id'] not in bot.config.check_fans_qun_list and \
            session.ctx['user_id'] not in bot.config.check_fans_qq_list:
        return
    data = await u.web_get('https://api.bilibili.com/x/relation/stat?vmid=364225566')
    follower = str(data['data']['follower'])
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await session.send('截止到{}，粉丝数为{}'.format(now, follower))
