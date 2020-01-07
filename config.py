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
check_status_list = [806609845, 872841902]
report_time_list = [806609845, 872841902]


def keientist_db_instance():
    mongo_client = MongoClient(host=mongo_host, port=mongo_port)
    mongo_client.keientist.authenticate(mongo_user, mongo_pwd)
    dbs = dict()
    dbs['keientist'] = mongo_client['keientist']
    return dbs


mongo_db = keientist_db_instance()
