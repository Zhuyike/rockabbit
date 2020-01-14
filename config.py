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
DEBUG = False


def keientist_db_instance():
    mongo_client = MongoClient(host=mongo_host, port=mongo_port)
    mongo_client.keientist.authenticate(mongo_user, mongo_pwd)
    dbs = dict()
    dbs['keientist'] = mongo_client['keientist']
    return dbs


mongo_db = keientist_db_instance()
