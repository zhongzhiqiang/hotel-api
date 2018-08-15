# coding:utf-8
from __future__ import unicode_literals
import json
import logging

from rest_framework import status
import requests

key = '2877351a0f04840ab0fdde1b447c2d3d'
url = 'https://restapi.amap.com/v3/geocode/geo'
logger = logging.getLogger(__name__)


GAODE_ERROR_INFO = {
    "10001": "key不正确或过期",
    "10002": "没有权限使用相应的服务或者请求接口的路径拼写错误",
    "10003": "访问已超出日访问量",
    "10004": "单位时间内访问过于频繁",
    "10005": "IP白名单出错，发送请求的服务器IP不在IP白名单内",
    "10006": "绑定域名无效",
    "10007": "数字签名未通过验证",
    "10008": "MD5安全码未通过验证",
    "10009": "请求key与绑定平台不符",
    "10010": "IP访问超限",
    "10011": "服务不支持https请求",
    "10012": "权限不足，服务请求被拒绝",
    "10013": "Key被删除",
    "10014": "云图服务QPS超限",
    "10015": "受单机QPS限流限制",
    "10016": "服务器负载过高",
    "10017": "所请求的资源不可用",
    "10019": "使用的某个服务总QPS超限",
    "10020": "某个Key使用某个服务接口QPS超出限制",
    "10021": "来自于同一IP的访问，使用某个服务QPS超出限制",
    "10022": "某个Key，来自于同一IP的访问，使用某个服务QPS超出限制",
    "10023": "某个KeyQPS超出限制",
    "20000": "请求参数非法",
    "20001": "缺少必填参数",
    "20002": "请求协议非法",
    "20003": "其他未知错误",
    "20800": "规划点（包括起点、终点、途经点）不在中国陆地范围内",
    "20801": "划点（起点、终点、途经点）附近搜不到路",
    "20802": "路线计算失败，通常是由于道路连通关系导致",
    "20803": "起点终点距离过长"
}

# TODO 打印日记等


class GaoDeMap(object):
    def __init__(self):
        self.key = key
        self.url = url
        self.success_code = '1'
        self.error_code = '0'
        self.timeout = 3

    def request_data(self, data):
        resp = requests.get(self.url, params=data, timeout=self.timeout)
        return resp

    def get_lat_longitude(self, address):
        data = {
            "key": self.key,
            "address": address,
        }
        ret = self.request_data(data)
        import ipdb
        ipdb.set_trace()
        if ret.status_code == status.HTTP_200_OK:
            try:
                content = json.loads(ret.content)
            except (ValueError, TypeError):
                ret = {
                    "status": "EEEEE",
                    "message": "返回参数错误"
                }
            else:
                code = content['status']
                if code == self.success_code:
                    geocodes = content['geocodes'][0]
                    lat_long = geocodes['location'].split(",")
                    latitude = lat_long[0]
                    longitude = lat_long[1]
                    ret = {
                        "status": "00000",
                        "data": {
                            "province": geocodes['province'],
                            "city": geocodes['city'],
                            "district": geocodes['district'],
                            "level": geocodes['level'],
                            "latitude": latitude,
                            'longitude': longitude,
                        }
                    }

                elif code == self.error_code:
                    ret = {
                        "status": "EEEEE",
                        "message": "请求错误"
                    }
        else:
            ret = {
                "status": "EEEEE",
                "message": "请求错误"
            }
        return ret

