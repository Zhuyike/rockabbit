# -*- coding: utf-8 -*-
import nonebot
import config


if __name__ == '__main__':
    nonebot.init(config)
    # nonebot.load_builtin_plugins()
    nonebot.load_plugins('bili/plugins', 'bili.plugins')
    nonebot.run()
