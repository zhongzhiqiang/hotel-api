# coding:utf-8

import os
import importlib

config_file = os.getenv('HOTEL_API_SETTINGS')
if not config_file:
    config_file = 'main.config.local'
config_module = importlib.import_module(config_file)
