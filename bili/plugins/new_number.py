from nonebot_local import on_notice, NoticeSession
import nonebot_local


@on_notice('group_increase')
async def _(session: NoticeSession):
    bot = nonebot_local.get_bot()
    if session.ctx['group_id'] not in bot.config.new_number_list:
        return
    await session.send('欢迎新战姬众～[CQ:at,qq={}]\n请认真看完置顶的群公告'.format(session.ctx['user_id']))
