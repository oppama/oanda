
# coding: utf-8

# In[29]:



# In[135]:
import sys
import httplib
import urllib
import json
import datetime
import requests
import json
import pandas
import pandas as pd
import numpy as np
import getPrice as gP


# In[30]:

def get_AccountFund(dom,token,acc):
    url = "https://" + dom + "/v1/accounts/" + acc
    s = requests.Session()
    headers = {'Authorization' : 'Bearer ' + token
                      }
    req = requests.Request("GET" , url , headers = headers)
    pre = req.prepare()
    resp = s.send(pre, stream = True, verify = True)
    s.close()
    return(resp.json()['balance'])
 


# In[31]:

def get_OrderNum(dom,token,acc):
    orderNum=round(get_AccountFund(dom,token,acc)*25/gP.get_Price(dom,token,"USD_JPY"),0)
    return(orderNum)

