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
            msg = get_msg(archive['owner']['name'], archive['title'], av_id, bot)
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
            msg = get_msg(result['author'], result['title'], av_id, bot)
            await u.batch_send_msg(bot.config.check_status_list, msg, bot)
            insert_data = {'av': av_id, 'read': True}
            await u.db_executor(mongo_db.bili_av.insert, insert_data)


def get_msg(author, title, av_id, bot):
    if author in bot.config.white_list:
        msg = "啊啊啊啊啊，这这这这是小妹的新视频，啊啊啊啊啊\nUP主：{}，标题：{}\nhttps://www.bilibili.com/video/{}\n大家、大家" \
              "、一定一定一定转发转发转发，然后是点赞投币收藏三连\n现在b站的转发进热门的比重是最大最大最大的!"\
            .format(author, title, av_id)
    else:
        msg = "有新的歌姬相关视频了\nUP主：{}，标题：{}\nhttps://www.bilibili.com/video/{}，快去抢热评" \
            .format(author, title, av_id)
    return msg
