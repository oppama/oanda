
# coding: utf-8

# In[5]:

import httplib
import urllib
import json
from  datetime import datetime
import requests
import json
import pandas as pd
import numpy as np


# In[6]:

def get_Price(dom,token,pare):
    url = "https://" + dom + "/v1/prices"
    s = requests.Session()
    headers = {'Authorization' : 'Bearer ' + token,
                      }
    params = {'instruments' : pare}
    req = requests.Request("GET" , url , headers = headers, params = params)
    pre = req.prepare()
    resp = s.send(pre, stream = True, verify = True)
    ret = round((resp.json()['prices'][0]['ask']+resp.json()['prices'][0]['bid'])/2,3)
    s.close()
    
    return ret


# In[34]:

#時間取得
def makeData(dom,token):
    day = int(datetime.now().strftime("%Y%m%d"))
    time = int(datetime.now().strftime("%H%M")+"00")

    #スプレッド以上の変動があったデータ
    chartData = pd.read_csv('csv/5minChart.csv')
    predData = pd.read_csv('csv/predData.csv')

    cnrow = chartData.shape[0]
    cncol = chartData.shape[1]

    pnrow = predData.shape[0]
    pncol = predData.shape[1]

    chartData.ix[cnrow,0] = day
    chartData.ix[cnrow,1] = time

    predData.ix[pnrow,0] = day
    predData.ix[pnrow,1] = time

    #チャートデータ 
    chartData.ix[cnrow,2] = get_Price(dom,token,"USD_JPY")


    #直近のデータが下がっていたかどうか
    if chartData.ix[cnrow,2] >= chartData.ix[cnrow-1,2]:
            predData.ix[pnrow-1,2] = 1
    else:
        predData.ix[pnrow-1,2] = 0

    
    #time1にいれる
    predData.ix[pnrow,3] = chartData.ix[cnrow,2] - chartData.ix[cnrow-1,2]
    
    #予測データ計算せずに出来るデータの代入
    for i in range(4,15,1):
        predData.ix[pnrow,i] =  predData.ix[pnrow-1,i-1]
    
    #移動平均のデータ作成
    def makeAvg(span,old):
        ans = chartData.ix[cnrow-span+1-old:cnrow,2].mean()
        return(ans)

    avg_5 = makeAvg(5,0)
    avg_12 = makeAvg(12,0) 
    avg_24 = makeAvg(24,0)
    old_avg_5 = makeAvg(5,1)
    old_avg_12 = makeAvg(12,1)
    old_avg_24 = makeAvg(24,1)


    #over_avg_5
    predData.ix[pnrow,15] = chartData.ix[cnrow,2] - avg_5
    #over_avg_12
    predData.ix[pnrow,16] = chartData.ix[cnrow,2] - avg_12
    #over_avg_24
    predData.ix[pnrow,17] = chartData.ix[cnrow,2] - avg_24

    #over_cross_avg_5
    if chartData.ix[cnrow,2] > avg_5 and chartData.ix[cnrow-1,2] <= old_avg_5:
        predData.ix[pnrow,18] = 1
    else:
        predData.ix[pnrow,18] = 0
    #over_cross_avg_12
    if chartData.ix[cnrow,2] > avg_12 and chartData.ix[cnrow-1,2] <= old_avg_12:
        predData.ix[pnrow,19] = 1
    else:
        predData.ix[pnrow,19] = 0

    #over_cross_avg_24
    if chartData.ix[cnrow,2] > avg_24 and chartData.ix[cnrow-1,2] <= old_avg_24:
        predData.ix[pnrow,20] = 1
    else:
        predData.ix[pnrow,20] = 0
    
    #under_cross_avg_5
    if chartData.ix[cnrow,2] < avg_5 and chartData.ix[cnrow-1,2] >= old_avg_5:
        predData.ix[pnrow,21] = 1
    else:
        predData.ix[pnrow,21] = 0


    #under_cross_avg_5
    if chartData.ix[cnrow,2] < avg_12 and chartData.ix[cnrow-1,2] >= old_avg_12:
        predData.ix[pnrow,22] = 1
    else:
        predData.ix[pnrow,22] = 0

    #under_cross_avg_24
    if chartData.ix[cnrow,2] < avg_24 and chartData.ix[cnrow-1,2] >= old_avg_24:
        predData.ix[pnrow,23] = 1
    else:
        predData.ix[pnrow,23] = 0 
        
    #trend_avg_5,12,24
    predData.ix[pnrow,24] = avg_5 - makeAvg(5,5)
    predData.ix[pnrow,25] = avg_12 - makeAvg(12,5)
    predData.ix[pnrow,26] = avg_24  - makeAvg(24,5)
    
    #trend_5_over_12	trend_5_over_24	trend_12_over_24
    predData.ix[pnrow,27] = avg_5 - avg_12
    predData.ix[pnrow,28] = avg_5  - avg_24
    predData.ix[pnrow,29] = avg_12  - avg_24
    
    
    #trend_5_over_cross_12	trend_5_over_cross_24	trend_12_over_cross_24
    if avg_5  > avg_12  and old_avg_5 < old_avg_12:
        predData.ix[pnrow,30] = 1
    else:
        predData.ix[pnrow,30] = 0

    if avg_5  > avg_24  and old_avg_5 < old_avg_24:
        predData.ix[pnrow,31] = 1
    else:
        predData.ix[pnrow,31] = 0

    if avg_12  > avg_24  and old_avg_12 < old_avg_24:
        predData.ix[pnrow,32] = 1
    else:
        predData.ix[pnrow,32] = 0

    
    #trend_5_under_cross_12	trend_5_under_cross_24	trend_12_under_cross_24
    if avg_5 < avg_12  and old_avg_5 > old_avg_12:
        predData.ix[pnrow,33] = 1
    else:
        predData.ix[pnrow,33] = 0

    if avg_5 < avg_24  and old_avg_5 > old_avg_24:
        predData.ix[pnrow,34] = 1
    else:
        predData.ix[pnrow,34] = 0

    if avg_12 < avg_24  and old_avg_12 > old_avg_24:
        predData.ix[pnrow,35] = 1
    else:
        predData.ix[pnrow,35] = 0
    #macd
    
#一日目の計算方法は、単純移動平均と同じで、対象期間における終値の平均
#二日目以降を「前日の指数平滑平均+ｋ×(当日終値-前日の指数平滑平均)」
    
#csv書き出し
    chartData.to_csv('csv/5minChart.csv',index=False)
    predData.to_csv('csv/predData.csv',index=False)

