import requests
import json
import emoji
import jieba
import os
import wordcloud 
stopWordList=open('stopWord.txt').read().splitlines()
member_list=[]
#分词
def jiebaClearText(text):
    
    jieba_list=jieba.cut(text,cut_all=False)
    
    #return ' '.join(list)
    outstr=""
    for word in jieba_list:
        if word not in stopWordList:
            outstr += " "
            outstr += word                 
    return outstr


def get_pl (av,ff,page=1):
    try:
        payload={'oid':av,'type':'1','next':str(page)}
        response = requests.get('https://api.bilibili.com/x/v2/reply/main', params=payload)
        response_json=response.json()
        
        #print((response_json['data']['cursor']['is_end']))
        if not (response_json['data']['cursor']['is_end']):
            for i in response_json['data']['replies']:
                print('\n'+str(i['member']['uname'])+':'+emoji.demojize(str(i['content']['message'])))
                member_list.append(i['member']['uname'])
                ff.write(jiebaClearText(emoji.demojize(i['content']['message'])))    
                if not i['replies'] == None:
                    for each in i['replies']:
                        print('\n'+str(each['member']['uname'])+':'+emoji.demojize(str(each['content']['message'])))
                        member_list.append(each['member']['uname'])
                        ff.write(jiebaClearText(emoji.demojize(str(each['content']['message']))))    
            get_pl(av,ff,page+1)
        else:
             print("成功获取全部评论及回复")
             print("一共有%d页"%(int(response_json['data']['cursor']['prev'])-1))
    except:
        print("可能出现了未知的错误")

def makeWordCloud(cloudText,filename):
    if(cloudText == "" ):
        print("评论为空")

    else:
        w=wordcloud.WordCloud(
            font_path='C:/Windows/Fonts/simkai.ttf',
            background_color='white',
            width=4096,
            height=2160,
            max_words=1000,
        )
        w.generate(cloudText)
        w.to_file(filename+".png")
        os.startfile(filename+".png")
        #os.startfile(av+".txt")

def somebody_in(name):
    for each in member_list:
        if each==name:
            print('找到目标用户')
            break
    else:
        print("没有找到目标用户")

if  __name__=="__main__":
    av=input("输入AV号：")
    file_open=open(av+".txt",'w',encoding='utf-8')
    get_pl(av,file_open)
    file_open.close()
    text=open(av+'.txt','r',encoding='utf-8').read()
    makeWordCloud(text,av)
   #somebody_in("大哥大非常大")
    
    


    
