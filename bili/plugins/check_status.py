import nonebot
import requests
import asyncio
import json
from aiocqhttp.exceptions import Error as CQHttpError


@nonebot.scheduler.scheduled_job('cron', second='*/30')
async def _():
    bot = nonebot.get_bot()
    loop = asyncio.get_event_loop()
    mongo_db = bot.config.mongo_db['keientist']
    text = await loop.run_in_executor(None, requests.get, 'https://api.bilibili.com/x/tag/detail?pn=1&ps=20&tag_id=8402119')
    data = json.loads(text.text)
    for archive in data['data']['news']['archives']:
        av_id = 'av' + str(archive['aid'])
        filter_ = {'av': av_id}
        check_data = await loop.run_in_executor(None, mongo_db.bili_av.find_one, filter_)
        if check_data:
            pass
        else:
            for group in bot.config.check_status_list:
                try:
                    await bot.send_group_msg(group_id=group,
                                             message="有新的歌姬相关视频了\n" +
                                                     "UP主：{}，标题：{}\n".format(archive['owner']['name'], archive['title']) +
                                                     "https://www.bilibili.com/video/{}，快去抢热评".format(av_id))
                    insert_data = {'av': av_id, 'read': True}
                    await loop.run_in_executor(None, mongo_db.bili_av.insert, insert_data)
                except CQHttpError:
                    pass
