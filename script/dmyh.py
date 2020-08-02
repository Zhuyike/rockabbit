# -*- coding: utf-8 -*-
import time
import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup

# search_url = 'https://acg.rip/?term='
# main_url = 'https://acg.rip'
topic_list = ['0{}'.format(i) if len(str(i)) == 1 else str(i) for i in range(1, 50)]


def fetch(db_):
    data = db_.bangumi.find_one({'status': 1})
    print(data)
    target_list_ = [[bangumi['label'], bangumi['name'], bangumi['topic']] for bangumi in data['bangumi']]
    return target_list_


def search(target_list_, main_url):
    # res = requests.get(main_url)
    # tr_obj = BeautifulSoup(res.text, 'html.parser').find_all('tr')
    # target_url_ = list()
    # for tr in tr_obj[1:]:
    #     title = tr.find('span', class_='title').find('a').contents[0]
    #     for target in target_list_:
    #         topic = str(target[2])
    #         if len(topic) == 1:
    #             topic = '0' + topic
    #         if '1080p' in title:
    #             title = ''.join(title.split('1080p'))
    #             if target[0] in title and target[1] in title and\
    #                     (' {} '.format(topic) in title or '[{}]'.format(topic) in title):
    #                 uri = tr.find('td', class_='action').find('a')
    #                 print(uri)
    #                 url = {'url': main_url + uri.get('href'), 'name': target[1], 'topic': topic}
    #                 target_url_.append(url)
    #                 target[2] += 1
    target_url_ = list()
    for target in target_list_:
        topic_cached = list()
        res = requests.get('{}/?term={}+{}+1080'.format(main_url, target[0], target[1]))
        while True:
            tr_obj = BeautifulSoup(res.text, 'html.parser').find_all('tr')
            for tr in tr_obj[1:]:
                title = tr.find('span', class_='title').find('a').contents[0]
                for topic in topic_list:
                    if int(topic) < target[2]:
                        continue
                    if ('[{}]'.format(topic) in title or ' {} '.format(topic) in title)\
                            and ('简' in title or 'chs' in title or 'CHT' in title):
                        print(title)
                        if topic not in topic_cached:
                            uri = tr.find('td', class_='action').find('a')
                            print(uri)
                            url = {'url': main_url + uri.get('href'), 'name': target[1], 'topic': topic}
                            target_url_.append(url)
                            topic_cached.append(topic)
            target_topic = str(target[2])
            if len(target_topic) == 1:
                target_topic = '0' + target_topic
            if target_topic not in topic_cached:
                res = requests.get('{}/page/2?term={}+{}+1080'.format(main_url, target[0], target[1]))
            else:
                break
        target[2] = max([int(url['topic']) for url in target_url_ if url['name'] == target[1]]) + 1
        time.sleep(5)
    return target_list_, target_url_


def download(target_url_, pwd):
    for url_ in target_url_:
        r = requests.get(url_['url'])
        with open("{}{}_{}.torrent".format(pwd, url_['name'], url_['topic']), "wb") as f:
            f.write(r.content)


def keientist_db_instance():
    mongo_client = MongoClient(host='123.57.95.42', port=27017)
    mongo_client.keientist.authenticate('keientist_admin', 'keientist_pwd')
    return mongo_client['keientist']


def save(db_, target_list_):
    bangumi = [{'name': target[1], 'label': target[0], 'topic': target[2]} for target in target_list_]
    data = db_.bangumi.find_one({'status': 1})
    data['bangumi'] = bangumi
    db_.bangumi.replace_one(data)


if __name__ == '__main__':
    db = keientist_db_instance()
    target_list = fetch(db)
    print(target_list)
    target_list, target_url = search(target_list, 'https://acg.rip')
    print(target_list)
    print(target_url)
    download(target_url, 'E://download/source_utorrent/')
    save(db, target_list)
