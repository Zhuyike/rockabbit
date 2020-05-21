from abc import ABC

from nonebot_local import on_command, CommandSession, permission as perm
import nonebot_local
import utils as u
import datetime
import tornado.web
import tornado.ioloop
import time


# @on_command('test', only_to_me=False, permission=perm.SUPERUSER)
# async def weather(session: CommandSession):
#     print(session.ctx)
#     print(session.args)
#     data = await u.web_get('https://api.bilibili.com/x/relation/stat?vmid=364225566')
#     follower = str(data['data']['follower'])
#     now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     await session.send('截止到{}，粉丝数为{}'.format(now, follower))


@on_command('test_teat', only_to_me=False, permission=perm.SUPERUSER)
async def _(session: CommandSession):
    class MainHandler(tornado.web.RequestHandler):
        async def get(self):
            await session.send('接收到了报警：\n{}'.format(self.request.arguments.get('ctx')))
            self.write("朕知道了\n{}".format(self.request.arguments.get('ctx')))
    application = tornado.web.Application([
        (r"/report", MainHandler),
    ])
    await session.send('start')
    application.listen(9999)
    tornado.ioloop.IOLoop.instance().start()
    while True:
        print("web server available")
        time.sleep(300)


@on_command('抵制高仿', aliases=('高仿', '缝合姬'), only_to_me=False)
async def _(session: CommandSession):
    await session.send('为什么要抵制高仿，先是用高仿名字蹭热度、引流，别的高仿号也就评论区抖机灵，这高仿在无授权的情况下发布录播。小妹'
                       '几次找到他要求改名还置之不理，最后被人举报和谐掉了再改个应援会的名字，美名其曰顾全大局。要求他人改名殊不知自己'
                       '就是这般无赖')


@on_command('引流', only_to_me=False)
async def _(session: CommandSession):
    if not u.check_1st_control(session):
        return
    await session.send('引流最严重的几次就像鸭鸭的cyberangel，本体播放12万，加上被引流吸血吸掉的5万，就是17万，但要考虑到b站播放越高'
                       '曝光也越多，这个视频起码能上20万，20万播放的视频能涨多少粉？所以需要大家抵制高仿')


@on_command('_version', only_to_me=False)
async def _(session: CommandSession):
    bot = nonebot_local.get_bot()
    await session.send('Version: {}\nAuthor: {}'.format(bot.config.VERSION, bot.config.AUTHOR))


@on_command('try_error', only_to_me=False)
async def _(session: CommandSession):
    await session.send('Error: {}'.format(1 / 0))
