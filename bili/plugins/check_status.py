import nonebot
import requests
from bs4 import BeautifulSoup
from aiocqhttp.exceptions import Error as CQHttpError


@nonebot.scheduler.scheduled_job('cron', second='30')
async def _():
    bot = nonebot.get_bot()
    mongo_db = bot.config.mongo_db
    for key in bot.config.t_keys:
        context = requests.get('https://t.bilibili.com/topic/name/{}/feed'.format(key)).text
        context = BeautifulSoup(context, "html.parser")
        context.find_all(name='div', attrs={"class": "feed-topic"})
    try:
        await bot.send_group_msg(group_id=806609845,
                                 message="test")
    except CQHttpError:
        pass
