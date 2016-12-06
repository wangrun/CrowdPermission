# -*- coding: utf-8 -*-


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
