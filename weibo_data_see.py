import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import decomposition
pca = decomposition.PCA(n_components=2)
df_false=pd.read_excel('C:\\Users\\A\\Desktop\\second_corpse_fans_fin_data8.xlsx')
df_true=pd.read_excel('C:\\Users\\A\\Desktop\\true_fans_fin_data8.xlsx')
df_false['original_page_num']=df_false['original_page_num'].astype('int')
df_false['weibo_num']=df_false['weibo_num'].astype('int')
df_false['original_ratio']=df_false['original_page_num']*10/df_false['weibo_num']
df_true['original_page_num']=df_true['original_page_num'].astype('int')
df_true['weibo_num']=df_true['weibo_num'].astype('int')
df_true['original_ratio']=df_true['original_page_num']*10/df_true['weibo_num']
df_false['original_ratio'][df_false['original_ratio']>1]=1
df_true['original_ratio'][df_true['original_ratio']>1]=1

df_false=df_false.drop(columns=['original_page_num','mean_comment','mean_like','mean_tran','mean_tran_comment','mean_tran_like','mean_tran_tran'])
df_true=df_true.drop(columns=['original_page_num','mean_comment','mean_like','mean_tran','mean_tran_comment','mean_tran_like','mean_tran_tran'])
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
X = pca.fit_transform(train)
pos=pd.DataFrame()
pos['X'] =X[:, 0]
pos['Y'] =X[:, 1]
tag=pd.DataFrame({'class':tag})
pos['class']=tag['class']
random=[]
with open(r'C:\Users\A\Desktop\b.txt','r',encoding='utf-8') as random_open:
    line=random_open.readline()
    for i in line:
        if i=='0' or i =='1':
            random.append(i)
pos['predict']=random
print(pos)
ax = pos[(pos['class']==1)&(pos['predict']=='1')].plot.scatter( x='X', y='Y',s=5,color='blue', marker='*',label='true')
pos[(pos['class']==1)&(pos['predict']=='0')].plot.scatter( x='X', y='Y', s=10,color='green', label='Negative_false', ax=ax)
pos[(pos['class']==0)&(pos['predict']=='0')].plot.scatter( x='X', y='Y', s=5,color='blue',marker='*', ax=ax)
pos[(pos['class']==0)&(pos['predict']=='1')].plot.scatter( x='X', y='Y', s=10,color='red', label='Positive_false',ax=ax)
plt.show()
