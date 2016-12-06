# -*- coding:utf-8 -*-

import math
import json

# map_content:  key(文本行号)，value:(index_origin,float_value)
# LDA 模型训练的结果
def sort_data(path="../result_data/k20.pz_d"):
    file=open(path)
    line_num=0
    map_content={}
    for line in file:
        list=[]
        index=0
        for word in line.split():
            if math.isnan(float(word)):
                list.append((index,0.0))
            else:
                list.append((index,float(word)))
            index=index+1
        list.sort(key=lambda x:x[1],reverse=True)
        map_content[str(line_num)]=list
        line_num=line_num+1
    file.close()
    # print len(map_content.keys())
    return map_content

# output{output a dic,(key:topic_id,value:app_id)}
# input{key:topic_id,value:lists of reivew_item_id}
def parse_review_to_docs(map_cluster):
    map_dic={}
    # document id mapping
    path="../merge_data/review_id.txt"
    file=open(path)
    for line in file:
        key=line.split()[0].strip()
        value=line.split()[1].strip()
        map_dic[key]=value
    # s=set()
    file.close()
    clustering={}
    for key in map_cluster.keys():
        s=set()
        list_reviews=map_cluster[key]
        for review_item in list_reviews:
            str_review_item=str(review_item)
            app_id=map_dic[str_review_item]
            s.add(app_id)
        clustering[key]=list(s)
    return clustering


# 将topic list(app_id) 写到文件
def write_result_to_file(clustering,path="../result_data/topic_app.txt"):
    file = open(path,'w')
    for topic in clustering.keys():
        app_list=clustering[topic]
        file.write("topic"+str(topic)+"\n")
        for val in app_list:
            file.write(val+" ")
        file.write("\n")
    file.close()


# input{key:review_id,value(topic_id,value_pro),已经排过序},
# output{topic_id,list(app_id)}
def cluster(map_content):
    # topic id:list(reivew_item_id)
    map_cluster={}
    for key in map_content.keys():
        value_list=map_content[key]
        # 找出概率最大的topic   max
        # 此处的聚类方法需要修改，修改为K-means的聚类，而非直接采取最大值的方式
        # 取top5的最大值？

        topic_id=value_list[0][0]

        if topic_id not in map_cluster.keys():
            review_id=[]
            review_id.append(key)
            map_cluster[topic_id]=review_id
        else:
            review_id=map_cluster[topic_id]
            review_id.append(key)
            map_cluster[topic_id]=review_id
# 输出  key:topic_id   values:app_id
    clustering=parse_review_to_docs(map_cluster)

    write_result_to_file(clustering)

    return clustering

def main():
    map_content=sort_data()
    cluster(map_content)

if __name__ == '__main__':
    main()
