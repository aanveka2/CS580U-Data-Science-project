# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 12:39:23 2019

@author: krupa
"""
import requests

def pythonConnectDB( databaseName, collectionName):
    import pymongo
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient[databaseName]
    dblist = myclient.list_database_names()
    if databaseName in dblist:
        print(databaseName + " database exists.")
    else:
        raise ValueError(databaseName + " database does not exist")
    return mydb[collectionName] 



#ARTICLES_DIR = join('tempdata', 'articles')
#makedirs(ARTICLES_DIR, exist_ok=True)

url ='https://api.nytimes.com/svc/mostpopular/v2/viewed/30.json?api-key=t5iAd3WTx5bAdx1X2Pr987wYOHbEKHRJ'
#https://api.nytimes.com/svc/archive/v1/2019/7.json?api-key=t5iAd3WTx5bAdx1X2Pr987wYOHbEKHRJ
r= requests.get(url)
json_data=r.json()

databaseName = "Trenddit"
collectionName = "NYTimes_mostviewed30D"
collection = pythonConnectDB(databaseName, collectionName)


collection.insert_one(json_data)
