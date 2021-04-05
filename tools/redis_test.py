# -*- coding: utf-8 -*-
# @File : redis_test.py
# @Author :WeiSanJin
# @Time :2021/04/04 22:47
# @Site :https://github.com/WeiSanJin
import redis

r = redis.Redis(host="localhost", port=6379, charset="utf8", decode_responses=True)

r.set("mobile", "10086")
r.expire("mobile", 1)
import time
time.sleep(1)
print(r.get("mobile"))
