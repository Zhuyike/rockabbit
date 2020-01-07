import nonebot
from aiocqhttp.exceptions import Error as CQHttpError
import datetime


@nonebot.scheduler.scheduled_job('cron', hour='*')
async def _():
    bot = nonebot.get_bot()
    now = datetime.datetime.now()
    for group in bot.config.report_time_list:
        try:
            await bot.send_group_msg(group_id=group,
                                     message=f'现在{now.hour}点整啦！')
        except CQHttpError:
            pass
