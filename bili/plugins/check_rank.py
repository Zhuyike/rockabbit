import utils as u
import nonebot_local
import hyper
import json


@nonebot_local.scheduler.scheduled_job('cron', minute='*/5')
async def _():
    bot = nonebot_local.get_bot()
    if not bot.config.event_981:
        return
    target_dict = bot.config.target_dict
    mongo_db = bot.config.mongo_db['keientist']
    filter_ = {'type': "999_rank"}
    rank = await u.db_executor(mongo_db.cookie_secret.find_one, filter_)
    c = hyper.HTTP20Connection('starmicro.happyelements.cn', port=443, secure=True, ssl_context=None)
    for i in "123456":
        if rank[i] != "x":
            while True:
                try:
                    c.request('GET', '/v2/birthday/rank?event_id=999&idol_id={}'.format(i),
                              headers=bot.config.wechat_auth)
                    break
                except AttributeError:
                    pass
            data = json.loads(c.get_response().read())
            for user in data['data']:
                if user['uid'] == bot.config.my_uid:
                    if user['rank'] > rank[i]:
                        tar = data['data'][target_dict[int(i)] - 1]
                        await bot.send_msg(user_id=791949127, message='在{}榜上被人超过了, 距离目标{}名{}票'.format(
                                           bot.config.idol_dict[int(i)], target_dict[int(i)],
                                           tar['point'] - user['point']))
                    else:
                        print('{}没有被超'.format(bot.config.idol_dict[int(i)]))
                    rank[i] = user['rank']
        else:
            print('{}不打算监控'.format(bot.config.idol_dict[int(i)]))
    await u.db_executor(mongo_db.cookie_secret.save, rank)
    print("success: {}".format(rank))
