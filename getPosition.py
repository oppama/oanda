
# coding: utf-8

# In[11]:

import httplib
import urllib
import json
import datetime
import requests
import json
import pandas as pd



# In[12]:

def get_Position(dom,token,acc):
    url = "https://" + dom + "/v1/accounts/" + acc + "/positions/USD_JPY"
    s = requests.Session()
    hdrs = {"Authorization" : "Bearer " + token}
    req = requests.Request("GET" , url , headers = hdrs)
    pre = req.prepare()
    resp = s.send(pre, stream = True, verify = True)
    s.close()

    if resp.json().keys()[0]==u'moreInfo':
        return None
    else:
        rtn = pd.DataFrame([[resp.json()['side']],
              [resp.json()['avgPrice'] ]] ).T  #とりあえず適当なデータを作ります
        rtn.columns = ["side","avg_price"]  #カラム名を付ける
        rtn.index   = [1]  #インデックス名を付ける
        return rtn


