# coding:utf-8
# Time    : 2018/9/4 下午10:10
# Author  : Zhongzq
# Site    : 
# File    : perms.py
# Software: PyCharm
from __future__ import unicode_literals


permission_list = [
    {
        "model": "banner",
        "perms": [
            {
                "name": "查看所有横幅",
                "codename": "search_banner"
            },
            {
                "name": "添加横幅",
                "codename": "add_banner"
            },
            {
                "name": "修改横幅内容",
                "codename": "update_banner"
            },
            {
                "name": "下架横幅",
                "codename": "delete_banner"
            }
        ]
    },
    {
        "model": "hotel",
        "perms": [
            {
                "name": "添加宾馆信息",
                "codename": "add_hotel"
            },
            {
                "name": "修改宾馆信息",
                "codename": "update_hotel",
            }
        ]
    }
]