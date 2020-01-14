import nonebot
import datetime
import utils as u


@nonebot.scheduler.scheduled_job('cron', hour='*')
async def _():
    bot = nonebot.get_bot()
    mongo_db = bot.config.mongo_db['keientist']
    data = await u.web_get('https://api.bilibili.com/x/relation/stat?vmid=364225566')
    follower = str(data['data']['follower'])
    now = datetime.datetime.now()
    insert_data = {'t': now.strftime("%Y-%m-%d %H"), 'count': int(follower)}
    await u.db_executor(mongo_db.fans_count.insert, insert_data)
    last_hour = now - datetime.timedelta(hours=1)
    filter_ = {'t': last_hour.strftime("%Y-%m-%d %H")}
    check_last_hour = await u.db_executor(mongo_db.fans_count.find_one, filter_)
    fans_update = int(follower) - check_last_hour["count"]
    message = f'现在{now.hour}点整啦！\n此时小妹拥有了{follower}个粉丝\n' + \
              f'较上一个小时{"涨" if fans_update >= 0 else "掉"}粉{int(abs(fans_update))}'
    if now.hour == 0:
        last_day = now - datetime.timedelta(days=1)
        filter_ = {'t': last_day.strftime("%Y-%m-%d %H")}
        check_last_day = await u.db_executor(mongo_db.fans_count.find_one, filter_)
        fans_update = int(follower) - check_last_day["count"]
        message += f'\n较昨天相比{"涨" if fans_update >= 0 else "掉"}粉{int(abs(fans_update))}'
    await u.batch_send_msg(bot.config.report_time_list, message, bot)
