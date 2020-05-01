from config import keientist_db_instance
import requests


class Main(object):
    def __init__(self, dbs):
        self.dbs = dbs

    def main(self):
        mongo_db = self.dbs['keientist']
        data = mongo_db.img_status.find()
        cal = dict()
        url = dict()
        for img_ in data:
            cal[img_['file']] = cal.get(img_['file'], 0) + 1
            url[img_['file']] = img_['url']
        img_list = [{'file': k, 'cal': v, 'url': url[k]} for k, v in cal.items()]
        img_list.sort(key=lambda x: x['cal'], reverse=True)
        with open('output.csv', 'w') as f:
            for img_ in img_list:
                f.write('{},{},{}\n'.format(img_['file'].split('.')[0], img_['cal'], '{}'.format(img_['url'])))
            if len(img_list) > 100:
                img_list = img_list[:100]
            print('开始下载')
            for index, img_ in enumerate(img_list):
                print(index)
                r = requests.get(img_['url'])
                houzui = ''
                if r.headers['Content-Type'] == 'image/gif':
                    houzui = '.gif'
                elif r.headers['Content-Type'] == 'application/x-jpg' or r.headers['Content-Type'] == 'image/jpeg':
                    houzui = '.jpg'
                elif r.headers['Content-Type'] == '	application/x-png' or r.headers['Content-Type'] == 'image/png':
                    houzui = '.png'
                elif r.headers['Content-Type'] == '	application/x-webp' or r.headers['Content-Type'] == 'image/webp':
                    houzui = '.webp'
                else:
                    print(r.headers['Content-Type'])
                with open("output/{}{}".format(img_['cal'], houzui), "wb") as code:
                    code.write(r.content)
                r.close()


if __name__ == '__main__':
    main = Main(keientist_db_instance())
    main.main()
