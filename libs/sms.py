from common import config
import requests
from django.conf import settings


def send_verify_code(phone,code):
    if settings.DEBUG:
        print("send verify code:", phone ,code)
        return True

    params = config.YZX_SMS_PARAMS.copy()

    params["param"]=code
    params["mobile"]=phone

    res = requests.post(config.REST_URL, json=params)

    if res.status_code==200:
        ret= res.json()
        if ret.get("code") == '000000':
            return True

    return False

    # print(phone,code)

# !/usr/bin/python
# coding:utf-8

