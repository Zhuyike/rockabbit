from nonebot import on_command, CommandSession
import utils as u
import datetime


@on_command('check', aliases=('查询视频', '四连情况如何'), only_to_me=False, shell_like=True)
async def weather(session: CommandSession):
    if not u.check_1st_control(session):
        return
    argv = session.args['argv']
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = '截止到{}\n'.format(now)
    if len(argv) == 0 or (len(argv) == 1 and len(argv[0]) == 1):
        data = await u.web_get('https://api.bilibili.com/x/space/arc/search?mid=364225566&pn=1&ps=25')
        for index in range(5 if len(argv) == 0 else int(argv[0])):
            status = data['data']['list']['vlist'][index]
            av_id = status['aid']
            data_v = await u.web_get('https://api.bilibili.com/x/web-interface/view?aid={}'.format(av_id))
            data_v = data_v['data']['stat']
            msg += '标题：{}\n播放数：{}\n赞：{}\n硬币：{}\n收藏：{}\n转发：{}\n\n'.format(
                status['title'], data_v['view'], data_v['like'], data_v['coin'], data_v['favorite'], data_v['share'])
    else:
        for arg in argv:
            av_id = arg[2:] if 'av' in arg or 'AV' in arg else arg
            data = await u.web_get('https://api.bilibili.com/x/web-interface/view?aid={}'.format(av_id))
            name_data = data['data']
            data = data['data']['stat']
            msg += '标题：{}\n播放数：{}\n赞：{}\n硬币：{}\n收藏：{}\n转发：{}\n\n'.format(
                name_data['title'], data['view'], data['like'], data['coin'], data['favorite'], data['share'])
    await session.send(msg + '当前同时观看人数仍在开发中')
