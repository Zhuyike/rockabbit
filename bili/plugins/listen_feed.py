import nonebot
from aiocqhttp.exceptions import Error as CQHttpError


@nonebot.scheduler.scheduled_job('cron', hour='*')
async def _():
    bot = nonebot.get_bot()
    try:
        await bot.send_group_msg(group_id=1,
                                 message=f'现在{now.hour}点整啦！')
    except CQHttpError:
        pass