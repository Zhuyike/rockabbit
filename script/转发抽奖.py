#!/usr/bin/python
# -*- coding: UTF-8 -*-
import random

user = list()
sum_ = 0
with open('data.txt', 'r') as f:
    for line in f.readlines():
        qq = line.split('QQ: ')[1].split(', 转发数: ')[0]
        count = int(line.split('QQ: ')[1].split(', 转发数: ')[1].strip())
        sum_ += count
        user.append((qq, count))
print(user)
print(sum_)
for i in range(5):
    target = random.randint(1, sum_)
    print('种子随机数为: {}'.format(target))
    flag = 0
    while True:
        if target > user[flag][1]:
            target -= user[flag][1]
        elif target <= user[flag][1]:
            print('中奖用户为: {}'.format(user[flag][0]))
            break
        flag += 1