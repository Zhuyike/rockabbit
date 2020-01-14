import nonebot
import utils as u


@nonebot.scheduler.scheduled_job('cron', second='*/30')
async def _():
    bot = nonebot.get_bot()
    mongo_db = bot.config.mongo_db['keientist']
    data = await u.web_get('https://api.bilibili.com/x/tag/detail?pn=1&ps=20&tag_id=8402119')
    data_revdol = await u.web_get('https://api.bilibili.com/x/web-interface/search/type?page=1&order=pubdate&keyword=战'
                                  '斗吧歌姬&duration=0&__refresh__=true&search_type=video&tids=0&highlight=1&single_col'
                                  'umn=0')
    for archive in data['data']['news']['archives']:
        if int(archive['owner']['mid']) in bot.config.black_list:
            continue
        av_id = 'av' + str(archive['aid'])
        filter_ = {'av': av_id}
        check_data = await u.db_executor(mongo_db.bili_av.find_one, filter_)
        if check_data:
            pass
        else:
            msg = "有新的歌姬相关视频了\nUP主：{}，标题：{}\nhttps://www.bilibili.com/video/{}，快去抢热评"\
                .format(archive['owner']['name'], archive['title'], av_id)
            await u.batch_send_msg(bot.config.check_status_list, msg, bot)
            insert_data = {'av': av_id, 'read': True}
            await u.db_executor(mongo_db.bili_av.insert, insert_data)
    for result in data_revdol['data']['result']:
        if int(result['mid']) in bot.config.black_list:
            continue
        av_id = 'av' + str(result['aid'])
        filter_ = {'av': av_id}
        check_data = await u.db_executor(mongo_db.bili_av.find_one, filter_)
        if check_data:
            pass
        else:
            msg = "有新的歌姬相关视频了\nUP主：{}，标题：{}\nhttps://www.bilibili.com/video/{}，快去抢热评" \
                .format(result['author'], result['title'], av_id)
            await u.batch_send_msg(bot.config.check_status_list, msg, bot)
            insert_data = {'av': av_id, 'read': True}
            await u.db_executor(mongo_db.bili_av.insert, insert_data)
