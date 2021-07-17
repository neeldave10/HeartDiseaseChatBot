import nltk
from newspaper import Article
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
import numpy as np
warnings.filterwarnings('ignore')
import ssl

try:
    _create_unverified_https_context=ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context=_create_unverified_https_context

nltk.download('punkt',quiet=True)

article=Article('https://www.mayoclinic.org/diseases-conditions/heart-disease/symptoms-causes/syc-20353118')
article.download()
article.parse()
article.nlp()
corpus=article.text
#print(corpus)

sentence_list=nltk.sent_tokenize(text=corpus)
#print(sentence_list)

#Greeting
def greeting(text):
    text=text.lower()

    bot_greeting=['hello','hey, how you doing','heya','hola','hi']

    user_greeting=['hello','hey, how you doing','heya','hola','hi','hey']

    for word in text.split():
        if word in user_greeting:
            return random.choice(bot_greeting)

def index_sort(list_var):
    length=len(list_var)
    list_index=list(range(0,length))

    x=list_var
    for i in range (length):
        for j in range (length):
            if x[list_index[i]]>x[list_index[j]]:
                temp=list_index[i]
                list_index[i]=list_index[j]
                list_index[j]=temp
    return list_index

def bot_response(user_input):
    user_input=user_input.lower()
    sentence_list.append(user_input)
    bot_response=''
    cm=CountVectorizer().fit_transform(sentence_list)
    similarity_scores=cosine_similarity(cm[-1],cm)
    similarity_scores_list=similarity_scores.flatten()
    index=index_sort(similarity_scores_list)
    index=index[1:]
    response_flag=0

    j=0
    for i in range(len(index)):
        if similarity_scores_list[index[i]]>0.0:
            bot_response=bot_response+''+sentence_list[index[i]]
            response_flag=1
            j=j+1
        if j>2:
            break

    if response_flag==0:
        bot_response=bot_response+''+"Sorry,I don't understand"

    sentence_list.remove(user_input)
    return bot_response

def run():
    print('Hey, I am your first aid medic bot, Ask me anything about any disease you want to know about and i will help you with answering everything I know')

    exit_list=['bye','thanks','thank you','good bye','see you later','quit']

    while(True):
        user_input=input()
        if user_input.lower() in exit_list:
            print("I will miss taking to you!!Bye Bye")
            break
        else:
            if greeting(user_input)!=None:
                print( greeting(user_input))
            else:
                print( bot_response(user_input))

run()




