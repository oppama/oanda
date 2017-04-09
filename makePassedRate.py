
# coding: utf-8

# In[44]:

from datetime import datetime
import total_prediction_normal as tpn
import pandas as pd
import numpy as np


if __name__ == '__main__':
    
    daytime = int(datetime.now().strftime("%Y%m%d"))
    timing = int(datetime.now().strftime("%H%M")+"00")

    predData = pd.read_csv('csv/predData.csv')
    acrData = pd.read_csv('csv/acrData.csv')
    
    
    tr_time = 0
    ch_time = 0
    acr_top = 0
    model_list1 = ['rf','svm','knn','logistic','percep']

    for tr in range(10000,60000,10000):
        for ch in range(10000,60000,10000):
            acr = 0
            for model in model_list1:
                acr = acr+tpn.passed_time_model_check_2(predData
                                                        ,daytime
                                                        ,timing
                                                        ,tr
                                                        ,ch
                                                        ,model
                                                        ,knl='rbf')
        if acr_top < acr:
                    acr_top = acr
                    tr_time = tr
                    ch_time = ch
        else:
            pass
    
    #スプレッド以上の変動があったデータ
    cnrow = acrData.shape[0]
    cncol = acrData.shape[1]
    acrData.ix[cnrow,0] = daytime
    acrData.ix[cnrow,1] = timing
    acrData.ix[cnrow,2] = tr_time
    acrData.ix[cnrow,3] = ch_time
    acrData.ix[cnrow,4] = acr_top/5

#csv書き出し
    acrData.to_csv('csv/acrData.csv',index=False)

