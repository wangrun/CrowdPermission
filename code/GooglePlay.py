# -*- coding:utf-8 -*-

# 处理Google Play的metadata信息，将离散的文件提取permission和description的信息综合到一个文件中

import os
import sys
import json



# 根据路径返回特定app的ID、权限和描述数据等
def write(path):
    file=open(path)
    f=json.load(file)
    description=""
    permissions=[]
    if "docid" not in f.keys():
        return "",permissions,description
    docid=f["docid"]
    if "details" not in f.keys():
        return docid,permissions,description
    details=f["details"]
    app_details=details["app_details"]

    if "permission" in app_details.keys():
        permissions=app_details["permission"]

    if "description_html" in f.keys():
        description=f["description_html"]

    file.close()
    return docid,permissions,description



def get_permission_descs():
    # root_path="C:/Users/Eric/Desktop/metadata"
    num=0
    line=1
    root_path="I:/Google Play/metadata"
    output_path="C:/Users/Eric/Desktop/output"
    file_dirs=os.listdir(root_path)
    for file_dir in file_dirs:
        apps_path=root_path+"/"+file_dir
        out_put_file_path=output_path+"/"+file_dir+".json"
        # print out_put_file_path
        apps=os.listdir(apps_path)
        contents={}
        for app_id in apps:
            app_id_path=apps_path+"/"+app_id
            # print app_id_path
            c=write(app_id_path)
            val=[]
            val.append(c[1])
            val.append(c[2])
            contents[c[0]]=val
            if line%100==0:
                print line/100
            line=line+1
        json_new = open(out_put_file_path,'w+')
        json.dump(contents,json_new)
        json_new.close()
        print "finished:",num
        num=num+1



def get_permission_desc():
    # root_path="J:/Google Play/metadata"
    root_path="C:/Users/Eric/Desktop/metadata"
    path_output="C:/Users/Eric/Desktop/output"
    dirs=os.listdir(root_path)
    for dir in dirs:
        lis_dir=root_path+"/"+dir
        app_dir=os.listdir(lis_dir)
        contents={}
        path_output=path_output+"/"+dir+".json"
        print "output:",path_output
        # print app_dir
        for app_id in app_dir:
            # prin
            path=lis_dir+"/"+app_id
            print "path:",path
            c=write(path)
            val=[]
            val.append(c[1])
            val.append(c[2])
            contents[app_id]=val

        # json_new=open(path_output,'w')
        # json.dump(contents,json_new)
        # json_new.close()


def main():
    # get_permission_desc()
    reload(sys)
    sys.setdefaultencoding('utf-8')
    get_permission_descs()



if __name__ == '__main__':
    main()
