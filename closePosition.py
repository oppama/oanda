
# coding: utf-8

# In[9]:



# In[135]:
import sys
import httplib
import urllib
import json
import datetime
import requests
import json
import pandas as pd
import numpy as np


# In[11]:

def close_Position(dom,token,acc,pare):
    url = "https://" + dom + "/v1/accounts/" + acc + "/positions/" + pare
    s = requests.Session()
    headers = {'Authorization' : 'Bearer ' + token
              }    
    req = requests.Request("DELETE" , url , headers = headers)
    pre = req.prepare()
    resp = s.send(pre, stream = True, verify = True)
    s.close
    return(resp)

