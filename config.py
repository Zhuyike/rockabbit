from nonebot_local.default_config import *
from pymongo import MongoClient
import configparser
import oss2


conf = configparser.ConfigParser()
conf.read('server.conf')
VERSION = "1.04 at.2020-05-21 16:01"
AUTHOR = "QQ791949127"

SUPERUSERS = [791949127, ]
COMMAND_START = ['', '/', '!', '／', '！', ]
HOST = '0.0.0.0'
PORT = 32409
t_keys = ['战斗吧歌姬', ]
mongo_host = conf.get("mongo", "mongo_host")
mongo_port = int(conf.get("mongo", "mongo_port"))
mongo_user = conf.get("mongo", "mongo_user")
mongo_pwd = conf.get("mongo", "mongo_pwd")
check_status_list = [806609845, 872841902, 827725907, 1065224474]
report_time_list = [806609845, 872841902]
check_fans_qun_list = [806609845, 872841902]
check_fans_qq_list = [791949127, 2893023449, 275535369, 940864516, 514864750, 435271985, 1486280626, 870409697,
                      2890368941, 1421580201, 2503392408, 742869912, 365696064, 2250385220, 826751365, 496000076,
                      937549550, 1163712411]
check_swiss_list = [791949127]
new_number_list = [827725907, 983826586, 1065224474]
black_list = [14843979, 282481375, 25585072, 200415385, 36409520, 265999599, 13324344]
settle_list = [791949127, 759906494]
white_list = [364225566]
zhuanfa = [364225566]
zhuanfa_list = [228415488, 827725907, 872841902, 806609845, 1065224474]
zhuanfa_double = ['av89216498', 'av89225040', 'av89219859', 'av92643783', 'av94360241', 'av94481794']
score_admin = []
DEBUG = False
event_981 = True
my_uid = 31189
idol_dict = {1: '卡缇娅',
             2: '罗兹',
             3: '李清歌',
             4: '伊莎贝拉',
             5: '玉藻',
             6: '墨汐'}
target_dict = {1: 30,
               2: 30,
               3: 30,
               4: 30,
               5: 30,
               6: 30}

oss_Address = conf.get("oss", "oss_Address")
oss_Address_Download = conf.get("oss", "oss_Address_Download")
oss_Bucket = conf.get("oss", "oss_Bucket")
oss_Prefix_antifan = conf.get("oss", "oss_Prefix_antifan")


def keientist_db_instance():
    mongo_client = MongoClient(host=mongo_host, port=mongo_port)
    mongo_client.keientist.authenticate(mongo_user, mongo_pwd)
    dbs = dict()
    dbs['keientist'] = mongo_client['keientist']
    return dbs

# def oss2_instance():
#     auth = oss2.Auth('', '')
#     bucket = oss2.Bucket(auth, 'http://oss-cn-beijing.aliyuncs.com', 'keientist')


def get_wechat_auth():
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'x-timezone-offset': '8',
        'accept': '*/*',
        'authorization': conf.get("wechat", "auth"),
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
