import requests
from bs4 import BeautifulSoup
import re
import time
import random
import pandas as pd

class My_fans():
    def __init__(self,cookie):
        self.cookie=cookie

    def get_fans_uid(self):
        session=requests.session()
        self.headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': self.cookie,
        'Host': 'weibo.cn',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'}
        self.res_my_fans=session.get('https://weibo.cn/6018012347/fans?page=2',headers=self.headers)
        self.res_my_fans.encoding = 'utf-8'
        self.soup_my_fans = BeautifulSoup(self.res_my_fans.text, 'html.parser')
        self.fans_list_length=self.soup_my_fans.find_all(attrs={'name':'mp'})
        print(self.soup_my_fans)
        self.fans_list_length=int(self.fans_list_length[0].attrs['value'])
        self.all_fans_uid=[]
        for i in range(self.fans_list_length):#所有粉丝页面爬取粉丝id
            temp_res=session.get('https://weibo.cn/6018012347/fans?page=%d'%i,headers=self.headers)
            temp_res.encoding='utf-8'
            temp_soup=BeautifulSoup(temp_res.text,'html.parser')
            uid=temp_soup.find_all(href=re.compile("/u/"))
            temp_uid_list = []
            for j in range(len(uid)):
                temp_uid_list.append(str(uid[j]).split('><'))
            uid_list = []
            for k in temp_uid_list:
                uid = re.findall(re.compile(r'[^\d]+(\d+)[^\d]+'), k[0])
                uid_list.append(uid[0])
            time.sleep(1)
            self.all_fans_uid+=list(set(uid_list))
        return self.all_fans_uid


class fans_info():
    def __init__(self,uidlist,cookie):
        self.cookie=cookie
        self.uidlist=uidlist
        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
            "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
            ]

    def get_fans_base_info(self):#粉丝基本信息
        self.user_agent=random.choice(self.user_agent_list)
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': self.cookie,
            'Host': 'weibo.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': self.user_agent}
        self.name_list=[]
        self.weibo_num_list=[]
        self.follow_num_list=[]
        self.fans_num_list=[]
        self.img_list=[]
        self.desc_bool_list=[]
        for uid in self.uidlist:
            session = requests.session()
            temp_res=session.get('https://weibo.cn/u/%s'%uid,headers=self.headers)
            temp_res.encoding = 'utf-8'
            temp_soup = BeautifulSoup(temp_res.text, 'html.parser')
            name=temp_soup.find_all(attrs={'class':'ctt'})
            name=str(name[0]).split('>')[1].split('<')[0].split('\xa0')[0]#用户名
            self.name_list.append(name)
            weibo_num=temp_soup.find_all(attrs={'class':'tc'})
            weibo_num=str(weibo_num[0]).split('[')[1].split(']')[0]#发博数
            self.weibo_num_list.append(weibo_num)
            follow_num=temp_soup.find_all(href='/%s/follow'%uid)
            follow_num=str(follow_num[0]).split('[')[1].split(']')[0]#关注数
            self.follow_num_list.append(follow_num)
            fans_num = temp_soup.find_all(href='/%s/fans' % uid)
            fans_num = str(fans_num[0]).split('[')[1].split(']')[0] # 粉丝数
            self.fans_num_list.append(fans_num)
            img = temp_soup.find_all(alt='头像')
            self.img_list.append(img[0].attrs['src'])
            desc_bool=temp_soup.find(style="word-break:break-all; width:50px;")#是否有描述
            if desc_bool.text:
                self.desc_bool_list.append('1')
            else:
                self.desc_bool_list.append('0')
        return  pd.DataFrame({'id':self.uidlist,'name':self.name_list,'weibo_num':self.weibo_num_list,'follow_num':self.follow_num_list,
                                  'fans_num':self.fans_num_list,'desc_bool':self.desc_bool_list,'img':self.img_list})


    def get_fans_weibo_base_info(self):
        self.all_dakuohao_count = []
        self.all_url_count = []
        self.all_weibo_like_list = []
        self.all_weibo_tran_list = []
        self.all_weibo_comment_list = []
        self.all_weibo_tran_like_list = []
        self.all_weibo_tran_tran_list = []
        self.all_weibo_tran_comment_list = []
        self.all_weibo_time_list = []
        self.all_weibo_resourse_list = []
        self.all_weibo_origional_list=[]
        self.count=0
        for uid in self.uidlist:
            self.user_agent = random.choice(self.user_agent_list)#随机useragent
            self.headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Cookie': self.cookie,
                'Host': 'weibo.cn',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': self.user_agent}
            dakuohao_count = 0
            url_count = 0
            weibo_like_list=[]
            weibo_tran_list=[]
            weibo_comment_list=[]
            weibo_tran_like_list=[]
            weibo_tran_tran_list = []
            weibo_tran_comment_list = []
            weibo_time_list=[]
            weibo_resourse_list=[]
            weibo_origional_list=[]
            session = requests.session()
            temp_res=session.get('https://weibo.cn/u/%s'%uid,headers=self.headers)
            temp_res.encoding = 'utf-8'
            temp_soup = BeautifulSoup(temp_res.text, 'html.parser')
            print(temp_soup)
            page_num=temp_soup.find_all(attrs={'name':'mp'})
            if page_num:#微博只有一页时
                page_num=int(page_num[0].attrs['value'])
            else:
                page_num=1
            if page_num>=10:#小于10抽样为0
                random_view_page=random.sample(range(2,page_num+1),int(0.1*page_num))#避开第一页
            elif 1<page_num<10:
                random_view_page = random.sample(range(2, page_num + 1), 1)
            else:
                random_view_page=[1]
            for num in random_view_page:
                temp_temp_res=session.get('https://weibo.cn/u/%s?page=%s&vt='%(uid,str(num)),headers=self.headers)
                temp_temp_res.encoding='utf-8'
                temp_temp_soup=BeautifulSoup(temp_temp_res.text,'html.parser')
                weibo_content=temp_temp_soup.find_all(attrs={'class':'ctt'})
                if page_num==1:
                    weibo_content=weibo_content[1:]
                for content in weibo_content:#括号和url频率
                    if '【' in content.text:
                        dakuohao_count+=1
                    if '#' in content.text:
                        url_count+=1
                time.sleep(5)
                patter_like=re.compile("赞\[")
                weibo_like=temp_temp_soup.find_all('a',text=patter_like)#点赞量
                for i in weibo_like:
                    weibo_like_list.append(i.text)
                patter_tran = re.compile("转发\[")
                weibo_tran = temp_temp_soup.find_all('a', text=patter_tran)  # 被转发量
                for i in weibo_tran:
                    weibo_tran_list.append(i.text)
                patter_comment = re.compile("评论\[")
                weibo_comment_raw = temp_temp_soup.find_all('a', text=patter_comment)  # 评论量
                weibo_comment=weibo_comment_raw.copy()
                for i in weibo_comment:
                    if '原文'in i.text:
                        weibo_comment.remove(i)
                for i in weibo_comment:
                    weibo_comment_list.append(i.text)
                weibo_tran_like=temp_temp_soup.find_all('span',text=patter_like)#转发博文点赞量
                for i in weibo_tran_like:
                    weibo_tran_like_list.append(i.text)
                weibo_tran_tran = temp_temp_soup.find_all('span', text=patter_tran)  # 转发博文被转发量
                for i in weibo_tran_tran:
                    weibo_tran_tran_list.append(i.text)
                weibo_tran_comment=[]#转发博文评论量
                for i in weibo_comment_raw:
                    if '原文' in i.text:
                        weibo_tran_comment.append(i)
                for i in weibo_tran_comment:
                    weibo_tran_comment_list.append(i.text)
                weibo_time_and_resourse=temp_temp_soup.find_all(attrs={'class':'ct'})
                for i in weibo_time_and_resourse:
                    weibo_time_and_resourse_splited=i.text.split('\xa0来自')
                    weibo_time_list.append(weibo_time_and_resourse_splited[0])
                    if len(weibo_time_and_resourse_splited)==2:
                        weibo_resourse_list.append(weibo_time_and_resourse_splited[1])
                    else:
                        weibo_resourse_list.append(None)
            res_origional=session.get('https://weibo.cn/u/%s?filter=1'%uid,headers=self.headers)
            res_origional.encoding = 'utf-8'
            soup_origional = BeautifulSoup(res_origional.text, 'html.parser')
            origional_weibo_page_num=soup_origional.find_all(attrs={'name':'mp'})
            if origional_weibo_page_num:  # 原创微博只有一页时
                origional_weibo_page_num = int(origional_weibo_page_num[0].attrs['value'])
            else:
                origional_weibo_page_num = 1
            weibo_origional_list.append(origional_weibo_page_num)
            time.sleep(1)
            self.all_dakuohao_count.append(dakuohao_count)
            self.all_url_count.append(url_count)
            self.all_weibo_like_list.append(weibo_like_list)
            self.all_weibo_tran_list.append(weibo_tran_list)
            self.all_weibo_comment_list.append(weibo_comment_list)
            self.all_weibo_tran_like_list.append(weibo_tran_like_list)
            self.all_weibo_tran_tran_list.append(weibo_tran_tran_list)
            self.all_weibo_tran_comment_list.append(weibo_tran_comment_list)
            self.all_weibo_time_list.append(weibo_time_list)
            self.all_weibo_resourse_list.append(weibo_resourse_list)
            self.all_weibo_origional_list.append(weibo_origional_list)
            # print(dakuohao_count)
            # print(url_count)
            # print('.......')
            # print(weibo_like_list)
            # print(weibo_tran_list)
            # print(weibo_comment_list)
            # print('........')
            # print(weibo_tran_like_list)
            # print(weibo_tran_tran_list)
            # print(weibo_tran_comment_list)
            # print(len(weibo_tran_like_list))
            # print(len(weibo_tran_tran_list))
            # print(len(weibo_tran_comment_list))
            # print('..........')
            # print(weibo_time_list)
            # print(weibo_resourse_list)
            # print('%%%%%%%%%')
            print(self.count)
            self.count+=1
        return pd.DataFrame({'id':self.uidlist,'dakuohao_count':self.all_dakuohao_count,
        'url_count':self.all_url_count,
        'weibo_like':self.all_weibo_like_list,
        'weibo_tran':self.all_weibo_tran_list,
        'weibo_comment':self.all_weibo_comment_list,
        'weibo_tran_like':self.all_weibo_tran_like_list,
        'weibo_tran_tran':self.all_weibo_tran_tran_list,
        'weibo_tran_comment':self.all_weibo_tran_comment_list,
        'weibo_time':self.all_weibo_time_list,
        'weibo_resourse':self.all_weibo_resourse_list,
        'weibo_origional':self.all_weibo_origional_list})





if __name__=='__main__':
    temp_cookie='_T_WM=ae57a16a2c2ba42543767d2f324afd2f; SCF=Ah9bFABp_WkcefnWf-Nxu_zMFPf2-PXB2ZUG83sgfDhhyw6j04qEfpgJ5jz5Tc_Q4ndyiRSNXEigPJWcVg9qMtg.; H5_wentry=H5; backURL=https%3A%2F%2Fweibo.cn%2F; ' \
                'SUB=_2A25xs4MDDeRhGeBO6loR8SzPzzuIHXVTXy1LrDV6PUJbkdANLXX6kW1NRdzJPxOWC7vHq7HSmzrxk93t6x8r84nc; SUHB=0ebt-bi55PbPWU; SSOLoginState=1555559251'
    # second_corpse_fans=My_fans(temp_cookie)
    # second_corpse_fans_uid=second_corpse_fans.get_fans_uid()
    # temp_file=open(r'C:\Users\A\Desktop\second_corpse_fans_uid.txt','w')
    # temp_file.write(str(second_corpse_fans_uid))
    df=pd.read_excel('真人uid.xlsx')
    a=[]

    for i in df.index:
        a.append(str(df.loc[i][210005629]))
    a.append('210005629')
    a=list(set(a))

    # a = [ '2840295044','1882018632','2259417313']
    second_corpse_fans_indiv=fans_info(a[700:],temp_cookie)
    # fans_base_info=second_corpse_fans_indiv.get_fans_base_info()
    # fans_base_info.to_excel('second_corpse_fans_base_info.xlsx')
    fans_weibo_base_info=second_corpse_fans_indiv.get_fans_weibo_base_info()
    fans_weibo_base_info.to_excel('true_fans_base_weibo_info_more700.xlsx')
