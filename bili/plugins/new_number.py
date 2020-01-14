from nonebot import on_notice, NoticeSession
import nonebot


@on_notice('group_increase')
async def _(session: NoticeSession):
    bot = nonebot.get_bot()
    if session.ctx['group_id'] not in bot.config.new_number_list:
        return
    await session.send('欢迎新战姬众～[CQ:at,qq={}]\n本萌新机器人还在开发中'.format(session.ctx['user_id']))
