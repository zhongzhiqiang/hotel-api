# coding:utf-8
# Time    : 2018/10/31 下午9:59
# Author  : Zhongzq
# Site    : 
# File    : decrypt.py
# Software: PyCharm
from __future__ import unicode_literals
import base64, hashlib

from Crypto.Cipher import AES


class ASECipher(object):

    def __init__(self, key):
        self.key = hashlib.md5(key.encode("utf-8")).hexdigest()

        self.BLOCK_SIZE = 32
        self.pad = lambda s: s + (self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE) * chr(self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE)
        self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return self.unpad(cipher.decrypt(enc)).decode("utf8")
