
# coding: utf-8

# In[2]:

from datetime import datetime
import closePosition as cP
import doOrder as dO
import getAccountFund as gA
import getPosition as gPo
import getPrice as gPr
import total_prediction as tp
import pandas as pd
import numpy as np
import total_prediction_normal as tpn

if __name__ == '__main__':
    
    accData = pd.read_csv('csv/accounts.csv')
    
    dom = accData.ix[0,0]
    token = accData.ix[0,1]
    acc = str(accData.ix[0,2])
    pare = 'USD_JPY'
    
    daytime = int(datetime.now().strftime("%Y%m%d"))
    timing = int(datetime.now().strftime("%H%M")+"00")
    
    gPr.makeData(dom,token)
    predData = pd.read_csv('csv/predData.csv')
    acrData = pd.read_csv('csv/acrData.csv')
    
    
    #直近の予測で、どの範囲の時間が良いかを探す
    cnrow = acrData.shape[0]
    cncol = acrData.shape[1]
    
    tr_time = acrData.ix[cnrow-1,2]
    ch_time = acrData.ix[cnrow-1,3]
    acr_top = acrData.ix[cnrow-1,4]

    if datetime.now().hour in range(9,14) or datetime.now().hour in range(18,24): 
        final_ans = tp.final_answer(predData
                                    ,daytime
                                    ,timing
                                    ,tr_time
                                    ,ch_time)
        if gPo.get_Position(dom,token,acc) is None:
            if final_ans == 'buy':
                if acr_top/5 >= 0.5:
                    dO.do_Order(dom
                                ,token
                                ,acc
                                ,pare
                                ,'buy'
                                ,int(round(gA.get_AccountFund(dom,token,acc)*24/gPr.get_Price(dom,token,"USD_JPY"),0))
#                                ,gPr.get_Price(dom,token,pare)+0.03
                                ,5
                               )
                else:
                    dO.do_Order(dom
                            ,token
                            ,acc
                            ,pare
                            ,'sell'
                            ,int(round(gA.get_AccountFund(dom,token,acc)*24/gPr.get_Price(dom,token,"USD_JPY"),0))
                            #,gPr.get_Price(dom,token,pare)-0.03
                            ,5
                            )
            else:
                if acr_top/5 >= 0.5:
                    dO.do_Order(dom
                            ,token
                            ,acc
                            ,pare
                            ,'sell'
                            ,int(round(gA.get_AccountFund(dom,token,acc)*24/gPr.get_Price(dom,token,"USD_JPY"),0))
                            #,gPr.get_Price(dom,token,pare)-0.03
                            ,5
                            )
                else:
                    dO.do_Order(dom
                            ,token
                            ,acc
                            ,pare
                            ,'buy'
                            ,int(round(gA.get_AccountFund(dom,token,acc)*24/gPr.get_Price(dom,token,"USD_JPY"),0))
#                                ,gPr.get_Price(dom,token,pare)+0.03
                            ,5
                            )
        else:
                pass
    else:
        cP.close_Position(dom,token,acc,pare)