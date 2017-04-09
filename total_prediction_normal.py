
# coding: utf-8

# # **為替予測 まとめ編**　　
# 
# 
# ***

# 予測に使うデータの読み込み

# In[168]:

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import Perceptron
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn import tree


# 各モデルの関数を定義

# In[169]:

def pred_model(data,date,time,tr_span,model,knl='rbf'):
    #予測する時間のレコードを抽出
    pre_data = data[data['daytime']==date]
    pre_data = pre_data[pre_data['time']==time]
    pre_data = pre_data.ix[:,3:]
    
    #学習データの抽出
    tr_data = data.dropna()
    tr_data = tr_data[tr_data['daytime']==date]
    tr_data = tr_data[tr_data['time']<time]
    tr_data = tr_data[tr_data['time']>time-tr_span]
    tr_data_label = tr_data.ix[:,2]
    tr_data = tr_data.ix[:,3:]

    #各モデルの実行
    if model=='rf':   
        model = RandomForestClassifier(class_weight="balanced")
#        model = tree.DecisionTreeClassifier(class_weight="balanced")

        model.fit( tr_data,tr_data_label )
        pred = model.predict(pre_data)
    
    if model=='svm':# linear,polynomial,rbf,sigmoidの4種類がある
        model = SVC(class_weight="balanced",kernel='rbf')
        model.fit( tr_data,tr_data_label )
        pred = model.predict(pre_data)
    
    if model=='knn':  
        model = KNeighborsClassifier(n_neighbors=3)
        model.fit( tr_data,tr_data_label )
        pred = model.predict(pre_data)


    if model=='logistic':
        model = LogisticRegression()
        model.fit( tr_data,tr_data_label )
        pred = model.predict(pre_data)

    if model=='percep':        
        model = Perceptron(n_iter=40, eta0=0.2)
        model.fit( tr_data,tr_data_label )
        pred = model.predict(pre_data)
    
    #結果
    return int(pred)


# In[170]:

def passed_time_model_check(data,date,time,tr_span,ch_span,model,knl='rbf'):
    #答え合わせをする際のテーブル準備
    answer_data = data[data['daytime']==date]
    answer_data = answer_data[answer_data['time']<time]
    answer_data = answer_data[answer_data['time']>time-ch_span]
    answer_data = answer_data.dropna()

    #インデックスの振り直し
    answer_data = answer_data.ix[:,1:3].reset_index(drop=True)

    passed_pred = np.array([])
    for tm in answer_data['time']:
        passed_pred=np.r_[passed_pred,pred_model(data,date,tm,tr_span,model)]

    #予測データと突き合わせ様のカラム追加
    answer_data['pre'] = passed_pred
            
    #正誤表の作成
    cnf_mat = confusion_matrix(answer_data.ix[:,1].tolist(),answer_data.ix[:,2].tolist())
            
    #カラム名作成
    name1=model+'_0_change_flg'
    name2=model+'_1_change_flg'
    name3=model+'_0_accuracy'
    name4=model+'_1_accuracy'
    
    #回答用データの作成
    r_data = pd.DataFrame(
            {name1:[],
             name2:[],
             name3:[],
             name4:[],
            })
    
    
    #1の時の、過去分の正解率による反転フラグと、正解率
    if cnf_mat[0][0]>cnf_mat[1][0] and cnf_mat[0][0]+cnf_mat[1][0]>0 :
        r_data.ix[0,name1] = 0
        r_data.ix[0,name3] = float(cnf_mat[0][0])/(cnf_mat[0][0]+cnf_mat[1][0])
    elif cnf_mat[0][0]+cnf_mat[1][0]>0 :
        r_data.ix[0,name1] = 1
        r_data.ix[0,name3] = float(cnf_mat[1][0])/(cnf_mat[0][0]+cnf_mat[1][0])
    else:
        pass
    #2の時の、過去分の正解率による反転フラグと、正解率
    if cnf_mat[0][1]<cnf_mat[1][1] and cnf_mat[0][1]+cnf_mat[1][1]>0:
        r_data.ix[0,name2] = 0
        r_data.ix[0,name4] = float(cnf_mat[1][1])/(cnf_mat[0][1]+cnf_mat[1][1])
    elif cnf_mat[0][1]+cnf_mat[1][1]>0:
        r_data.ix[0,name2] = 1
        r_data.ix[0,name4] = float(cnf_mat[0][1])/(cnf_mat[0][1]+cnf_mat[1][1])
    else:
        pass
    return(r_data)


# In[171]:

def final_normal_answer(data,date,time,tr_span,ch_span):
    model_list = ['rf','svm','knn','logistic','percep']
    passed_model_result = pd.DataFrame({'base': [1]})
    pred_model_result = pd.DataFrame(
        {'rf': [0],
         'svm': [0],
         'knn': [0],
         'logistic': [0],
         'percep': [0]
        })

    for m in model_list:
        passed_model_result = pd.concat([passed_model_result, passed_time_model_check(data,date,time,tr_span,ch_span,m,knl='rbf')], axis=1)
        pred_model_result[m] = pred_model(data,date,time,tr_span,m,knl='rbf')



    #最終的な答えのデータフレーム
    pred_answer = pd.DataFrame(
    {'rf':  [0.0,0.0],
     'svm':  [0.0,0.0],
     'knn':  [0.0,0.0],
     'logistic':  [0.0,0.0],
     'percep': [0.0,0.0]
    })

    #カラムにアクセスするための名前作り
    rf_flg = 'rf_'+ str(pred_model_result ['rf'][0]) +'_change_flg'
    rf_ac = 'rf_'+ str(pred_model_result ['rf'][0]) +'_accuracy'
    svm_flg = 'svm_'+ str(pred_model_result ['svm'][0]) +'_change_flg'
    svm_ac = 'svm_'+ str(pred_model_result ['svm'][0]) +'_accuracy'
    knn_flg = 'knn_'+ str(pred_model_result ['knn'][0]) +'_change_flg'
    knn_ac = 'knn_'+ str(pred_model_result ['knn'][0]) +'_accuracy'
    logistic_flg = 'logistic_'+ str(pred_model_result ['logistic'][0]) +'_change_flg'
    logistic_ac = 'logistic_'+ str(pred_model_result ['logistic'][0]) +'_accuracy'
    percep_flg = 'percep_'+ str(pred_model_result ['percep'][0]) +'_change_flg'
    percep_ac = 'percep_'+ str(pred_model_result ['percep'][0]) +'_accuracy'



    #反転が必要かどうかを判定し、必要ならば反転する
    #正答率は、直近3時間分のものを使用する
    pred_answer['rf'][0] = pred_model_result['rf'][0]
    pred_answer['rf'][1] = passed_model_result[rf_ac]
    
    pred_answer['svm'][0] = pred_model_result['svm'][0]
    pred_answer['svm'][1] = passed_model_result[svm_ac]
    
    pred_answer['knn'][0] = pred_model_result['knn'][0]
    pred_answer['knn'][1] = passed_model_result[knn_ac]
    
    pred_answer['logistic'][0] = pred_model_result['logistic'][0]
    pred_answer['logistic'][1] = passed_model_result[logistic_ac]
    
    pred_answer['percep'][0] = pred_model_result['percep'][0]
    pred_answer['percep'][1] = passed_model_result[percep_ac]


        #合計をとって高い方を選ぶ
    bear=0
    bull=0

    for i in range(pred_answer.shape[1]):
        if pred_answer.ix[0,i]==1:
            bull = bull+pred_answer.ix[1, i]
        else:
            bear = bear+pred_answer.ix[1, i]


    if bull >= bear:
        answer = 'buy'
    else:
        answer = 'sell'

    return(answer)


# In[172]:

def passed_time_model_check_2(data,date,time,tr_span,ch_span,model,knl='rbf'):
    #答え合わせをする際のテーブル準備
    answer_data = data[data['daytime']==date]
    answer_data = answer_data[answer_data['time']<time]
    answer_data = answer_data[answer_data['time']>time-ch_span]
    answer_data = answer_data.dropna()

    #インデックスの振り直し
    answer_data = answer_data.ix[:,1:3].reset_index(drop=True)

    passed_pred = np.array([])
    for tm in answer_data['time']:
        passed_pred=np.r_[passed_pred,pred_model(data,date,tm,tr_span,model)]

    #予測データと突き合わせ様のカラム追加
    answer_data['pre'] = passed_pred

    #正誤表の作成
    cnf_mat = confusion_matrix(answer_data.ix[:,1].tolist(),answer_data.ix[:,2].tolist())

    ans = float(max(cnf_mat[0][0],cnf_mat[1][0])+max(cnf_mat[0][1],cnf_mat[1][1]))/(cnf_mat[0][0]+cnf_mat[1][0]+cnf_mat[0][1]+cnf_mat[1][1])
#    ans = float(cnf_mat[0][0]+cnf_mat[1][1])/(cnf_mat[0][0]+cnf_mat[1][0]+cnf_mat[0][1]+cnf_mat[1][1])
    
    return(ans)
