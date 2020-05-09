from nonebot_local import on_command, CommandSession
import re
import nonebot_local
import datetime
import utils as u
import html


@on_command('zhuanfazhuanfazhuanfa', only_to_me=False)
async def _(session: CommandSession):
    bot = nonebot_local.get_bot()
    if not u.check_zhuanfa(session):
        return
    content = session.ctx['message'][0]['data']['content']
    try:
        av = content.split('www.bilibili.com/video/')[1].split('/?p=')[0]
        data = await u.web_get('https://api.bilibili.com/x/web-interface/view?bvid={}'.format(av[2:]))
        mid = data['data']['owner']['mid']
        if mid in bot.config.zhuanfa:
            await send_feedback(session, data['data']['title'], content, bot)
    except Exception:
        try:
            title = content.split('"desc":"')[1].split('"')[0]
            await send_feedback(session, title, content, bot, type=1)
        except IndexError:
            print('111111111111111111111111111')
            print(content)


def get_re_str(str_):
    str__ = ''
    for each in str_:
        if each in ['$', '(', ')', '*', '+', '.', '[', ']', '?', '\\', '^', '{', '}', '|']:
            str__ += '\\' + each
        else:
            str__ += each
    return str__


async def send_feedback(session, title, content, bot, type=1):
    if check_content(session, content, type):
        await session.send('[CQ:at,qq={}]盗别人转发的biss'.format(session.ctx['user_id']))
    else:
        mongo_db = bot.config.mongo_db['keientist']
        title = html.unescape(title)
        re_str = title[:-4]
        if len(re_str) > 30:
            re_str = re_str[:30]
        re_str = get_re_str(re_str)
        filter_data = {'title': re.compile(re_str)}
        check_data = await u.db_executor(mongo_db.zhuanfa_list.find_one, filter_data)
        if check_data:
            video_id = check_data['av'] if check_data.get('av') else check_data['bv']
            date = datetime.datetime.fromtimestamp(check_data['ctime'])
            days = datetime.timedelta(days=7)
            if date + days < datetime.datetime.now():
                await session.send('[CQ:at,qq={}]\n感谢转发，内容：{}\n不过，这个视频超出7天时间不会被记录啦'.format(
                    session.ctx['user_id'], title))
                return
            success = True
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            filter_user = {'qq': session.ctx['user_id']}
            check_user = await u.db_executor(mongo_db.zhuanfa_user.find_one, filter_user)
            if not check_user:
                check_user = {'qq': session.ctx['user_id'], 'data': {video_id: {'count': 1, 'uptime': today}}}
                await u.db_executor(mongo_db.zhuanfa_user.insert, check_user)
            else:
                av_data = check_user['data'].get(video_id)
                count = 2 if video_id in bot.config.zhuanfa_double else 1
                if av_data:
                    if av_data['uptime'] == today:
                        success = False
                    else:
                        av_data['uptime'] = today
                        av_data['count'] += count
                else:
                    check_user['data'][video_id] = {'count': count, 'uptime': today}
                await u.db_executor(mongo_db.zhuanfa_user.save, check_user)
            if success:
                await session.send('[CQ:at,qq={}]\n感谢转发，内容：{}'.format(session.ctx['user_id'], title))
            else:
                await session.send('[CQ:at,qq={}]\n感谢转发，内容：{}\n不过本机器人一天只记录第一次转发哦'.format(
                    session.ctx['user_id'], title))


def check_content(session, content, type):
    if type == 1:
        qq = content.split('"uin":')[1].split('}')[0]
        return int(qq) != session.ctx['user_id']
    else:
        len_1 = len(content.split('android_pkg_name')[0])
        len_2 = len(content.split('source_url')[0])
        return len_1 > len_2


@on_command('zhuanfazhuanfazhuanfa_2', only_to_me=False)
async def _(session: CommandSession):
    if not u.check_zhuanfa(session):
        return
    bot = nonebot_local.get_bot()
    content = session.ctx['message'][0]['data']['content']
    try:
        title = content.split('"title":"')[1].split('"')[0]
        await send_feedback(session, title, content, bot, type=2)
    except IndexError:
        print('111111111111111111111111111')
        print(content)


@on_command('zhuanfazhuanfazhuanfa_hd', only_to_me=False)
async def _(session: CommandSession):
    if not u.check_zhuanfa(session):
        return
    bot = nonebot_local.get_bot()
    content = str(session.ctx['message'])
    try:
        title = content.split('text=')[1].split('…,url=')[0]
        await send_feedback(session, title.strip(), content, bot, type=2)
    except IndexError:
        print('111111111111111111111111111')
        print(content)


@on_command('rank', only_to_me=False)
async def _(session: CommandSession):
    if not u.check_zhuanfa(session):
        return
    bot = nonebot_local.get_bot()
    mongo_db = bot.config.mongo_db['keientist']
    rank_data = list(await u.db_executor(mongo_db.zhuanfa_user.find, {}))
    rank_list = [{'qq': rank['qq'], 'count': sum([rank['data'][key]['count'] for key in rank['data'].keys()])}
                 for rank in rank_data]
    rank_list.sort(key=lambda x: x['count'], reverse=True)
    if len(rank_list) > 10:
        rank_list = rank_list[:10]
    msg = '当前转发数排名前{}用户\n'.format(len(rank_list))
    msg += '\n'.join(['QQ: {}, 转发数: {}'.format(rank['qq'], rank['count']) for rank in rank_list])
    msg += '\n每个视频每天只会记录一次转发哦~~各位再接再厉\n转发群: 228415488'
    await session.send(msg)


@on_command('detail', only_to_me=False, shell_like=True)
async def _(session: CommandSession):
    if not u.check_zhuanfa(session):
        return
    bot = nonebot_local.get_bot()
    mongo_db = bot.config.mongo_db['keientist']
    if not u.check_1st_control(session):
        return
    argv = session.args['argv']
    try:
        qq = int(argv[0])
    except ValueError:
        await session.send('请输入正确的QQ号')
        return
    filter_ = {'qq': qq}
    qq_data = await u.db_executor(mongo_db.zhuanfa_user.find_one, filter_)
    if qq_data:
        av_dict = {av['av']: av['title'] for av in list(await u.db_executor(mongo_db.zhuanfa_list.find, {}))}
        msg = '转发明细:\n'
        msg += '\n'.join(['标题: {}\n转发次数: {}'.format(av_dict[key], qq_data['data'][key]['count'])
                          for key in qq_data['data'].keys()])
        msg += '\n本机器人替小妹谢谢你的支持'
    else:
        msg = '要么是QQ号输错了，要么是目前还木有转发记录'
    await session.send(msg)


@on_command('settlement', only_to_me=True)
async def _(session: CommandSession):
    bot = nonebot_local.get_bot()
    if session.ctx['user_id'] not in bot.config.settle_list:
        return
    mongo_db = bot.config.mongo_db['keientist']
    rank_data = list(await u.db_executor(mongo_db.zhuanfa_user.find, {}))
    rank_list = [{'qq': rank['qq'], 'count': sum([rank['data'][key]['count'] for key in rank['data'].keys()])}
                 for rank in rank_data]
    rank_list.sort(key=lambda x: x['count'], reverse=True)
    msg = '\n'.join(['QQ: {}, 转发数: {}'.format(rank['qq'], rank['count']) for rank in rank_list])
    await session.send(msg)


@on_command('finish', only_to_me=True)
async def _(session: CommandSession):
    bot = nonebot_local.get_bot()
    if session.ctx['user_id'] not in bot.config.settle_list:
        return
    mongo_db = bot.config.mongo_db['keientist']
    await u.db_executor(mongo_db.zhuanfa_user.remove, {})
    msg = '本月转发数据已初始化'
    await session.send(msg)


@on_command('转发群', only_to_me=False)
async def _(session: CommandSession):
    await session.send('转发群用于战姬众转发歌姬视频，蛋仔可完成转发应援小任务获取【贝化值】。此外还会【记录转发数】，依据数量排名每月'
                       '有小奖品抽送哦！群号：228415488\n[CQ:image,file=DEFD7FC6846CC8C3D2508BCF4E9CB795.jpg,url=https://g'
                       'chat.qpic.cn/gchatpic_new/791949127/827725907-3174956380-DEFD7FC6846CC8C3D2508BCF4E9CB795/0?ter'
                       'm=2]')


# @on_command('转发抽奖', only_to_me=True)
# async def _(session: CommandSession):
#     bot = nonebot_local.get_bot()
#     if session.ctx['user_id'] not in bot.config.settle_list:
#         return
#     await session.send('种子随机数为: 474\n中奖用户为: 260074725\n种子随机数为: 143\n中奖用户为: 759906494\n种子随机数为: 1053'
#                        '\n中奖用户为: 874122811\n种子随机数为: 2466\n中奖用户为: 527418826\n种子随机数为: 3664\n中奖用户为: 35'
#                        '09374368')
