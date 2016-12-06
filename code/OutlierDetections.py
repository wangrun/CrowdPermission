# -*- coding: utf-8 -*-

# 计算topic中permission的具体信息，需要检索app的权限列表，得到某一个类别中permission的分布情况
import os
import sys
import json
import tool as tl
import string
import result


# 存储Google Paly的app信息列表
global permission_contents
permission_contents=[]


# 读取所有的app的信息，其中包括permission的数据，存放在permission_contents列表
def read_app_permission(path="F:/ky/AppReview/summary_metadata_GooglePlay"):
    dir = os.listdir(path)
    for file_path in dir:
        path_file=path+"/"+file_path
        file=open(path_file)
        file_json=json.load(file)
        permission_contents.append(file_json)
        file.close()

    print "File read completed!"


# 返回app_id的权限信息数据
def permission_id(app_id):
    for index in permission_contents:
        if app_id in index.keys():
            return index[app_id][0]
        else:
            continue

# 返回topic，list(app_id)
# topic_app，topic_app的格式{topic:list(app_id)}
def get_topic_app():
    map_content=result.sort_data()
    return result.cluster(map_content)

# 根据一个topic，输出其topic中的所有权限列表信息，包含有重复的数据
def topic_list_per(topic_app,topic_id):
    app_list=topic_app[topic_id]
    list_per=[]
    for item in app_list:
        permission_app_id=permission_id(item)
        if permission_app_id==None:
            continue
        list_per=list_per+permission_app_id

    return list_per


# 获得文中研究的permission信息
# 与topic对应的permission内容
def get_permission_dic(path="../data/dictionary"):
    file = open(path)
    permissions=[]
    count = 1
    for line in file:
        if count%2==1:
            permissions.append(line.strip())
        else:
            pass
        count=count+1
    file.close()

    return permissions


# 输出一个主题下的权限信息，包含permission_name和percentage
# output格式：list((num,permission_name))
def find_topic_permission(topic_app,topic_id):
    if topic_id in topic_app.keys():
        values=topic_list_per(topic_app,topic_id)
        value_permission=get_permission_dic()
        pairs=[]
        for val in value_permission:
            num=1.0*values.count(val)/len(topic_app[topic_id])
            store=(num,val)
            pairs.append(store)

        pairss=list(set(pairs))
        pairss.sort(key=lambda x:x[0],reverse=True)

# list((num,permission_name))
        return pairss
    else:
        return None

# ............待测试
# 返回所有主题下的权限信息列表
def get_topic_permissions(topic_app):
    topic_permission_percentage=[]
    for topic_id in range(0,len(topic_app.keys())):
        lists=find_topic_permission(topic_app,topic_id)
        print "Topic",topic_id,":"
        print lists
        per_lis=get_permission_dic()
        topic_per=range(0,len(per_lis))
        for i in range(0,len(per_lis)):
            for item in lists:
                if item[1]==per_lis[i]:
                    topic_per[i]=item[0]

        topic_permission_percentage.append(topic_per)

    return topic_permission_percentage

# 返回映射表
def define_topic_permission(topic_app):
    arr=get_topic_permissions(topic_app)
    tl.iterate(arr)
    topic_permission=tl.get_max(arr)
    # permission_1,permission_2
    # topic_x,topic_y
    # 输出的为对应的topic_id
    return topic_permission

# ...............



# topic_app:{topic_name,list(app)}主题和应用的字典
# app_id：应用的ID号
# 输出根据系统计算得出的应用权限内容
def Real_permission(topic_app,app_id):
    iterate=0
    # app 计算得出的permission列表
    topic_app_per=[]
    # app_id 所属的topic
    topic_list_app_id=[]
    for topic_key in topic_app.keys():
        app_lists=topic_app[topic_key]
        if app_id in app_lists:
            topic_list_app_id.append(topic_key)
    # print "App:",app_id,"     Topic:",topic_list_app_id

    for topic_num in topic_list_app_id:
        print "Iterate:",iterate
        iterate=iterate+1
        per=find_topic_permission(topic_app,topic_num)
        if per is not None:
            topic_app_per.append(per)
        else:
            print "error!"

    return app_id,topic_list_app_id,topic_app_per

def final(app_ID):
    read_app_permission()
    topic_app=get_topic_app()
    permission_cal=Real_permission(topic_app,app_ID)
    permission_raw=permission_id(app_ID)

    print "APP:  ",permission_cal[0]
    print "Topic_lists: ",permission_cal[1]
    print "Topic_permission_percentage:",permission_cal[2]
    print "App permission information:",permission_raw


def output_topic_permission():
    read_app_permission()
    topic_app=get_topic_app()
    s=define_topic_permission(topic_app)
    print s

def main():
    final("com.poynt.android")

if __name__ == '__main__':
    main()
