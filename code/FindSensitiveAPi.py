# -*- coding:utf-8 -*-

# 找出permission对应的sensitive api列表

def permission_list(path="../data/permission_list.txt"):
    permission_data=[]
    file=open(path)
    for line in file:
        permission_data.append(line.strip())
    file.close()
    return permission_data

def find_sensitiveAPI(path):
    file= open(path)
    permission_data=permission_list("../data/permission_list.txt")
    flag=False
    key=None
    value=[]
    map={}
    for line in file:
        if line.startswith("Permission"):
            permission_find=line[line.rindex(".")+1:].strip()
            if permission_find in permission_data:
                if key!=None:
                    map[key]=value
                    value=[]
                key=permission_find
                flag=True
            else:
                if key!=None:
                    map[key]=value
                key=None
                value=[]
                flag=False
        else :
            if flag and line.startswith("<"):
                value.append(line.strip())

    if key!=None:
        map[key]=value
    file.close()

    return map


# ../data/api
if __name__=="__main__":
    map=find_sensitiveAPI(path="../data/jellybean_publishedapimapping.txt")
    for key in map.keys():
        for value in map[key]:
            print key,":",value.strip()
