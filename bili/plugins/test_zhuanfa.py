from nonebot import on_command, CommandSession
import re
import nonebot
import datetime
import utils as u


@on_command('zhuanfazhuanfazhuanfa', only_to_me=False)
async def _(session: CommandSession):
    bot = nonebot.get_bot()
    content = session.ctx['message'][0]['data']['content']
    try:
        av = content.split('www.bilibili.com/video/')[1].split('/?p=')[0]
        data = await u.web_get('https://api.bilibili.com/x/web-interface/view?aid={}'.format(av[2:]))
        mid = data['data']['owner']['mid']
        if mid in bot.config.zhuanfa:
            await send_feedback(session, data['data']['title'], content, bot)
    except IndexError:
        try:
            title = content.split('"desc":"')[1].split('"')[0]
            await send_feedback(session, title, content, bot, type=1)
        except IndexError:
            print('111111111111111111111111111')
            print(content)


async def send_feedback(session, title, content, bot, type=1):
    if check_content(session, content, type):
        await session.send('盗别人转发的biss')
    else:
        mongo_db = bot.config.mongo_db['keientist']
        filter_data = {'title': re.compile(title[:-4])}
        check_data = await u.db_executor(mongo_db.zhuanfa_list.find_one, filter_data)
        if check_data:
            success = True
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            filter_user = {'qq': session.ctx['user_id']}
            check_user = await u.db_executor(mongo_db.zhuanfa_user.find_one, filter_user)
            if not check_user:
                check_user = {'qq': session.ctx['user_id'], 'data': {check_data['av']: {'count': 1, 'uptime': today}}}
                await u.db_executor(mongo_db.zhuanfa_user.insert, check_user)
            else:
                av_data = check_user['data'].get(check_data['av'])
                if av_data:
                    if av_data['uptime'] == today:
                        success = False
                    else:
                        av_data['uptime'] = today
                        av_data['count'] += 1
                else:
                    check_user['data'][check_data['av']] = {'count': 1, 'uptime': today}
                await u.db_executor(mongo_db.zhuanfa_user.save, check_user)
            if success:
                await session.send('感谢转发，内容：{}'.format(title))
            else:
                await session.send('感谢转发，内容：{}\n不过本机器人一天只记录第一次转发哦'.format(title))


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
    bot = nonebot.get_bot()
    content = session.ctx['message'][0]['data']['content']
    try:
        title = content.split('"title":"')[1].split('"')[0]
        await send_feedback(session, title, content, bot, type=2)
    except IndexError:
        print('111111111111111111111111111')
        print(content)
