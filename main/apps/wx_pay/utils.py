# coding:utf-8
# Time    : 2018/9/26 下午5:18
# Author  : Zhongzq
# Site    : 
# File    : utils.py
# Software: PyCharm
from __future__ import unicode_literals
import json
import time
import random
import hashlib
import string
from urllib import quote

from weixin.pay import WXAppPay
import xml.etree.ElementTree as ET

from main.common.wx_config import WXConfig


def unifiedorder(out_trade_no, total_fee, openid, detail):
    total_fee = int(float(total_fee) * 100)
    kwargs = {
        "body": '曼嘉酒店-商场',
        "out_trade_no": out_trade_no,
        "total_fee": total_fee,
        "openid": openid,
        "detail": detail,

    }
    wx_pay = WXAppPay(WXConfig.APP_ID, WXConfig.MCH_ID, partner_key=WXConfig.KEY)
    result = wx_pay.unifiedorder(**kwargs)
    return result


class WeixinHelper(object):
    @classmethod
    def checkSignature(cls, signature, timestamp, nonce):
        """微信对接签名校验"""
        tmp = [WXConfig.TOKEN, timestamp, nonce]
        tmp.sort()
        code = hashlib.sha1("".join(tmp)).hexdigest()
        return code == signature

    @classmethod
    def nonceStr(cls, length):
        """随机数"""
        return ''.join(
            random.choice(string.ascii_letters + string.digits)
            for _ in range(length))

    @classmethod
    def xmlToArray(cls, xml):
        """将xml转为array"""
        return dict((child.tag, child.text) for child in ET.fromstring(xml))


class CommonUtilPub(object):
    """所有接口的基类"""

    @staticmethod
    def trim_string(value):
        if value is not None and len(value) == 0:
            value = None
        return value

    @staticmethod
    def create_noncestr(length=32):
        """产生随机字符串，不长于32位"""
        chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        strs = []
        for x in range(length):
            strs.append(chars[random.randrange(0, len(chars))])
        return "".join(strs)

    @staticmethod
    def format_biz_query_para_map(para_map, url_encode):
        """格式化参数，签名过程需要使用"""
        slist = sorted(para_map)
        buff = []
        for k in slist:
            v = quote(para_map[k]) if url_encode else para_map[k]
            buff.append("{0}={1}".format(k, v))
        import logging
        logger = logging.getLogger(__name__)
        logger.info("buff string ={}".format(buff))
        return "&".join(buff)

    def get_sign(self, obj):
        """生成签名"""
        # 签名步骤一：按字典序排序参数,formatBizQueryParaMap已做
        String = self.format_biz_query_para_map(obj, False)
        # 签名步骤二：在string后加入KEY
        String = "{0}&key={1}".format(String, WXConfig.KEY)
        # 签名步骤三：MD5加密
        String = hashlib.md5(String).hexdigest()
        # 签名步骤四：所有字符转为大写
        result_ = String.upper()
        return result_

    def array_to_xml(self, arr):
        """array转xml"""
        xml = ["<xml>"]
        for k, v in arr.iteritems():
            if v.isdigit():
                xml.append("<{0}>{1}</{0}>".format(k, v))
            else:
                xml.append("<{0}><![CDATA[{1}]]></{0}>".format(k, v))
        xml.append("</xml>")
        return "".join(xml)

    @staticmethod
    def xml_to_array(xml):
        """将xml转为array"""
        return WeixinHelper.xmlToArray(xml)


class WxpayServerPub(CommonUtilPub):
    """响应型接口基类"""
    SUCCESS, FAIL = "SUCCESS", "FAIL"

    def __init__(self):
        self.data = {}  # 接收到的数据，类型为关联数组
        self.returnParameters = {}  # 返回参数，类型为关联数组

    def save_data(self, xml):
        """将微信的请求xml转换成关联数组，以方便数据处理"""
        self.data = self.xml_to_array(xml)

    def checkSign(self):
        """校验签名"""
        tmpData = dict(self.data)  # make a copy to save sign
        del tmpData['sign']
        sign = self.get_sign(tmpData)  # 本地签名
        if self.data['sign'] == sign:
            return True
        return False

    def getData(self):
        """获取微信的请求数据"""
        return self.data

    def setReturnParameter(self, parameter, parameterValue):
        """设置返回微信的xml数据"""
        self.returnParameters[self.trim_string(parameter)] = self.trim_string(
            parameterValue)

    def create_xml(self):
        """生成接口参数xml"""
        return self.array_to_xml(self.returnParameters)

    def return_xml(self):
        """将xml数据返回微信"""
        return_xml = self.create_xml()
        return return_xml
