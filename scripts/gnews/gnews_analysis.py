#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 12:39:11 2019

@author: prathamesh
"""

# Libraries for text preprocessing
import re
import nltk
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
#nltk.download('wordnet') 
from nltk.stem.wordnet import WordNetLemmatizer

stop_words = set(stopwords.words("english"))

def removeUselessWords(data):
    corpus = []
    #Remove punctuations
    text = re.sub('[^a-zA-Z]', ' ', data)
    
    #Convert to lowercase
    text = text.lower()
    
    #remove tags
#        text=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)
    
    # remove special characters and digits
#        text=re.sub("(\\d|\\W)+"," ",text)
    
    ##Convert to list from string
    text = text.split()
#    print(len(text))
    ##Stemming
#        ps=PorterStemmer()    #Lemmatisation
    lem = WordNetLemmatizer()
    text = [lem.lemmatize(word) for word in text if not word in stop_words] 
    text = " ".join(text)
    corpus.append(text)
    return corpus

import json
gnews = []
with open('../../../gnews.json') as f:
    for line in f:
        gnews.append(json.loads(line))
        
oneNews = gnews[0]


meta = []
hashArray = []

newsSource = {}
noOfSubNews = 0
for i,eachQuery in enumerate([elem for i,elem in enumerate(gnews )if i%60 == 0]):
    tempHash = []
    for j,eachNews in enumerate(eachQuery['news']):
        tempMeta = []
        aggText = ''
        aggText = eachNews['text']
        for k,eachSubNews in  enumerate(eachNews['relatedArticles']):
#            print(eachSubNews['text:'])
            aggText += eachSubNews['text:']
#            newsKey = '_'.join(eachSubNews['source'].split())
            newsKey = eachSubNews['source']
            noOfSubNews = noOfSubNews + 1
            if newsKey in newsSource :
                newsSource[newsKey] = int( newsSource[newsKey]) + 1
            else:
                newsSource[newsKey] = 1
       
        aggTextKeywords = removeUselessWords(aggText)[0]
        
        hashOfWords = hash(aggTextKeywords)
        tempHash.append(hashOfWords)        
        tempMeta.append({
                    'aggText': aggText,
                    'aggTextKeywords': aggTextKeywords,
                    'hash' : hashOfWords
                })
    
    tempHash.reverse()
    hashArray.append(tempHash)
    meta.append(tempMeta)
        
reverseHash = {}
for i in hashArray:
    for j in i:
        reverseHash[j] = 50
        
plotData = []
for elem in hashArray:
    tempPlotData = []
    for i in list(reverseHash):
        if i in elem:
            tempPlotData.append(elem.index(i))
        else:
            tempPlotData.append(50)
    plotData.append(tempPlotData)
    
import matplotlib.pyplot as plt
plt.ylim([0,25])
plt.plot(plotData[0:5])
plt.savefig('newsTrends.png', dpi = 300)
plt.close()


newsSourceGraphData = [[i, newsSource[i]] for i in list(newsSource)]
newsSourceGraphData.sort(key=lambda x: x[1], reverse = 1)
newsSourceGraphData = newsSourceGraphData[0:30]
import numpy as np

y_pos = np.arange(len(newsSourceGraphData))
plt.bar(y_pos, [ i[1]for i in newsSourceGraphData], align='center', alpha=0.5)
plt.xticks(y_pos,  [ i[0]for i in newsSourceGraphData])
plt.xticks( rotation=45,
    horizontalalignment='right',
    fontweight='light',
    fontsize='xx-small')
plt.ylabel('No of occurrence')
plt.title('News Channels')
#plt.show()
plt.savefig('newsSourceOccurence.png', dpi = 300, bbox_inches='tight')
plt.close()
