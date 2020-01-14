import requests
import asyncio
import json
from aiocqhttp.exceptions import Error as CQHttpError


loop = asyncio.get_event_loop()


async def web_get(url):
    text = await loop.run_in_executor(None, requests.get, url)
    return json.loads(text.text)


async def db_executor(method, data):
    return await loop.run_in_executor(None, method, data)


async def batch_send_msg(groups, msg, bot):
    for group in groups:
        try:
            await bot.send_group_msg(group_id=group, message=msg)
        except CQHttpError:
            pass
