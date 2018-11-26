# -*- coding: utf-8 -*-
# Time    : 2018/11/23 9:06
# Author  : XYZ
import requests
import json
from conf.settings import remote_url


def submit_to_service(data):

    res = requests.post(url=remote_url, data=data)
    obj = res.text
    print(res.status_code, obj)
