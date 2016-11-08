import json
import re
import konlpy

#belongs_to :
#Role :
#Parameter :
#Return :

if __name__=='__main__':
    #READ
    fname = 'all_news_del_under1000.json'
    dic_of_big_cat = read_json(fname)
    #PROCESSING DATA
    featuresets = split_and_count_word(dic_of_big_cat)
    #SAVE
    fname = 'all_news_word_featuresets.json'
    save(featuresets,fname)
    
def read_json(fname):
    #belongs_to : Main
    #Role : Read json file(dict of content ex.{'politic':{'청와대': [기사,기사]}..})
    #Parameter : str fname(file name)
    #Return : dictionary json_data(dict of content ex.{'politic':{'청와대': [기사,기사]}..})
    with open(fname, encoding='cp949') as data_file:
        json_data = json.load(data_file)
    return json_data

def change(data):
    #Deprecated
    #belongs_to : Main
    #Role : 기사 개수 맞추기(100개로)
    #Parameter : dictionary data(dict of content ex.{'politic':{'청와대': [기사,기사]}..})
    #Return : None
    for bg in data:
        for sm in data[bg]:
            del data[bg][sm][1000:]

    with open('all_news_del_under1000.json', 'w') as f:
         json.dump(data, f)
         
def split_and_count_word(data):
    #belongs_to : Main
    #Role : 뒷부분 기자 광고글 빼고 konlpy로 단어 쪼개서 2단어 이상 featureset(단어:True) 만들기. 
    #Parameter : dictionary data(dict of content ex.{'politic':{'청와대': [기사,기사]}..})
    #Return : list featuresets([{'단어':True',...},'politic']=featureset + category)
    
    featuresets = []
    twitter = konlpy.tag.Twitter()

    for big_cat in data:

        for small_cat in data[big_cat]:
            #save category name needed in featuresets 
            category = str(big_cat[0:3])+'/'+str(small_cat)
            count = 0; print(small_cat)
            for one_news in data[big_cat][small_cat]:
                count+=1
                if count%100==0: print(count,end=' ')                
                #split word as using konlpy/one_news is list in list so open it!
                doc = one_news[0][0]
                list_of_splited_word = twitter.morphs(doc[:-63])#기자,광고글 
                #get word length is higher than two and get list of splited words
                list_of_up_two_word = [word for word in list_of_splited_word if len(word)>1]
                dict_of_featuresets = make_featuresets(list_of_up_two_word)
                #save 
                featuresets.append((dict_of_featuresets,category))
                
    return featuresets


#make featureset that said in nltk doc.
def make_featuresets(data):
    #belongs_to : split_and_count_word
    #Role : 단어  featureset 만들기
    #Parameter : list list_of_up_two_word(ex.['비누','떨어','지다']
    #Return : dictionary {word : True for word in data}
    
    #PROBLEM 수정필요
    #cannot consider the freqency of word
    #(BUT the test sample isn't long,so there would not be a problem)
    return {word : True for word in data}


def save(data,fname):
    with open(fname, 'w') as f:
         json.dump(data, f)



