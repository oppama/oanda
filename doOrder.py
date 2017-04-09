
# coding: utf-8

# In[4]:



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





# In[9]:

def do_Order(dom,token,acc,pare,side,unit,stopLoss):
    url = "https://" + dom + "/v1/accounts/" + acc + "/orders"
    s = requests.Session()
    headers = {'Authorization' : 'Bearer ' + token
              }
    payload = {'instrument': pare,
               'side': side,
               'type': 'market',
               'units': str(unit),
#               'stopLoss': str(stopLoss)
               'trailingStop': str(stopLoss)               
              }
    
    req = requests.Request("POST" , url , headers = headers, data=payload)
    pre = req.prepare()
    resp = s.send(pre, stream = True, verify = True)
    s.close
    return(resp)

