# -*- coding:utf-8 -*-

import os
import sys
import json
import string


# 统计筛选的用户评论数据，返回app的个数和用户评论的条目数
def review_data_statistic():
    path="../review_data"
    count_review=0
    count_id=0
    dir=os.listdir(path)
    for paths in dir:
        p=path+"/"+paths
        f=open(p)
        json_file=json.load(f)
        count_id=count_id+len(json_file.keys())
        for key in json_file.keys():
            count_review=count_review+len(json_file[key])
        f.close()
    print "APP_ID:",count_id,"Review_count:",count_review

# 统计原始抓取数据的信息，包括抓取的app和用户评论的数量
def raw_data_statistic():
    path="E:/execution/data"
    dir=os.listdir(path)
    app_count=0
    review_count=0
    for d in dir:
        path_file=path+"/"+d
        file=open(path_file)
        json_file=json.load(file)
        for app in json_file:
            app_count=app_count+1
            for k in app.keys():
                val=app[k]
                review_count=review_count+len(val)
            # val=key[key.keys()]
            # review_count=review_count+len(val)
        file.close()
    print "App:",app_count,"Reviews:",review_count


# 将ReviewSelection阶段输出的多个存放在review_data 中的小数据文件合并在一个文件中，输出到BTM模型
#review_id.json 合并后卫文件app的review的index   格式{"app_id":[index1,index2]}
# merge.txt  合并后的文本文件
# review_id.txt：合并后的review的index，格式为(index:app_id)
def merge_review_data(path_dir):
    dir = os.listdir(path_dir)
    merge_file_url="../merge_data/merge.txt"
    review_id_url="../merge_data/review_id.txt"
    merge_file=open(merge_file_url,'w')
    review_file=open(review_id_url,'w')

    line_number=0
    for path in dir:
        file_path=path_dir+"/"+path
        file=open(file_path)
        file_json=json.load(file)
        for app_id in file_json.keys():
            review_app=file_json[app_id]
            review_id=[]
            for item in review_app:
                review_file.write(str(line_number)+" "+app_id+"\n")
                # review_id.append(line_number)
                line_number=line_number+1
                merge_file.write(item.strip()+"\n")


    review_file.close()
    merge_file.close()

if __name__ == '__main__':
    # review_data()
    reload(sys)
    sys.setdefaultencoding('utf-8')
    merge_review_data("../review_data")

    # review_data_statistic()
    # raw_data_statistic()
