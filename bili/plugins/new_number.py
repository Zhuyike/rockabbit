from nonebot import on_notice, NoticeSession
import nonebot


@on_notice('group_increase')
async def _(session: NoticeSession):
    bot = nonebot.get_bot()
    if session.ctx['group_id'] not in bot.config.new_number_list:
        return
    await session.send('欢迎新战姬众～[CQ:at,qq={}]\n请认真看完置顶的群公告（暴躁老哥模式）\n顺便： https://wj.qq.com/s2/5662973/8258/ live相关的问卷了解一下'.format(session.ctx['user_id']))
