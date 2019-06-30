import pandas as pd
from collections import Counter
import numpy as np
import cv2
from skimage import io

class analyse():
    def __init__(self,file):
        self.file=file
    def data_analyse(self):
        self.id_list=[]
        self.like_num_list=[]
        self.tran_num_list = []
        self.comment_num_list = []
        self.tran_like_num_list = []
        self.tran_tran_num_list = []
        self.tran_comment_num_list = []
        self.mean_like_list=[]
        self.mean_tran_list = []
        self.mean_comment_list = []
        self.mean_tran_like_list = []
        self.mean_tran_tran_list = []
        self.mean_tran_comment_list = []
        self.pop_index=[]
        self.tran_pop_index=[]
        self.no_like_and_no_comment_ratio=[]
        self.time_list=[]
        self.midnight_ratio=[]
        self.double_in_one_min_ratio=[]
        self.phone_ratio=[]
        self.dakuohao_tario=[]
        self.url_ratio=[]
        self.origonal_page_list=[]
        self.weibo_interval=[]

        df=pd.read_excel(self.file)
        df.dropna()
        self.num=df.shape[0]
        for i in df.index:#id
            self.id_list.append(df.loc[i]['id'])
        for i in df.index:
            self.origonal_page_list.append(eval(df.loc[i]['weibo_origional'])[0])
        for i in df.index:#点赞量数字
            temp_list=df.loc[i]['weibo_like']
            like_temp_list=[]
            temp_list=eval(temp_list)
            for j in temp_list:
                like_temp_list.append(int(j[2:-1]))
            self.like_num_list.append(like_temp_list)
        for i in df.index:#转发量数字
            temp_list=df.loc[i]['weibo_tran']
            tran_temp_list=[]
            temp_list = eval(temp_list)
            for j in temp_list:
                tran_temp_list.append(int(j[3:-1]))
            self.tran_num_list.append(tran_temp_list)
        for i in df.index:#评论量数字
            temp_list=df.loc[i]['weibo_comment']
            comment_temp_list=[]
            temp_list = eval(temp_list)
            for j in temp_list:
                if j=='#名博评论[超话]#':
                    pass
                else:
                    comment_temp_list.append(int(j[3:-1]))
            self.comment_num_list.append(comment_temp_list)
        for i in df.index:#转发点赞量数字
            temp_list=df.loc[i]['weibo_tran_like']
            tran_like_temp_list=[]
            temp_list = eval(temp_list)
            for j in temp_list:
                tran_like_temp_list.append(int(j[2:-1]))
            self.tran_like_num_list.append(tran_like_temp_list)
        for i in df.index:#转发转发量数字
            temp_list=df.loc[i]['weibo_tran_tran']
            tran_tran_temp_list=[]
            temp_list = eval(temp_list)
            for j in temp_list:
                tran_tran_temp_list.append(int(j[5:-1]))
            self.tran_tran_num_list.append(tran_tran_temp_list)
        for i in df.index:#转发评论量数字
            temp_list=df.loc[i]['weibo_tran_comment']
            tran_comment_temp_list=[]
            temp_list = eval(temp_list)
            for j in temp_list:
                tran_comment_temp_list.append(int(j[5:-1]))
            self.tran_comment_num_list.append(tran_comment_temp_list)
        print(self.like_num_list)
        print(self.comment_num_list)
        print(self.tran_num_list)
        print(self.tran_like_num_list)
        print(self.tran_tran_num_list)
        print(self.tran_comment_num_list)

        for i in range(self.num):#微博人气指数
            pop_index_sum=0
            length=min([len(self.like_num_list[i]),len(self.tran_num_list[i]),len(self.comment_num_list[i])])
            if length!=0:
                for j in range(length):
                    temp=pow((self.like_num_list[i][j]+1)*(self.tran_num_list[i][j]+1)*(self.comment_num_list[i][j]+1),0.2)
                    pop_index_sum+=temp
                self.mean_like_list.append(np.mean(self.like_num_list[i]))
                self.mean_tran_list.append(np.mean(self.tran_num_list[i]))
                self.mean_comment_list.append(np.mean(self.comment_num_list[i]))
                self.pop_index.append(pop_index_sum/length)
            else:
                self.mean_like_list.append(0)
                self.mean_tran_list.append(0)
                self.mean_comment_list.append(0)
                self.pop_index.append(1)
        print(self.pop_index)
        for i in range(self.num):#转发微博人气指数
            tran_pop_index_sum=0
            length=min([len(self.tran_like_num_list[i]),len(self.tran_tran_num_list[i]),len(self.tran_comment_num_list[i])])
            if length!=0:
                for j in range(length):
                    temp=pow((self.tran_like_num_list[i][j]+1)*(self.tran_tran_num_list[i][j]+1)*(self.tran_comment_num_list[i][j]+1),0.2)
                    tran_pop_index_sum+=temp
                self.mean_tran_like_list.append(np.mean(self.tran_like_num_list[i]))
                self.mean_tran_tran_list.append(np.mean(self.tran_tran_num_list[i]))
                self.mean_tran_comment_list.append(np.mean(self.tran_comment_num_list[i]))
                self.tran_pop_index.append(tran_pop_index_sum/length)
            else:
                self.mean_tran_like_list.append(0)
                self.mean_tran_tran_list.append(0)
                self.mean_tran_comment_list.append(0)
                self.tran_pop_index.append(1)
        print(self.tran_pop_index)
        for i in range(self.num):#微博无评论无转发比例
            no_like_and_no_comment_sum=0
            length = len(self.like_num_list[i])
            if length!=0:
                for j in range(length):
                    if self.like_num_list[i][j]==0 and self.comment_num_list[i][j]==0:
                        no_like_and_no_comment_sum+=1
                self.no_like_and_no_comment_ratio.append(no_like_and_no_comment_sum/length)
            else:
                self.no_like_and_no_comment_ratio.append(0)
        print(self.no_like_and_no_comment_ratio)
        for i in df.index:
            temp_list=df.loc[i]['weibo_time']
            temp_list = eval(temp_list)
            time_temp_list=[]
            for j in temp_list:
                time_temp_list.append(j.split(' ')[1][0:5])

            self.time_list.append(time_temp_list)
        for i in range(self.num):#夜间发博率和一分钟内多条发博率
            midnight_sum=0
            double_in_one_min_sum=0
            length=len(self.time_list[i])
            if length!=0:
                for j in range(length):
                    if self.time_list[i][j][0:2] in ['01','02','03','04','05']:
                        midnight_sum+=1
                self.midnight_ratio.append(midnight_sum/length)
                if len(list(set(self.time_list[i])))<length:
                    count_dic=Counter(self.time_list[i])
                    count=list(count_dic.values())
                    for k in count:
                        if k!=1:
                            double_in_one_min_sum+=k
                self.double_in_one_min_ratio.append(double_in_one_min_sum/length)
            else:
                self.midnight_ratio.append(0)
                self.double_in_one_min_ratio.append(0)
        for i in range(self.num):#发博间隔方差
            length=len(self.time_list[i])
            if length>1:
                temp_list=[]
                for j in self.time_list[i]:
                    temp_list.append(int(j.split(':')[0])*60+int(j.split(':')[1]))
                temp_list=sorted(temp_list)
                diff = [temp_list[i] - temp_list[i + 1] for i in range(len(temp_list) - 1)]
                self.weibo_interval.append(np.std(diff))
            else:
                self.weibo_interval.append(None)
        print('..........')
        print(self.weibo_interval)
        print('..........')
        print(self.midnight_ratio)
        print(self.double_in_one_min_ratio)
        for i in df.index:#手机发博率
            temp_list=df.loc[i]['weibo_resourse']
            temp_list=eval(temp_list)
            temp_list=list(filter(None,temp_list))
            length=len(temp_list)
            phone_ratio_sum=0
            if length!=0:
                phone_brand_list=['iphone','iPhone','ipad','iPad','vivo','VIVO','HUAWEI','huawei','小米','xiaomi','OPPO','oppo','Android','android'
                          'intl','荣耀','SUMSAM','三星','Werco','红米','华为','手机','魅族']
                for j in temp_list:
                    for k in phone_brand_list:
                        if k in j:
                            phone_ratio_sum+=1
                self.phone_ratio.append(phone_ratio_sum/length)
            else:
                self.phone_ratio.append(0)

        print(self.phone_ratio)
        for i in df.index:#博文中含大括号和url率
            temp1=df.loc[i]['dakuohao_count']
            temp1=int(temp1)
            length=len(eval(df.loc[i]['weibo_like']))
            self.dakuohao_tario.append(temp1/length)
            temp2=df.loc[i]['url_count']
            temp2=int(temp2)
            self.url_ratio.append(temp2/length)
        print(self.dakuohao_tario)
        print(self.url_ratio)
        return pd.DataFrame({'id':self.id_list,'mean_like':self.mean_like_list,'mean_tran':self.mean_tran_list,'mean_comment':self.mean_comment_list,
                             'mean_tran_like':self.mean_tran_like_list,'mean_tran_tran':self.mean_tran_tran_list,'mean_tran_comment':self.mean_tran_comment_list,
                             'pop_index':self.pop_index,'tran_pop_index':self.tran_pop_index,'no_like_and_no_comment_ratio':self.no_like_and_no_comment_ratio,
                            'midnight_ratio':self.midnight_ratio,'double_in_one_min_ratio':self.double_in_one_min_ratio,'phone_ratio':self.phone_ratio,
                            'dakuohao_ratio':self.dakuohao_tario,'url_ratio':self.url_ratio,'origional_page_num':self.origonal_page_list,'weibo_interval':self.weibo_interval})



def getImageVar(imgsrc):
    image = io.imread(imgsrc)
    image=cv2.resize(image,(800, 800))
    img2gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imageVar = cv2.Laplacian(img2gray, cv2.CV_64F).var()
    return imageVar

class base_analyse():
    def __init__(self,path):
        self.path=path

    def analyse(self):
        self.id_list=[]
        self.name_length_list=[]
        self.img_blur_list=[]
        self.weibo_num_list=[]
        self.hot_index_list=[]
        self.desc_bool_list=[]
        self.follow_list=[]
        self.fans_list=[]
        df=pd.read_excel(self.path)
        df.dropna()
        df.reset_index()
        for i in df.index:#用户名长度
            self.name_length_list.append(len(df.loc[i]['name']))
        print(self.name_length_list)
        for i in df.index:
            img_src_50=df.loc[i]['img']#头像模糊度
            img_src_1024=img_src_50.replace('.50/','.1024/')
            try:
                self.img_blur_list.append(getImageVar(img_src_1024))
            except BaseException:
                self.img_blur_list.append(None)
            self.id_list.append(df.loc[i]['id'])#id
            self.weibo_num_list.append(df.loc[i]['weibo_num'])#微博数
            self.hot_index_list.append(df.loc[i]['follow_num']/(df.loc[i]['follow_num']+(df.loc[i]['fans_num'])))#人气指数
            self.desc_bool_list.append(df.loc[i]['desc_bool'])#是否有描述
            self.follow_list.append(df.loc[i]['follow_num'])#关注数
            self.fans_list.append(df.loc[i]['fans_num'])#粉丝数
        return pd.DataFrame({'id':self.id_list,'name_length':self.name_length_list,'img_blur':self.img_blur_list,
                             'weibo_num':self.weibo_num_list,'hot_index':self.hot_index_list,'desc_bool':self.desc_bool_list,
                             'follow_num':self.follow_list,'fans_num':self.fans_list})


if __name__=='__main__':
    analyse_true=analyse('true_fans_base_weibo_info_more.xlsx')
    true_data_info=analyse_true.data_analyse()
    true_data_info.to_excel('true_fans_weibo_fin_data.xlsx')

    base_analyse_true=base_analyse('true_fans_base_info.xlsx')
    true_base_info=base_analyse_true.analyse()
    true_base_info.to_excel('true_fans_base_fin_data.xlsx')

    analyse_false = analyse('second_corpse_fans_base_weibo_info.xlsx')
    false_data_info = analyse_false.data_analyse()
    false_data_info.to_excel('second_corpse_fans_base_weibo_fin_data.xlsx')

    base_analyse_false = base_analyse('second_corpse_fans_base_info1-820.xlsx')
    false_base_info = base_analyse_false.analyse()
    false_base_info.to_excel('second_corpse_fans_base_fin_data.xlsx')

    true_data_info=pd.read_excel('true_fans_weibo_fin_data.xlsx')
    true_base_info=pd.read_excel('true_fans_base_fin_data.xlsx')
    false_data_info=pd.read_excel('second_corpse_fans_base_weibo_fin_data.xlsx')
    false_base_info=pd.read_excel('second_corpse_fans_base_fin_data.xlsx')
    true_fin=pd.merge(true_data_info,true_base_info)
    true_fin=true_fin.drop(columns=['id'])
    true_fin.to_excel('true_fans_fin_data.xlsx')
    false_fin=pd.merge(false_data_info,false_base_info)
    false_fin=false_fin.drop(columns=['id'])
    false_fin.to_excel('second_corpse_fans_fin_data.xlsx')


