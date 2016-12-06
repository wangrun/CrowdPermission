# -*- coding: utf-8 -*-


# 计算topic中permission的具体信息，需要检索app的权限列表，得到某一个类别中permission的分布情况
import os
import sys
import json
import string
import result


# 存储Google Paly的app信息列表
global permission_contents
permission_contents=[]
# 根据输入的app ID编号，输出app的路径
def find_app_id(app_id):
    # root_path="E:/experiment data/Google Play/metadata"
    # root_path="H:/metadata"
    root_path="J:/Google Play/metadata"
    dirs=os.listdir(root_path)
    for dir in dirs:
        lis_dir=root_path+"/"+dir
        app_dir=os.listdir(lis_dir)
        if app_id+".json" in app_dir:
            return lis_dir+"/"+app_id+".json"

# 根据输入的app ID编号，输出app的权限列表信息
def permission_id_old(app_id):
    path=find_app_id(app_id)
    if path==None:
        return None
    file=open(path)
    f=json.load(file)
    docid=f["docid"]
    details=f["details"]
    app_details=details["app_details"]
    if "permission" not in app_details.keys():
        return None
    permission=app_details["permission"]

    file.close()
    # print app_id,permission
    return permission

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


# ...........
def permission_id(app_id):
    for index in permission_contents:
        if app_id in index.keys():
            return index[app_id][0]
        else:
            continue


# 返回topic，list(app_id)
# topic_app
def get_topic_app():
    map_content=result.sort_data()
    return result.cluster(map_content)

# 根据一个topic，输出其topic中的所有权限列表信息
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



# .....................................
# 返回topic_id的潜在语义permission_name
# list((比例，permission))
def find_topic_permissions(topic_app,topic_id):
    if topic_id in topic_app.keys():
        values=topic_list_per(topic_app,topic_id)
        value_permission=get_permission_dic()
        pairs=[]

        for val in value_permission:
            num=1.0*values.count(val)/len(topic_app[topic_id])
            store=(num,val)
            pairs.append(store)

        # for data in values:
        #     num=values.count(data)
        #     store=(num,data)
        #     pairs.append(store)
        # 去除重复元素
        pairss=list(set(pairs))
        pairss.sort(key=lambda x:x[0],reverse=True)

# list((num,permission_name))
        return pairss

    #     s=set()
    #     for temp in pairs:
    #         s.add(temp)
    #         if len(s)==top_number:
    #             return s
    # else:
    #     return None

# arr列表中有value的所有位置
def find_same(arr,value):
    index_arr=[]
    index=0
    for val in arr:
        if val==value:
            index_arr.append(index)
        index=index+1
    return index_arr


def find_max(arr,indexs):
    max=arr[indexs[0]]
    for i in indexs:
        if arr[i]>max:
            max=arr[i]
    return arr.index(max)


# topic是列表，共长度为permission的个数，相应的值是permission_name,索引是第i个主题
def find_iterate(topic,info):
    if len(topic)==len(set(topic)):
        return topic
    else:
        for val in topic:
            if topic.count(val)>1:
                indexs=find_same(topic,val)
                index_max=find_max(topic,indexs)
                for i in indexs:
                    if i!=index_max:
                        permission_name=topic[i]
                        topic_info=info[i]
                        # 排好序的列表，（比例，权限名称）
                        index_j=0
                        index_prior=0
                        for j in topic_info:
                            if j[1]==permission_name:
                                index_prior=index_j
                                print "Same index:",index_j
                            index_j=index_j+1
# 边界检查？
                        topic[i]=info[i][index_prior+1]
                        find_iterate(topic,info)





def define_topic_permission(topic_app):
# 存放主题与权限的映射信息列表
# x修改需要初始化，。。。。。。。。。？？？？？？？？？？？？
    topic_mapping=[]
    # topic下面关于paper中权限的比例信息，按序排列
    topic_permisssion_summary={}
    for topic_id in topic_app.keys():
        topic_permisssion_summary[topic_id]=find_topic_permission(topic_app,topic_id)
        topic_mapping[topic_id]=topic_permisssion_summary[topic_id][0][1]

    return find_iterate(topic_mapping,topic_permisssion_summary)


def define_topic_permission_test(topic_app):
    # 存放主题与权限的映射信息列表
        topic_mapping=["","","","","","","",""]
        # topic下面关于paper中权限的比例信息，按序排列
        # topic_permisssion_summary={}
        for topic_id in topic_app.keys():
            topic_mapping[topic_id]=topic_app[topic_id][0][1]
            # print topic_app[topic_id][0][1]

        return find_iterate(topic_mapping,topic_app)



# .................

# 返回topic_id的潜在语义permission_name
def find_topic_permission(topic_app,topic_id,top_number=1):
    if topic_id in topic_app.keys():
        values=topic_list_per(topic_app,topic_id)
        pairs=[]
        for data in values:
            num=values.count(data)
            store=(num,data)
            pairs.append(store)
        pairs.sort(key=lambda x:x[0],reverse=True)
        s=set()
        for temp in pairs:
            s.add(temp)
            if len(s)==top_number:
                return s
    else:
        return None

def find_topic_permissionsss(topic_app,topic_id):
    if topic_id in topic_app.keys():
        values=topic_list_per(topic_app,topic_id)
        value_permission=get_permission_dic()
        pairs=[]
        for val in value_permission:
            num=1.0*values.count(val)/len(topic_app[topic_id])
            store=(num,val)
            pairs.append(store)

        # for data in values:
        #     num=values.count(data)
        #     store=(num,data)
        #     pairs.append(store)
        # 去除重复元素
        pairss=list(set(pairs))
        pairss.sort(key=lambda x:x[0],reverse=True)

# list((num,permission_name))
        return pairss
    else:
        return None



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
    print "App:",app_id,"     Topic:",topic_list_app_id

    for topic_num in topic_list_app_id:
        print "Iterate:",iterate
        iterate=iterate+1
        per=find_topic_permissionsss(topic_app,topic_num,top_number=1)
        if per is not None:
            topic_app_per.append(per)
        else:
            print "error!"

    return topic_app_per

def final(app_ID):
    read_app_permission()
    topic_app=get_topic_app()
    permission_cal=Real_permission(topic_app,app_ID)
    permission_raw=permission_id(app_ID)
    print "calculation:",permission_cal
    print "raw:",permission_raw


def test():
    topic_app={0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[]}
    topic_app[0]=[(0.3,"permission1"),(0.21,"permission2"),(0.17,"permission3"),(0.15,"permission4"),(0.1,"permission5"),(0.08,"permission6"),(0.06,"permission7"),(0.03,"permission8")]
    topic_app[1]=[(0.4,"permission2"),(0.1,"permission6"),(0.08,"permission3"),(0.06,"permission5"),(0.02,"permission6"),(0.01,"permission1"),(0.01,"permission4"),(0.01,"permission8")]
    topic_app[2]=[(0.24,"permission8"),(0.21,"permission6"),(0.19,"permission2"),(0.17,"permission4"),(0.14,"permission3"),(0.12,"permission1"),(0.11,"permission7"),(0.09,"permission5")]
    topic_app[3]=[(0.36,"permission1"),(0.31,"permission2"),(0.21,"permission3"),(0.18,"permission4"),(0.13,"permission5"),(0.12,"permission6"),(0.1,"permission7"),(0.08,"permission8")]
    topic_app[4]=[(0.34,"permission2"),(0.32,"permission7"),(0.26,"permission3"),(0.11,"permission5"),(0.08,"permission1"),(0.03,"permission6"),(0.02,"permission4"),(0.01,"permission8")]
    topic_app[5]=[(0.28,"permission5"),(0.14,"permission3"),(0.12,"permission1"),(0.08,"permission2"),(0.07,"permission7"),(0.07,"permission6"),(0.06,"permission8"),(0.05,"permission4")]
    topic_app[6]=[(0.37,"permission8"),(0.31,"permission2"),(0.29,"permission6"),(0.26,"permission7"),(0.24,"permission3"),(0.14,"permission5"),(0.09,"permission1"),(0.04,"permission4")]
    topic_app[7]=[(0.5,"permission3"),(0.2,"permission2"),(0.1,"permission1"),(0.02,"permission4"),(0.01,"permission7"),(0.009,"permission6"),(0.008,"permission5"),(0.007,"permission8")]

    # print topic_app[0][0][1]

    topics=define_topic_permission_test(topic_app)
    print topics

def main():
    # map=get_topic_app()
    # Real_permission(map,"com.poynt.android")

    # read_app_permission()
    # print permission_id("com.poynt.android")

    final("com.poynt.android")
    # print get_permission_dic()

if __name__ == '__main__':
    # main()
    map=get_topic_app()
    for key in map.keys():
        list_app_id=map[key]
        print "Topic:",key,"App_lists:",list_app_id
        break
