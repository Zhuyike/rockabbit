import nonebot
from aiocqhttp.exceptions import Error as CQHttpError
import datetime


@nonebot.scheduler.scheduled_job('cron', hour='*')
async def _():
    bot = nonebot.get_bot()
    now = datetime.datetime.now()
    try:
        await bot.send_group_msg(group_id=806609845,
                                 message=f'现在{now.hour}点整啦！')
    except CQHttpError:
        pass
