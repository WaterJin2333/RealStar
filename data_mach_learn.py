from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,roc_curve, auc,precision_score,recall_score,f1_score,classification_report,confusion_matrix
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import cross_val_score
import numpy as np


df_false=pd.read_excel('second_corpse_fans_fin_data8.xlsx')
df_true=pd.read_excel('true_fans_fin_data8.xlsx')


df_false['original_page_num']=df_false['original_page_num'].astype('int')
df_false['weibo_num']=df_false['weibo_num'].astype('int')
df_false['original_ratio']=df_false['original_page_num']*10/df_false['weibo_num']
df_true['original_page_num']=df_true['original_page_num'].astype('int')
df_true['weibo_num']=df_true['weibo_num'].astype('int')
df_true['original_ratio']=df_true['original_page_num']*10/df_true['weibo_num']
df_false['original_ratio'][df_false['original_ratio']>1]=1
df_true['original_ratio'][df_true['original_ratio']>1]=1

df_false=df_false.drop(columns=['original_page_num','mean_comment','mean_like','mean_tran','mean_tran_comment','mean_tran_like','mean_tran_tran','original_ratio'])
df_true=df_true.drop(columns=['original_page_num','mean_comment','mean_like','mean_tran','mean_tran_comment','mean_tran_like','mean_tran_tran','original_ratio'])
feature_name=df_false.columns.values.tolist()
df_false[feature_name] = df_false[feature_name].apply(pd.to_numeric)
df_true[feature_name] = df_true[feature_name].apply(pd.to_numeric)
df_false=df_false.fillna(method='ffill')
df_true=df_true.fillna(method='ffill')

list_false=df_false.values.tolist()
list_true=df_true.values.tolist()
tag=[]
for i in range(len(list_false)):
    tag.append(1)
for i in range(len(list_true)):
    tag.append(0)
train=list_false+list_true



x_train, x_test, y_train, y_test = train_test_split(train, tag, test_size=0.33, random_state=42)

#RandomForest
#'''
rnd_clf = RandomForestClassifier(n_estimators=50, max_leaf_nodes=15, n_jobs=2)
rnd_clf.fit(x_train, y_train)
y_predict_rf = rnd_clf.predict(x_test)
y_predict_prob=rnd_clf.predict_proba(x_test)
print('accuracy_score:%f'%accuracy_score(y_test, y_predict_rf))
print('precision_score:%f'%precision_score(y_test, y_predict_rf))
print('recall_score:%f'%recall_score(y_test, y_predict_rf))
print('f_score:%f'%f1_score(y_test, y_predict_rf))
print(classification_report(y_test,y_predict_rf,target_names=['true','false']))
print(confusion_matrix(y_test,y_predict_rf))
for name, score in zip(feature_name, rnd_clf.feature_importances_):
    print(name, score)

y_score=[]
for prob in y_predict_prob:
    y_score.append(prob[1])

fpr, tpr, thresholds  =  roc_curve(y_test, y_score)
roc_auc =auc(fpr, tpr)


plt.figure()
lw = 2
plt.figure(figsize=(10,10))
plt.plot(fpr, tpr, color='darkorange',
         lw=lw, label='ROC curve (area = %0.2f)' % roc_auc) ###假正率为横坐标，真正率为纵坐标做曲线
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic')
plt.legend(loc="lower right")
plt.show()
#'''

#adaboost
'''
ada_clf = AdaBoostClassifier(n_estimators=50)    # 指定10个弱分类器
ada_clf.fit(x_train, y_train)
y_predict_rf = ada_clf.predict(x_test)
y_predict_prob=ada_clf.predict_proba(x_test)

b=ada_clf.predict(train)
print(type(b))
temp_file=open(r'C:\\Users\\A\\Desktop\\b.txt','w')
temp_file.write(str(list(b)))

print('accuracy_score:%f'%accuracy_score(y_test, y_predict_rf))
print('precision_score:%f'%precision_score(y_test, y_predict_rf))
print('recall_score:%f'%recall_score(y_test, y_predict_rf))
print('f_score:%f'%f1_score(y_test, y_predict_rf))
print(classification_report(y_test,y_predict_rf,target_names=['true','false']))
print(confusion_matrix(y_test,y_predict_rf))

for name, score in zip(feature_name, ada_clf.feature_importances_):
    print(name, score)

y_score=[]
for prob in y_predict_prob:
    y_score.append(prob[1])

fpr, tpr, thresholds  =  roc_curve(y_test, y_score)
roc_auc =auc(fpr, tpr)
print(roc_auc)
plt.figure()
lw = 2
plt.figure(figsize=(10,10))
plt.plot(fpr, tpr, color='darkorange',
         lw=lw, label='ROC curve (area = %0.2f)' % roc_auc) ###假正率为横坐标，真正率为纵坐标做曲线
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic')
plt.legend(loc="lower right")
plt.show()
'''
