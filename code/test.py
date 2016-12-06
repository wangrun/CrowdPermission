# -*- coding: utf-8 -*-

# import sqlite3,sys
# conn=sqlite3.connect('C:/Users/Eric/Desktop/experiment/esalib-master/esalib-master/example/esa_en.db')
# cursor=conn.cursor()
# cursor.execute("select * from en_ndx limit 0,1")
# # x="muhi"
# # x.encode("utf-8")
# # sql="select * from en_terms where term=?"
# # cursor.execute(sql,(x))
# values=cursor.fetchall()
#
# for row in values:
#     # print row
#     sys.stdout.write("%s %s"%(row[0],row[1]))
#
# cursor.close()
# conn.close()


# s=['hekk','a','m','the','a']
# t=['a','the']
# print s.count(t)

import os
import json


# 找出二维列表中，每一列的最大值的，位置，返回其在列中的位置信息
# 返回的是每一个permission对应的topic
def get_max(arr):
    max_index=[]
    for i in range(0,len(arr[0])):
        col=[]
        for j in range(0,len(arr[0])):
            col.append(arr[j][i])
        max_value=max(col)
        max_index.append(col.index(max_value))
    return max_index


# 找出列表arrs中value的索引
def index_l(arrs,value):
    index_lists=[]
    for i in range(0,len(arrs)):
        if arrs[i]==value:
            index_lists.append(i)
    return index_lists

def iterate(arr):
    # value：topic_id
    max_index=get_max(arr)
    if len(max_index)==len(set(max_index)):
        return max_index
    else:
        for i in range(0,len(max_index)):
            if max_index.count(max_index[i])>1:
                index_lists=index_l(max_index,max_index[i])
                max=arr[max_index[i]][index_lists[0]]
                for index_per in range(0,len(index_lists)):
                    row=max_index[i]
                    col=index_lists[index_per]
                    if arr[row][col]>max:
                        max=arr[row][col]
                for index_per in range(0,len(index_lists)):
                    row=max_index[i]
                    col=index_lists[index_per]
                    if arr[row][col]<max:
                        arr[row][col]=0
                break
            else:
                continue
        iterate(arr)

def main():
    arr=[
    [1,4.1,3.9,4],
    [2,3,2,2],
    [3,2,4,3],
    [4,1,3,1]
    ]

    iterate(arr)
    print get_max(arr)

if __name__ == '__main__':
    s=range(0,4)
    print s
