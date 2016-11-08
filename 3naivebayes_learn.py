import json
import konlpy
from nltk.tokenize import word_tokenize
from nltk.classify import accuracy,naivebayes
from nltk.probability import ProbDistI
import random; import pickle
import _pickle as cpickle
import time



##########################READ list of news_featurset######################### 
def read_json(fname):
    with open(fname, encoding='cp949') as data_file:
        json_data = json.load(data_file)
    return json_data

##############################PROCESSING DATA##########################
def naive_train(featuresets):
    #belongs_to : Main
    #Role : Learning by naive bayes rule
    #Parameter : list featuresets([{'단어':True',...},'pol'])
    #Return : object classifier(nltk naivebayesclassifier object),
    #               list test_set(the featuresets that are randomly selected)
    random.shuffle(featuresets)
    train_set, test_set = featuresets[1000:], featuresets[:1000]
    classifier = naivebayes.NaiveBayesClassifier.train(train_set)

    return classifier,test_set

####################################SAVE################################
def save_classifier(classifier,fname):
    #belongs_to : Main
    #Role : save object that are made from naive_train
    #Parameter : list featuresets([{'단어':True',...},'pol'])
    #Return : None(just save pickle)
    with open(fname,'wb') as savedata:
       pickle.dump(classifier,savedata)
    #with open('naive_classifierc.pickle','wb') as savedata:
    #    cpickle.dump(classifier,savedata)


####################################TEST################################
def change_form_of_sentence(sentence):
    twitter = konlpy.tag.Twitter()

    list_of_splited_word = twitter.morphs(sentence)
    list_of_up_two_word = [word for word in list_of_splited_word if len(word)>1]
    dict_of_featuresets = {word : True for word in list_of_up_two_word}
    print(dict_of_featuresets)
    
    return dict_of_featuresets


def determine_category(dict_of_featuresets,list_of_catageory):
    category = classifier.classify(dict_of_featuresets)
    probdist = classifier.prob_classify(dict_of_featuresets)
    list_of_probability = [(probdist.prob(cat),cat) for cat in list_of_catageory]
    
    return category,list_of_probability



def test(classifier,sentence):
    dict_of_featuresets = change_form_of_sentence(sentence)
    list_of_catageory = classifier.labels()
    category,probability = determine_category(dict_of_featuresets,list_of_catageory)

    return category,probability




if __name__==__main__:
    #READ
    start_time = time.time()
    fname = 'all_news_word_featuresets_changed_cat_ver.json'
    featuresets = read_json(fname)
    print("--- %s seconds ---" % (time.time() - start_time))

    start_time = time.time()
    #PROCESSING DATA
    classifier,test_set = naive_train(featuresets)
    print("DONE \n" + str(accuracy(classifier, test_set)))
    print("--- %s seconds ---" % (time.time() - start_time))

    start_time = time.time()
    #SAVE
    fname = "naive_classifier3_change_category.pickle"
    save_classifier(classifier,fname)
    print("--- %s seconds ---" % (time.time() - start_time))

    #TEST
    sentence = "최고존엄 훼손...오바마 떠나기전 백악관 없어질 것"
    category,probability = test(classifier,sentence)


#deprecated
def change1(data):
    #belongs_to : Main
    #Role : Change data from small cat to big cat
    #Parameter : list featuresets([{'단어':True',...},'politic'])
    #Return : list featuresets([{'단어':True',...},'pol'])
    #U need to load 'all_news_word_featuresets.json' file
    for one_data in data:
        if (one_data[1][0:3] == 'sci' or one_data[1][0:3] == 'iit'): category = 'sit'
        else: category = one_data[1][0:3]
        one_data[1] = category

    return data

#deprecated
def change2(data):
    #belongs_to : Main
    #Role : make data's number small
    #Parameter : list featuresets([{'단어':True',...},'politic'])
    #Return : list featuresets([{'단어':True',...},'pol'])
    small_data = []
    a = 0
    
    for one_data in data:
        a += 1
        if a%10==0: small_data.append(one_data)

    return small_data

#deprecated
def save(data,fname):
    with open(fname, 'w') as f:
         json.dump(data, f)

 
