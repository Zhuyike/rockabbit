from nonebot import on_command, CommandSession
import nonebot
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
            await send_feedback(session, data['data']['title'], content)
    except IndexError:
        try:
            title = content.split('"desc":"')[1].split('"')[0]
            await send_feedback(session, title, content)
        except IndexError:
            print('111111111111111111111111111')
            print(content)


async def send_feedback(session, title, content):
    qq = content.split('"uin":')[1].split('}')[0]
    if int(qq) != session.ctx['user_id']:
        await session.send('盗别人转发的biss')
    else:
        await session.send('感谢转发，内容：{}'.format(title))
