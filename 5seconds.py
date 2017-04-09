
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


# In[ ]:

if __name__ == '__main__':
    accData = pd.read_csv('csv/accData.csv')
    
    dom = accData.ix[0,0]
    token = accData.ix[0,1]
    acc = accData.ix[0,2]
    pare = 'USD_JPY'

    

    if gPo.get_Position(dom,token,acc) is None:
        pass
    elif str(gPo.get_Position(dom,token,acc).iloc[0,0])=='buy' and gPr.get_Price(dom,token,pare) >= float(gPo.get_Position(dom,token,acc).iloc[0,1])+0.06:
        cP.close_Position(dom,token,acc,pare)
    elif str(gPo.get_Position(dom,token,acc).iloc[0,0])=='sell' and gPr.get_Price(dom,token,pare) <= float(gPo.get_Position(dom,token,acc).iloc[0,1])-0.06:
        cP.close_Position(dom,token,acc,pare)
    else:
        pass

