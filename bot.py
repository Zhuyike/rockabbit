# -*- coding: utf-8 -*-
import nonebot_local
import config


if __name__ == '__main__':
    nonebot_local.init(config)
    # nonebot.load_builtin_plugins()
    nonebot_local.load_plugins('bili/plugins', 'bili.plugins')
    nonebot_local.run()
