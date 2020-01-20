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

url ='https://api.nytimes.com/svc/archive/v1/2019/7.json?api-key=t5iAd3WTx5bAdx1X2Pr987wYOHbEKHRJ'
#https://api.nytimes.com/svc/archive/v1/2019/7.json?api-key=t5iAd3WTx5bAdx1X2Pr9    87wYOHbEKHRJ
r= requests.get(url)
json_data=r.json()

databaseName = "Trenddit"
collectionName = "NYTimes"
collection = pythonConnectDB(databaseName, collectionName)
json_data['response']['docs'] = json_data['response']['docs'][0:3000]

collection.insert_one(json_data)
