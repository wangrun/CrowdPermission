# -*- coding:utf-8 -*-

# 扩充字典的语义，利用wordnet(NLTK提供)
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords


def word_similar(phrase):
    set_hyper=[]
    set_hypon=[]
    all_dic=set()

# 抓取同义词集合
    phrases=wn.synsets(phrase)
    # print type(phrase)
    if len(phrases)==0:
        return
    else:
        for item in phrases:
            all_dic.add(item.lemmas()[0].name())

    # 上位词集合
    words_hypernyms=phrases[0].hypernyms()
    # print type(words_hypernyms)
    if len(words_hypernyms)!=0:
        for item in words_hypernyms:
            set_hyper.append(item.lemmas()[0].name())
    else:
        pass

    # 下位词集合
    words_hyponyms=phrases[0].hyponyms()
    # print type(words_hyponyms)
    if len(words_hyponyms)!=0:
        for item in words_hyponyms:
            set_hypon.append(item.lemmas()[0].name())
    else:
        pass

    return set_hyper+set_hypon+list(all_dic)


# 停用词
def stopword(word):
    stop=stopwords.words('english')
    words=[]
    for w in word:
        if w not in stop:
            words.append(w)
    return words

def input(path):
    file = open(path)
    map={}
    line_num=1
    permission=""
    word_list=""
    for line in file:
        if line_num%2==1:
            permission=line.strip()
        else:
            word_list=line.strip()
            lists=[]
            for word in word_list.split(','):
                if ' ' in word:
                    space=word.split(' ')
                    lists=lists+stopword(space)
                else:
                    lists.append(word)
            map[permission]=lists
        line_num=line_num+1
    file.close()
    return map


# 返回字典，key：permission_name，value：单词列表
def output(input_path):
    map_dic=input(input_path)
    map_dics={}
    for item in map_dic.keys():
        permission_name=item
        word_list=map_dic[item]
        words=[]
        for w in word_list:
            contents=word_similar(w)
            if contents is not None:
                words=words+contents
        words=words+word_list
        map_dics[permission_name]=words
    # print map_dics.keys()
    
    return map_dics


if __name__ == '__main__':
    # expansion_dic()
    # map=input("../data/dictionary")
    # print map.keys()
    # for item in map.keys():
    #     print item,map[item]
    output("../data/dictionary")
