from bs4 import BeautifulSoup
import re
import requests
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
from dcard import Dcard  #DcardSpider套件，可以直接爬Dcard文章取得後設資訊


##獲取網站
url = "https://www.dcard.tw"
BOARD = 'horoscopes'
ARTICLE_NUM=10000 #輸入100的倍數
myfont = FontProperties(fname=r'./GenYoGothicTW-Regular.ttf')


##定義變數
kind=4      #w改成kind
horo_num=12 #h改成horo_num
sum_of = [[0 for x in range(kind)] for y in range(horo_num)]
horo_string = [[0 for x in range(kind)] for y in range(horo_num)] #horo改成horo_string
horo_string_boy = [[0 for x in range(kind)] for y in range(horo_num)] 
horo_string_girl = [[0 for x in range(kind)] for y in range(horo_num)] 
custom_sum = [ 0 for x in range(horo_num)]
horo_list = [[] for y in range(horo_num)]
max_like = [[0 for x in range(kind)] for x in range(horo_num)]                    
content_horo = []                                                      
output = []                                                          
search_query=[""]
post=[]    #n改成post


##定義變數    
horo_string=["牡羊","金牛","雙子","巨蟹","獅子","處女","天秤","天蠍","射手","摩羯","水瓶","雙魚"]
horo_string_boy=["牡羊男","金牛男","雙子男","巨蟹男","獅子男","處女男","天秤男","天蠍男","射手男","摩羯男","水瓶男","雙魚男"]
horo_string_girl=["牡羊女","金牛女","雙子女","巨蟹女","獅子女","處女女","天秤女","天蠍女","射手女","摩羯女","水瓶女","雙魚女"]
horo_english=["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"] #b改成horo_english
title_list=[]
excerpt_list=[]
id_list=[]
gender_list=[]
like_list=[]                                                       


##將原本的Search_Board()函式分成兩個，新的Search_Board()函式專門存取Dcard網站上的資訊，Count_gender(gender_list)函式專門計算男女發文的次數
##爬星座版，存取其中的title,excerpt,id,gender,likeCount，並 return title_list,excerpt_list,id_list,gender_list
def Search_Board():
  dcard = Dcard()
  forum = dcard.forums('horoscopes')

  for forum in forum.get_metas(num=10000):
    title_list.append(forum['title'])
    excerpt_list.append(forum['excerpt'])
    id_list.append(forum['id'])
    gender_list.append(forum['gender'])
    like_list.append(forum['likeCount'])

  return  title_list, excerpt_list, id_list, gender_list


##計算男女發文的次數
def Count_gender(gender_list):

  post_Male=0   #post_M改為post_Male
  post_Female=0 #post_F改為post_Female

  for i in range(ARTICLE_NUM):
    if gender_list[i]=='M':
      post_Male+=1
    if gender_list[i]=='F':
      post_Female+=1

  post.append(post_Male)
  post.append(post_Female)


##尋找文章數量
##用in運算子取代原本搜尋字串的for迴圈        
def Search_String(title_list, excerpt_list, like_list, id_list):  
    for k in range(12):
        #尋找提到各星座的文章數量
        max_like_e=0
        for i in range(ARTICLE_NUM):
            #爬標題
            flag_title_searched=0
            if horo_string[k] in title_list[i]:
              if flag_title_searched==0:
                sum_of[k][0]+=1
                horo_list[k].append(id_list[i])
                flag_title_searched=1
                if like_list[i]>max_like_e:                 
                  max_like_e=like_list[i]             
                  max_like_id_e=id_list[i]           
                  max_like_title_e=title_list[i]
            #爬內容  
            if  horo_string[k] in excerpt_list[i]:
              if flag_title_searched==0:
                sum_of[k][1]+=1
                horo_list[k].append(id_list[i])
                if like_list[i]>max_like_e:                
                  max_like_e=like_list[i]                 
                  max_like_id_e=id_list[i]             
                  max_like_title_e=title_list[i]

        max_like[k][0]=max_like_e                 
        max_like[k][1]=max_like_id_e                
        max_like[k][2]=max_like_title_e
       

def Gender_Article(title_list, excerpt_list):

    for k in range(12):
        #尋找提到各星座提到男女的文章數量
        for i in range(ARTICLE_NUM):
            flag_male=0           #flag_m改為flag_male
            flag_female=0         #flag_f改為flag_female
            flag_male_excerpt=0   #me改為male_excerpt
            flag_female_excerpt=0 #me改為female_excerpt
            flag_title_searched_m=0
            flag_title_searched_f=0
            #爬標題
            if horo_string_boy[k] in title_list[i]:
                if flag_male==1:
                    break
                else:
                  sum_of[k][2]+=1
                  flag_male=1
                  flag_title_searched_m=1
            elif horo_string_girl[k] in title_list[i]:
                if flag_female==1:
                    break
                else:
                  sum_of[k][3]+=1
                  flag_female=1
                  flag_title_searched_f=1
            #爬內容
            if horo_string_boy[k] in excerpt_list[i]:
                if flag_male_excerpt==1:
                    break
                else:
                  if flag_title_searched_m==0:
                    sum_of[k][2]+=1
                    flag_male_excerpt=1

            elif horo_string_girl[k] in excerpt_list[i]:
                if flag_female_excerpt==1:
                    break
                else:
                  if flag_title_searched_f==0:
                    sum_of[k][3]+=1
                    flag_female_excerpt=1


##搜尋關鍵字
def Search_Custom(title_list,excerpt_list):
    for k in range(12):
        custom_sum[k]=0
    for i in range(ARTICLE_NUM):
        flag_custom=0
        for j in range(len(title_list[i])-1):
            if title_list[i][j]==search_query[0]:
                if title_list[i][j+1]==search_query[1]:
                    if flag_custom==0:                                 
                        for k in range(12):
                            for m in range(len(horo_list[k])):
                                if id_list[i]==horo_list[k][m]:
                                    custom_sum[k]+=1
                                    flag_custom=1
                                    break
            #爬內容
        for j in range(len(excerpt_list[i])-1):
            if excerpt_list[i][j]==search_query[0]:
                if excerpt_list[i][j+1]==search_query[1]:
                    if flag_custom==0:
                        for k in range(12):
                            for m in range(len(horo_list[k])):
                                if id_list[i]==horo_list[k][0]:
                                    custom_sum[k]+=1
                                    flag_custom=1
                                    custom_sum[k]+=1
                                    break
    return custom_sum
        


##最多讚數
def Most_Like(max_like,horo_string,title_list):                
    for k in range(12):
        res = requests.get(url + "/f/horoscopes/p/" + str(max_like[k][1]))
        soup = BeautifulSoup(res.text, 'html.parser')
        for entry in soup.select('article div'):
            if entry.has_attr('class'):
                item = re.search('sc-4ihej7-0',entry['class'][0])
                if item is not None:
                    content = entry.text
                    content_horo.append(content)
                    break

        output.append(str(horo_string[k])+" 讚數："+str(max_like[k][0])+" \t"+str(max_like[k][2])+"\n"+str(content_horo[k])+"\n")
    return output
        


##畫圖表
def Plot_Graph(ans):
    
    title_count_list=[]     #a改為title_count_list
    content_list=[]         #c改為content_list
    boy_list=[]             #d改為boy_list
    girl_list=[]            #e改為girl_list
    add_list=[]             #f改為add_list
    gender=["Male","Female"]#h改為gender
    
    for k in range(12):
        title=sum_of[k][0]
        content=sum_of[k][1]
        add=sum_of[k][0]+sum_of[k][1]
        boy=sum_of[k][2]
        girl=sum_of[k][3]
        key=custom_sum[k]
        title_count_list.append(title)
        content_list.append(content)
        add_list.append(add)
        boy_list.append(boy)
        girl_list.append(girl)
    

    ##星座男女討論度比較/男女發文數比例    
    if ans==1:
        plt.title("Horoscope Investigation",fontsize=20)
        plt.subplot(121)
        plt.plot(figsize=(20,5))
        plt.xticks(fontsize=5)
        plt.yticks(fontsize=8)
        plt.rcParams["font.family"]="DejaVu Sans"
        plt.xlabel('Horoscope',fontsize=15)
        plt.ylabel('Number',fontsize=15)
        p1=plt.bar(horo_english,boy_list,label = 'Male',align = "edge", width = 0.35)
        p2=plt.bar(horo_english,girl_list,label = 'Female',align = "edge", width = -0.35)
        plt.legend()
        plt.subplot(122)
        plt.plot(figsize=(3,3))
        plt.pie(post,labels=gender,autopct='%1.1f%%')

        plt.show()

    
    ##各星座討論度比較
    if ans==2 or ans==3:
        plt.figure(figsize=(15,5))
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        plt.rcParams["font.family"]="DejaVu Sans"    
        plt.xlabel('Horoscope',fontsize=20)
        plt.ylabel('Number',fontsize=20)
        if ans==2: 
          plt.bar(horo_english,add_list)
        elif ans==3:
          plt.bar(horo_english,custom_sum)
        plt.title("Horoscope Investigation",fontsize=25)
        plt.show()

        

##初始畫面
if __name__ == '__main__':

    Search_Board()
    Count_gender(gender_list)
    Search_String(title_list, excerpt_list, like_list, id_list) 
    Gender_Article(title_list, excerpt_list)            
    
    for k in range(12):                
        print(horo_string[k],"\t符合文章： ",sum_of[k][0]+sum_of[k][1],"\t男： ",sum_of[k][2],"\t女： ",sum_of[k][3],"\t最多按讚文: 讚:\t",max_like[k][0],"\t",max_like[k][2],sep="")  

    print("")
    
    Most_Like(max_like,horo_string,title_list)                

    mode=""
    while mode!=0:
        mode=eval(input("請輸入模式（1：查詢最多按讚文，2：畫圖表，3：查詢關鍵字,0：結束)\t："))

        ##查詢最多按讚文
        if mode==1:
            output_n=""                 
            while output_n!=0:
                    output_n=eval(input("輸入項查詢的星座：\n1.牡羊 2.金牛 3.雙子 4.巨蟹 5.獅子 6.處女 7.天秤 8.天蠍 9.射手 10.摩羯 11.水瓶 12.雙魚 （輸入0跳過）: \n"))
                    if output_n==0:
                        break
                    elif output_n>0 and output_n<13:
                        print("")
                        print(output[output_n-1])
                        print("")

        ##畫圖表
        if mode==2:
            ans=""
            while ans!=0:
                ans=eval(input('輸入繪圖模式（1：各星座男女討論度比較，2：各星座討論度比較，0：跳過）:'))
                if ans==0:
                    break
                elif ans>0 and ans<3:
                    Plot_Graph(ans)

        ##查詢關鍵字
        if mode==3:
            search_query=""
            while search_query!="0":
                search_query=str(input("輸入查詢字眼（需輸入兩個字，輸入0跳過）： "))
                
                if search_query=="0":
                    break
                elif len(search_query)!=2:
                    search_query=str(input("請輸入兩個字的詞，輸入0跳過： "))
                else:
                    Search_Custom(title_list,excerpt_list)
                    for k in range(12):
                        print(horo_string[k],"\t",custom_sum[k])
                    ans=3
                    Plot_Graph(ans)