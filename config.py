from nonebot.default_config import *
from pymongo import MongoClient

SUPERUSERS = [791949127, ]
COMMAND_START = ['', '/', '!', '／', '！', ]
HOST = '127.0.0.1'
PORT = 32409
t_keys = ['战斗吧歌姬', ]
mongo_host = '123.57.95.42'
mongo_port = 27017
mongo_user = 'keientist_admin'
mongo_pwd = 'keientist_pwd'
check_status_list = [806609845, 872841902, 827725907]
report_time_list = [806609845, 872841902]
check_fans_qun_list = [806609845, 872841902]
check_fans_qq_list = [791949127, 2893023449, 275535369, 940864516, 514864750, 435271985, 1486280626, 870409697,
                      2890368941, 1421580201, 2503392408, 742869912, 365696064, 2250385220, 826751365, 496000076,
                      937549550, 1163712411]
new_number_list = [827725907, 983826586]
black_list = [14843979, 282481375]
white_list = [364225566]
zhuanfa = [364225566]
DEBUG = False
event_903 = True
my_uid = 31189
idol_dict = {1: '卡缇娅',
             2: '罗兹',
             3: '李清歌',
             4: '伊莎贝拉',
             5: '玉藻',
             6: '墨汐'}


def keientist_db_instance():
    mongo_client = MongoClient(host=mongo_host, port=mongo_port)
    mongo_client.keientist.authenticate(mongo_user, mongo_pwd)
    dbs = dict()
    dbs['keientist'] = mongo_client['keientist']
    return dbs


def get_wechat_auth():
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'x-timezone-offset': '8',
        'accept': '*/*',
        'authorization': 'Miinno Tx5ZBthwvPdvQH9YPzRzkvNuvB-CZ7Cc_1556905329',
        'brand': 'iPhone',
        'accept-language': 'zh-cn',
        'accept-encoding': 'br, gzip, deflate',
        'platform': '1',
        'user-agent': 'Mozilla/5.0(iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.5(0x17000523) NetType/WIFI Language/zh_CN',
        'referer': 'https://servicewechat.com/wx0a48c468391428fd/61/page-frame.html',
        'model': 'iPhone 8 Plus (GSM+CDMA)<iPhone10,2>'
    }
    return headers


mongo_db = keientist_db_instance()
wechat_auth = get_wechat_auth()
