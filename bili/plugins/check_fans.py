from nonebot import on_command, CommandSession
import requests
import asyncio
import datetime
import json


@on_command('fans', aliases=('查询小妹粉丝数', '粉丝数', '小妹粉丝'), only_to_me=False)
async def weather(session: CommandSession):
    loop = asyncio.get_event_loop()
    text = await loop.run_in_executor(None, requests.get, 'https://api.bilibili.com/x/relation/stat?vmid=364225566')
    follower = str(json.loads(text.text)['data']['follower'])
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await session.send('截止到{}，粉丝数为{}'.format(now, follower))
