from nonebot_local import on_command, CommandSession
import re
import nonebot_local
import datetime
import utils as u


@on_command('cq_image_tongji____xxxx', only_to_me=False)
async def _(session: CommandSession):
    if not u.check_zhuanfa(session):
        return
    msgs = session.ctx['message']
    for msg in msgs:
        if msg['type'] == 'image':
            mongo_db = nonebot_local.get_bot().config.mongo_db['keientist']
            now = datetime.datetime.now()
            insert_data = {'t': now.strftime("%Y-%m-%d %H:%M:%S"), 'file': msg['data']['file'],
                           'url': msg['data']['url'], 'qq': session.ctx['user_id']}
            await u.db_executor(mongo_db.img_status.insert, insert_data)
            print(insert_data)


@on_command('img_status', aliases='康康表情包', only_to_me=False)
async def _(session: CommandSession):
    if not u.check_1st_control(session):
        return
    mongo_db = nonebot_local.get_bot().config.mongo_db['keientist']
    data = list(await u.db_executor(mongo_db.img_status.find, {}))
    cal = dict()
    url = dict()
    for img_ in data:
        cal[img_['file']] = cal.get(img_['file'], 0) + 1
        url[img_['file']] = img_['url']
    img_list = [{'file': k, 'cal': v, 'url': url[k]} for k, v in cal.items()]
    img_list.sort(key=lambda x: x['cal'], reverse=True)
    if len(img_list) > 5:
        img_list = img_list[:5]
    msg = '当前使用数量排名前{}的表情包\n'.format(len(img_list))
    msg += '\n'.join(['MD5: {}, 使用数: {}{}'.format(img_['file'].split('.')[0], img_['cal'],
                                                  '[CQ:image,file={},url={}]'.format(img_['file'], img_['url']))
                      for img_ in img_list])
    await session.send(msg)
