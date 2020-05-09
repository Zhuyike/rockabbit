from nonebot_local import on_command, CommandSession
import nonebot_local
import utils as u
import time
import datetime


class Code(object):
    SWISS_OPEN = 1
    SWISS_CLOSE = 0


@on_command('swiss', aliases=('瑞士轮', ), only_to_me=False, shell_like=True)
async def _(session: CommandSession):
    bot = nonebot_local.get_bot()
    argv = session.args['argv']
    if len(argv) == 0:
        await session.send('缺少参数')
        return
    cmd = argv[0]
    argv = argv[1:]
    if cmd == 'new':  # 限制少数人拥有权限才可开启
        if not check_swiss_control(session, bot):
            await session.send('您并不能开启一个新比赛，如有需要请联系超管开通权限')
            return
        swiss = await get_swiss(session, bot)
        if swiss:
            await session.send('当前群内已有开启状态的比赛\nID：{}\n名称：{}'.format(str(swiss['_id']), swiss['name']))
            return
        if len(argv) < 1:
            await session.send('缺少比赛名称')
            return
        swiss = new_swiss(session, argv[0])
        await save_swiss(bot, swiss)
        await session.send('创建成功，名称：{}'.format(swiss['name']))
        return
    elif cmd == 'add':  # 由加入选手输入，swiss add 11111，由发起人输入+qq号
        swiss = await get_swiss(session, bot)
        if not swiss:
            await session.send('当前群内无开启状态的比赛')
            return
        if len(argv) == 0:
            qq = session.ctx['user_id']
            swiss['player'][str(qq)] = new_player(qq, session.ctx['sender']['card'])
            await session.send("选手已登记\nQQ：{}\n昵称：{}".format(qq, session.ctx['sender']['card']))
            await save_swiss(bot, swiss)
            return
        elif len(argv) == 2:
            if session.ctx['user_id'] != swiss['qq']:
                await session.send('当前群内比赛并不是您主持的')
            else:
                swiss['player'][str(argv[0])] = new_player(argv[0], argv[1])
                await session.send("选手已登记\nQQ：{}\n昵称：{}".format(argv[0], argv[1]))
                await save_swiss(bot, swiss)
                return
        else:
            await session.send('参数数量错误')
            return
    elif cmd == 'next':  # todo 由发起人输入，进入下一轮，输出排表
        swiss = await get_swiss(session, bot)
        if session.ctx['user_id'] != swiss['qq']:
            await session.send('当前群内比赛并不是您主持的')
        else:
            check_scb_next, result = check_swiss_can_be_next(swiss)
            if not check_scb_next:
                msg = '当前以下桌次未完成比赛：\n'
                msg += '\n'.join(['No.{}，{} vs {}'.format(table['index'], swiss['player'][str(table['left'])]['name'],
                                                          swiss['player'][str(table['right'])]['name'])for table in result])
                await session.send(msg)
            else:
                swiss = next_swiss(swiss)
                await print_game_status(swiss, session)
                await save_swiss(bot, swiss)
        return
    elif cmd == 'game_status':  # todo 由选手和发起人输入，显示排表，第几轮，比分输入情况
        success, err, swiss = await check_swiss_all(session, bot)
        if not success:
            await session.send(err)
            return
        print(1)
        await print_game_status(swiss, session)
        return
    elif cmd == 'player_status':  # todo 由选手和发起人输入，显示选手积分小分对手胜率等等
        success, err, swiss = await check_swiss_all(session, bot)
        if not success:
            await session.send(err)
            return
        if swiss['round'] == 0 or swiss['round'] == 1:
            await session.send('当前比赛并没有具体比分')
            return
        players = get_players_status(swiss)
        await print_players_status(swiss, players, session)
        return
    elif cmd == 'result':  # todo swiss result qq11111 2 1或者swiss result no22 2
        success, err, swiss = await check_swiss_owner(session, bot)
        if not success:
            await session.send(err)
            return
        if len(argv) != 3:
            await session.send('参数数量不对')
            return
        try:
            left = int(argv[1])
            right = int(argv[2])
            no = int(argv[0][2:])
        except ValueError:
            await session.send('参数类型不对')
            return
        final_score_left, final_score_right = -1, -1
        if argv[0][:2] == 'qq':
            zhuo = -1
            for index, table in enumerate(swiss['table_rank'][swiss['round'] - 1]):
                if table['left'] == no:
                    table['result'] = [left, right]
                    final_score_left, final_score_right = left, right
                    zhuo = index
                    break
                if table['right'] == no:
                    table['result'] = [right, left]
                    final_score_left, final_score_right = right, left
                    zhuo = index
                    break
            if zhuo == -1:
                await session.send('该QQ未找到对应桌次')
                return
        elif argv[0][:2] == 'no':
            try:
                swiss['table_rank'][swiss['round'] - 1][no - 1]['result'] = [left, right]
                final_score_left, final_score_right = left, right
            except IndexError:
                await session.send('该No未找到对应桌次')
                return
            zhuo = no - 1
        else:
            await session.send('参数格式不对')
            return
        table = swiss['table_rank'][swiss['round'] - 1][zhuo]
        await session.send('第{}桌，{} VS {}，比分：{}:{}，已记录'.format(
            zhuo + 1, swiss['player'][str(table['left'])]['name'],
            swiss['player'][str(table['right'])]['name'] if table['right'] != 0 else '轮空',
            final_score_left, final_score_right))
        await save_swiss(bot, swiss)
    elif cmd == 'cancel':  # todo 取消比分：swiss cancel qq11111 或者swiss cancel no22
        success, err, swiss = await check_swiss_owner(session, bot)
        if not success:
            await session.send(err)
            return
        if len(argv) != 1:
            await session.send('参数数量不对')
            return
        try:
            no = int(argv[0][2:])
        except ValueError:
            await session.send('参数类型不对')
            return
        if argv[0][:2] == 'qq':
            for table in swiss['table_rank'][swiss['round'] - 1]:
                if table['left'] == no or table['right'] == no:
                    table['result'] = [-1, -1]
                    break
        elif argv[0][:2] == 'no':
            swiss['table_rank'][swiss['round'] - 1][no - 1]['result'] = [-1, -1]
        else:
            await session.send('参数格式不对')
            return
        await save_swiss(bot, swiss)
    elif cmd == 'delete':  # todo 选手退出比赛：swiss delete 11111，由发起人输入，仅限第一轮之前
        success, err, swiss = await check_swiss_owner(session, bot)
        if not success:
            await session.send(err)
            return
        if len(argv) != 1:
            await session.send('参数数量不对')
            return
        try:
            no = int(argv[0])
        except ValueError:
            await session.send('参数类型不对')
            return
        swiss['player'].pop(str(no))
        await save_swiss(bot, swiss)
    elif cmd == 'end':  # todo 比赛结束：swiss end，由发起人输入
        success, err, swiss = await check_swiss_owner(session, bot)
        if not success:
            await session.send(err)
            return
        swiss['open'] = Code.SWISS_CLOSE
        await save_swiss(bot, swiss)
        await session.send('{}比赛已关闭 at {}'.format(swiss['name'],
                                                  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    elif cmd == 'help':  # todo 帮助
        msg = "1，新建比赛：swiss new，限制少数人拥有权限才可开启\n" \
              "2，加入比赛：swiss add，由加入选手输入，swiss add 11111，由发起人输入+qq号\n" \
              "3，进入下一轮：swiss next 由发起人输入，进入下一轮，输出排表\n" \
              "4，状态1：swiss game_status 由选手，发起人输入，显示排表，第几轮，比分输入情况\n" \
              "5，状态2：swiss player_status 由选手，发起人输入，显示选手积分小分对手胜率等等\n" \
              "6，输入比分：swiss result qq11111 2 1或者swiss result no22 2 1，\n" \
              "由发起人输入，表示qq号11111的选手2比1赢，或者第22桌前者2比后者1赢。每输入一桌会显示还剩几桌\n" \
              "7，取消比分：swiss cancel qq11111 或者swiss cancel no22\n" \
              "8，选手退出比赛：swiss delete 11111，由发起人输入，仅限第一轮之前\n" \
              "9，比赛结束：swiss end，由发起人输入\n" \
              "10，返回上一轮`：swiss back"
        await session.send(msg)
    elif cmd == 'back':  # todo 上一轮
        success, err, swiss = await check_swiss_owner(session, bot)
        if not success:
            await session.send(err)
            return
        if swiss['round'] == 0:
            await session.send('已经是第一轮了')
            return
        swiss['round'] -= 1
        swiss['table_rank'] = swiss['table_rank'][:-1]
        await save_swiss(bot, swiss)
        await session.send('已退回上一轮，当前轮数：{}'.format(swiss['round']))
    else:
        await session.send('“{}”命令不能识别'.format(cmd))
        return


async def check_swiss_owner(session, bot):
    swiss = await get_swiss(session, bot)
    if not swiss:
        return False, '当前群内无开启状态的比赛', None
    if session.ctx['user_id'] != swiss['qq']:
        return False, '当前群内没有您名下开启状态的比赛', swiss
    return True, None, swiss


async def check_swiss_all(session, bot):
    swiss = await get_swiss(session, bot)
    if not swiss:
        return False, '当前群内无开启状态的比赛', None
    if session.ctx['user_id'] != swiss['qq']:
        flag = True
        for player in swiss['player'].keys():
            if int(player) == session.ctx['user_id']:
                flag = False
                break
        if flag:
            return False, '您并未参与当前群内比赛', swiss
    return True, None, swiss


async def print_players_status(swiss, players, session):
    msg = '现在已完成前{}轮，选手排名如下：\n'.format(swiss['round'] - 1)
    msg += '\n'.join(['ID：{}，积分：{}，对手胜率：{}%'.format(
        swiss['player'][str(player['qq'])]['name'], player['score'],
        round(player['op_rate'] * 100, 1)) for player in players])
    await session.send(msg)


async def print_game_status(swiss, session):
    msg = '现在是第{}轮，桌次如下：\n'.format(swiss['round'])
    msg += '\n'.join(["第{}桌，{}VS{}, {}完成{}".format(
        index + 1, swiss['player'][str(table['left'])]['name'],
        swiss['player'][str(table['right'])]['name'] if table['right'] != 0 else '轮空',
        '未' if table['result'] == [-1, -1] else '已',
        '，比分是：{}:{}'.format(table['result'][0], table['result'][1]) if table['result'] != [-1, -1] else '')
                      for index, table in enumerate(swiss['table_rank'][swiss['round'] - 1])])
    await session.send(msg)


def get_players_status(swiss):
    players = {int(player): {'score': 0, 'op': list(), 'win': 0, 'total': 0} for player in swiss['player'].keys()}
    for lun in range(swiss['round'] - 1):
        for player in players.keys():
            players[player]['op'].append(0)
        for table in swiss['table_rank'][lun]:
            players[table['left']]['op'][lun] = table['right']
            if table['right'] != 0:
                players[table['right']]['op'][lun] = table['left']
            if table['right'] == 0:
                players[table['left']]['score'] += 3
            else:
                if table['result'][0] > table['result'][1]:
                    players[table['left']]['score'] += 3
                elif table['result'][0] < table['result'][1]:
                    players[table['right']]['score'] += 3
                else:
                    players[table['right']]['score'] += 1
                    players[table['left']]['score'] += 1
                players[table['left']]['win'] += table['result'][0]
                players[table['left']]['total'] += table['result'][0] + table['result'][1]
                players[table['right']]['win'] += table['result'][1]
                players[table['right']]['total'] += table['result'][0] + table['result'][1]
    for player in players.keys():
        rate_total = 0.0
        for op in players[player]['op']:
            if op != 0:
                rate_total += float(players[op]['win']) / float(players[op]['total'])
        players[player]['op_rate'] = rate_total / len(players[player]['op'])
        players[player]['k'] = players[player]['score'] + players[player]['op_rate']
        players[player]['qq'] = player
    players = [players[player] for player in players.keys()]
    players.sort(key=lambda x: x['k'], reverse=True)
    return players


def next_swiss(swiss):
    swiss = get_lun(swiss, random=1 if swiss['round'] == 0 else 0)
    return swiss


def get_lun(swiss, random=0):
    import random as r
    if random == 1:
        players = [{'qq': int(player), 'k': r.random(), 'op': list()} for player in swiss['player'].keys()]
        players.sort(key=lambda x: x['k'])
    else:
        players = get_players_status(swiss)
    swiss['round'] += 1
    point = 0
    swiss['table_rank'].append(list())
    total_players = len(players)
    while point < total_players:
        if total_players == point + 1:
            swiss['table_rank'][swiss['round'] - 1].append(new_table(players[point]['qq'], 0))
        else:
            swiss['table_rank'][swiss['round'] - 1].append(new_table(players[point]['qq'], players[point + 1]['qq']))
        point += 2
    if random == 0:
        swiss = check_repeat(swiss, players)
    return swiss


def check_repeat(swiss, players):
    repeat = swiss['check_repeat'] if swiss['round'] > swiss['check_repeat'] else swiss['round']
    players = {player['qq']: player for player in players}
    for index, table in enumerate(swiss['table_rank'][swiss['round'] - 1]):
        # print(-repeat)
        # print(players)
        # print(table['right'])
        # print(players[table['right']]['op'])
        if table['right'] != 0 and table['left'] in players[table['right']]['op'][-repeat:]:
            point = index + 1
            while point < len(swiss['table_rank']):
                if swiss['table_rank'][swiss['round'] - 1][point]['left'] not in players[table['right']]['op'][-repeat:] and \
                        (swiss['table_rank'][swiss['round'] - 1][point]['right'] not in players[table['left']]['op'][-repeat:] or
                         swiss['table_rank'][swiss['round'] - 1][point]['right'] == 0):
                    swiss['table_rank'][swiss['round'] - 1][point]['left'], table['right'] = \
                        table['right'], swiss['table_rank'][swiss['round'] - 1][point]['left']
                    break
                if (swiss['table_rank'][swiss['round'] - 1][point]['right'] not in players[table['right']]['op'][-repeat:] or
                    swiss['table_rank'][swiss['round'] - 1][point]['right'] == 0) and \
                        swiss['table_rank'][swiss['round'] - 1][point]['left'] not in players[table['left']]['op'][-repeat:]:
                    swiss['table_rank'][swiss['round'] - 1][point]['right'], table['right'] = \
                        table['right'], swiss['table_rank'][swiss['round'] - 1][point]['right']
                    break
    return swiss


def check_swiss_can_be_next(swiss):
    if swiss['round'] == 0:
        return True, list()
    failed = list()
    for table in swiss['table_rank'][swiss['round'] - 1]:
        if table['result'][0] == -1:
            failed.append(table)
    if failed:
        return False, failed
    return True, failed


def new_table(qq_1, qq_2, index=0):
    return dict(left=qq_1, right=qq_2, result=[-1, -1], index=index)


def new_player(qq, nickname):
    return dict(name=nickname, qq=qq)


def new_swiss(session, name):
    return dict(name=name, qq=session.ctx['user_id'], group=session.ctx['group_id'], player=dict(), ctime=time.time(),
                open=Code.SWISS_OPEN, round=0, table_rank=list(), check_repeat=1)


def check_swiss_control(session, bot):
    if session.ctx['user_id'] not in bot.config.check_swiss_list:
        return False
    return True


async def get_swiss(session, bot):
    mongo_db = bot.config.mongo_db['keientist']
    try:
        group_id = session.ctx['group_id']
    except KeyError:
        return None
    filter_ = {'open': Code.SWISS_OPEN, 'group': group_id}
    return await u.db_executor(mongo_db.swiss.find_one, filter_)


async def save_swiss(bot, swiss):
    mongo_db = bot.config.mongo_db['keientist']
    await u.db_executor(mongo_db.swiss.save, swiss)
