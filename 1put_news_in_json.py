import json

if __name__ == '__main__':
    dic_of_big_cat = write_big_cat()
    save(dic_of_big_cat)

def write_big_cat():
    #belongs_to : Main
    #Role : 소분류/대분류로 된 json 읽어와서 한  dictionary로 리턴하기
    #Parameter : None
    #Return : dictinary  dic_of_bic_cat(ex.{'politic':{'청와대': [기사,기사]}})
    dic_of_big_cat = {}
    small_cat_name = {'politic' : ['청와대','국회','북한','행정','국방외교','정치일반'],
                                      'economy' : ['금융','증권','산업재계','중기벤처','부동산','글로벌경제','생활경제','경제일반'],
                                      'society' : ['사건사고','교육','노동','언론','환경','인권복지','식품의료','지역','인물','사회일반'],
                                      'life' : ['건강정보','자동차','도로교통','여행','음식','패션','공연','책','종교','날씨','생활일반'],
                                      'world' : ['세계'],
                                      'scit' : ['모바일','인터넷SNS','통신뉴미디어','IT일반','보안해킹','컴퓨터','게임','과학일반']}
    
    for i in range(6):
        small_cat_num = [6,8,10,11,1,8]
        big_cat_name = ['politic','economy','society','life','world','scit']
        dic_of_big_cat[big_cat_name[i]]= write_small_cat(small_cat_num[i],big_cat_name[i],small_cat_name[big_cat_name[i]])
        
    return dic_of_big_cat

#function in the write_big_cat()
def write_small_cat(num,big_name,small_name):
    #belongs_to : write_bic_cat()
    #Role : json 파일 읽어와서 한 대분류 dictionary 리턴하기
    #Parameter : int num(number of small category in one big category),
    #                    str big_name(ex.'politic'),str_list small_name(['청와대','국회'..]))
    #Return :dictionary dic_of_small_cat(ex.{'청와대': [기사,기사]})
    
    dic_of_small_cat = {}
        
    for i in range(num):
        #write file name
        fname = big_name + '_news' + str(i+1) + '.json'
        with open(fname, encoding='cp949') as data_file:
            #read json and write list into dictionary
            data = json.load(data_file)
            #write news contents in small_cat
            #small name is imported list that got from write big namep
            dic_of_small_cat[small_name[i]] = data
            
    return dic_of_small_cat

def save(data):
    with open('all_news.json', 'w') as f:
         json.dump(data, f)

#Deprecated
def parse_list(li):
    parse = ""
    for i in range(len(li)):
        parse += ":]" + li[i][0][0]
    return parse

    

