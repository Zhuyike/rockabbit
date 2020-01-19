import utils as u
import nonebot
import hyper
import json


@nonebot.scheduler.scheduled_job('cron', second='1', minute='*/5')
async def _():
    bot = nonebot.get_bot()
    if not bot.config.event_903:
        return
    mongo_db = bot.config.mongo_db['keientist']
    filter_ = {'type': "903_rank"}
    rank = await u.db_executor(mongo_db.cookie_secret.find_one, filter_)
    print(rank)
    c = hyper.HTTP20Connection('starmicro.happyelements.cn', port=443, secure=True, ssl_context=None)
    for i in "123456":
        if rank[i] != "x":
            while True:
                try:
                    c.request('GET', '/v2/new-year/supporter-rank?event_id=903&idol_id={}'.format(i),
                              headers=bot.config.wechat_auth)
                    break
                except AttributeError:
                    pass
            data = json.loads(c.get_response().read())
            for user in data['data']:
                if user['uid'] == bot.config.my_uid:
                    if user['rank'] > rank[i]:
                        await bot.send(context={'user_id': '791949127'},
                                       message='在{}榜上被人超过了'.format(bot.config.idol_dict[int(i)]))
                    else:
                        print('{}没有被超'.format(bot.config.idol_dict[int(i)]))
                    rank[i] = user['rank']
        else:
            print('{}不打算监控'.format(bot.config.idol_dict[int(i)]))
    await u.db_executor(mongo_db.cookie_secret.save, rank)
    print("success: {}".format(rank))
