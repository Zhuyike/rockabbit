import requests
import asyncio
import json
import nonebot
from bs4 import BeautifulSoup
from aiocqhttp.exceptions import Error as CQHttpError


loop = asyncio.get_event_loop()
bot = nonebot.get_bot()


async def web_get(url):
    text = await loop.run_in_executor(None, requests.get, url)
    if '</html>' in text.text:
        soup = BeautifulSoup(text.text, 'lxml')
        data = soup.pre.contents
    else:
        data = text.text
    return json.loads(data)


async def db_executor(method, data):
    return await loop.run_in_executor(None, method, data)


async def batch_send_msg(groups, msg):
    for group in groups:
        try:
            await bot.send_group_msg(group_id=group, message=msg)
        except CQHttpError:
            pass


def check_1st_control(session):
    if session.ctx['group_id'] not in bot.config.check_fans_qun_list and \
            session.ctx['user_id'] not in bot.config.check_fans_qq_list:
        return False
    return True