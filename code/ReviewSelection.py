# -*- coding:utf-8 -*-

# 利用扩充的字典，筛选有关的review数据

import os
import json
import string

import SemanticExpansion as se
from nltk.corpus import stopwords


# 单词共现的阈值
global threshold
threshold=0.3

# 添加去除标点符号，词源
def word_process():
    pass

#
def contains(sentence,word_list):
    count = 0
    for word in sentence:
        for i in word_list:
            count=count+word.count(i)
    return count

# review评论列列表，dic_contents字典
# 补充threshold？？？？
def select(review,dic_contents):
    count_map={}
    max=0
    per=""
    for key in dic_contents.keys():
        permission=key
        value=dic_contents[key]
        count=contains(review,value)
        if 1.0*count/len(review)>max:
            max=1.0*count/len(review)
            per=permission
        count_map[permission]=1.0*count/len(review)

    if max>threshold:
        # print per,dic_contents[per]
        return True
    else:
        return False
    # return per

# 获取扩充后的语义字典
def get_dic():
    contents=se.output("../data/dictionary")
    return contents


# 将字符串转为列表
# 添加词源处理
# 去除标点符号等
# .......待补充相关内容
def sentence_to_list(sentence):
    word_list=[]
    items=sentence.split(" ")
    word_list=se.stopword(items)
    return word_list


def read_json(path):
    file_json=open(path)
    fp=json.load(file_json)
    store_map={}
    count_ids=0

    dics=get_dic()
    for app_id in fp:
        for key in app_id.keys():
            # key为app的ID
            count_ids=count_ids+1
            print "App:   ",count_ids
            app_contents=app_id[key]
            contents=[]
            for item in app_contents:
                review_content=item["review_contents"]

                if select(sentence_to_list(review_content),dics):
                    contents.append(review_content)
            if len(contents)!=0:
                store_map[key]=contents
                # print review_content

    path_name=path[path.rindex('/')+1:path.index('.')]
    url="../review_data/contents_"+path_name+".json"
    file_new=open(url,"w+")
    # file_new=open("../data/contents.json","w+")
    # print store_map.keys()
    json.dump(store_map,file_new)
    file_new.close()
    file_json.close()
    print url,'    finished!'

# 输出的格式：permission_name,list(reviews)
def parse(dir='E:/execution/data'):
    files=os.listdir(dir)
    for path in files:
        read_json(dir+"/"+path)

if __name__ == '__main__':
    # parse()
    s="It's the mobile version of Zuma basically. LOVE this game! Thanks!"
    print sentence_to_list(s)
