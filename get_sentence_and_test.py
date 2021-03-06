import pickle; import time
from nltk.classify import accuracy,naivebayes; from nltk.probability import ProbDistI
import konlpy
import requests; from bs4 import BeautifulSoup

class Guess:
    def __init__(self, fname):
        start_time = time.time()
        print("It would take about 20 sec")
        with open(fname,'rb') as loaddata:
            self.classifier = pickle.load(loaddata)
        print("load_pickle.")
        print("--- %s seconds ---" % (time.time() - start_time))

    def by_sentence(self, sentence):
        #belongs_to : Main
        #Role : guess category by using naivebayes classifier
        #Parameter : str sentence
        #Return : str category, list proabability(ex.[(0.95,'sci'),..])
       
        category,probability = test(self.classifier,sentence)
        print("guessing category DONE")
        category,probability = korean(category,probability)

        #필요한 category index 검색해서 확률 뽑아오기
        one_category_index = [cat for prob,cat in probability].index(category)
        one_probability = probability[one_category_index][0]
        print(category+"일 확률 "+str(one_probability)+'%')
        return category,probability
    
    def by_url(self, url):
        #belongs_to : Main
        #Role : guess category by using naivebayes classifier
        #Parameter : list url_list(ex.['http://www.naver.com']
        #Return : object classifier(nltk naivebayesclassifier object),
       
        if len(url)==0: #url이 없는 경우
            print("url이 없습니다. 아무것도 return 되지 않습니다.")
            return "",""
        else:
            #print(url)
            sentence = spider(url)
            if len(sentence)<5 :
                print("글이 충분치 않습니다. 아무것도 return 되지 않습니다.")
                return "",""
            category,probability = test(self.classifier,sentence)
            print("guessing category DONE")
            category,probability = korean(category,probability)
        
        one_category_index = [cat for prob,cat in probability].index(category)
        one_probability = probability[one_category_index][0]
        print(category+"일 확률 "+str(one_probability)+'%')

        return category,probability


#########################Function######################################
def spider(url):
    #belongs_to : Anywhere, guess_by_url,guess_by_url_list.
    #Role : get title and content in url
    #Parameter : url
    #Return : str title, str content

    #get page
    try:
        source_code = requests.get(url)
    except:#400 error
        print("없는 페이지 입니다. 아무것도 return 되지 않습니다.")
        return "",""
    
    text = source_code.text
    soup  = BeautifulSoup(text,"lxml")
    
    #delete script tag content
    for script in soup.findAll('script'):
        script.extract()
    
    #title
    try:
        if soup.find(property = 'og:title'):
            title = str(soup.title.string)+ str(soup.find(property = 'og:title')['content'])
        else:
            title = soup.title.string
    except:#없는 페이지
        print("없는 페이지 입니다. 아무것도 return 되지 않습니다.")
        title = ""
        
    #content
    try:
        body_descendant = soup.body.descendants
        content = ""
        for one_para in body_descendant:
            if  one_para.string ==None: continue
            if len(one_para.string)>60: content += one_para.string
    except:
        content = ""
        
    sentence = str(title) + str(content)
    
    return sentence

def test(classifier,sentence):
    #belongs_to : Anywhere, by_url,guess_by_url_list.guess_by_sentence
    #Role : 카테고리 고르기 main
    #Parameter : object classifier(nltk naivebayesclassifier object), str sentence
    #Return : str category,  list proabability(ex.[(0.95,'sci'),..])
    
    dict_of_featuresets = change_form_of_sentence(sentence)
    list_of_catageory = classifier.labels()
    category,probability = determine_category(classifier,dict_of_featuresets,list_of_catageory)

    return category,probability

def change_form_of_sentence(sentence):
    #belongs_to : test
    #Role : konlpy 분석 후 featureset 생성
    #Parameter : str sentence
    #Return : dictionary dict_of_featuresets{'단어':True',...}
    twitter = konlpy.tag.Twitter()

    list_of_splited_word = twitter.morphs(sentence)
    list_of_up_two_word = [word for word in list_of_splited_word if len(word)>1]
    dict_of_featuresets = {word : True for word in list_of_up_two_word}
    #print(dict_of_featuresets)
    
    return dict_of_featuresets

def determine_category(classifier,dict_of_featuresets,list_of_catageory):
    #belongs_to : test
    #Role : 카테고리 고르기
    #Parameter : object classifier(nltk naivebayesclassifier object),
    #                    dictionary dict_of_featuresets{'단어':True',...}
    #                    list list_of_category = ['soc','sci'...]
    #Return : str category, list proabability(ex.[(0.95,'sci'),..])
    
    category = classifier.classify(dict_of_featuresets)
    probdist = classifier.prob_classify(dict_of_featuresets)
    list_of_probability = [(round(probdist.prob(cat),2)*100,cat) for cat in list_of_catageory]
    
    return category,list_of_probability

def guess_by_url_list(self,classifier,url_list):
    #belongs_to : Main
    #Role : get category list by using naivebayes classifier
    #Parameter : object classifier(nltk naivebayesclassifier object), list url_list(ex.['http://www.naver.com'...])
    #Return : list category_list(ex.['sci','soc'])
    category_list = []
    for url in url_list:
        category,probability = guess_by_url(classifier, url)
        category_list.append(category)
    
    print("guessing category DONE")
    return category_list


def korean(category,probability) :
    k_category = {'soc' : '사회','lif':'생활','wor':'세계','pol':'정치','eco':'경제','sit':'IT/과학'}
    k_probability = [(prob,k_category[cat]) for prob,cat in probability]

    return k_category[category],k_probability
