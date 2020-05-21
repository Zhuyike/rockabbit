#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import time
import json
import smtplib
import requests
import configparser
from email.mime.text import MIMEText


conf = configparser.ConfigParser()
conf.read('../server.conf')


class Tail(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.callback = self._callback
        self._file = None
        self.file_length = None

    def follow(self, n=10):
        with open(self.file_name, 'rb') as f:
            self._file = f
            self._file.seek(0, 2)
            self.file_length = self._file.tell()
            self.showLastLine(n)
            while True:
                line = self._file.readline()
                while line:
                    self.callback(line)
                    line = self._file.readline()
                time.sleep(1)

    def showLastLine(self, n):
        len_line = 100
        read_len = len_line * n
        while True:
            if read_len > self.file_length:
                self._file.seek(0)
                last_lines = self._file.read().split('\n')[-n:]
                break
            self._file.seek(-read_len, 2)
            last_words = self._file.read(read_len)
            count = last_words.count('\n')
            if count >= n:
                last_lines = last_words.split('\n')[-n:]
                break
            len_per_line = read_len if count == 0 else read_len/count
            read_len = len_per_line * n
        for line in last_lines:
            self.callback(line+'\n')

    def _callback(self, line):
        try:
            data = json.loads(line)
        except ValueError:
            return 0
        log = data['log']
        sys.stdout.write(log)
        if ' nonebot] ERROR: ' in log:
            ctx = log
            while True:
                line = self._file.readline()
                if line:
                    data = json.loads(line)
                    log = data['log']
                    sys.stdout.write(log)
                    ctx += log
                else:
                    break
            Mail().mail(ctx)
            requests.get('127.0.0.1:9999/report?ctx={}'.format(ctx))
        return 0


class Mail(object):
    def __init__(self):
        self.msg_from = conf.get("mail", "mail")
        self.passwd = conf.get("mail", "passwd")
        self.msg_to = conf.get("mail", "mail")
        self.subject = "qq-bot错误告警"

    def mail(self, content):
        msg = MIMEText(content)
        msg['Subject'] = self.subject
        msg['From'] = self.msg_from
        msg['To'] = self.msg_to
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        try:
            s.login(self.msg_from, self.passwd)
            s.sendmail(self.msg_from, self.msg_to, msg.as_string())
            print("发送成功")
        except smtplib.SMTPException as e:
            print(e)
            print("发送失败")
        finally:
            s.quit()


if __name__ == '__main__':
    filename = sys.argv[1]
    py_tail = Tail(filename)
    py_tail.follow(20)
