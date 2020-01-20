import requests
import json

'''
ARTICLES_DIR = join('tempdata', 'articles')
makedirs(ARTICLES_DIR, exist_ok=True)
'''

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

databaseName = "Trenddit"
collectionName = "newsapi_trending"
collection_countries = pythonConnectDB(databaseName, collectionName + '_countries')
collection_sources = pythonConnectDB(databaseName, collectionName + '_sources')

top_headlines_url = 'https://newsapi.org/v2/top-headlines'

headers ={'Authorization' : 'ae1b243f56474b719185f6f51783cfa2'}
payload = {'country': '','pageSize': 100}


countries = ["us","ca","au","in","gb","sg"]
for country in countries:
    payload['country'] = country
    response = requests.get(url=top_headlines_url, headers=headers, params=payload)
    print("country :" + country)
    resp = response.json()
    resp_dump = json.dumps(resp,indent=2, ensure_ascii=False)
    data = json.loads(resp_dump)
    data['country'] = country
    #print(data_3)
    
    for i,eachElem in enumerate (data['articles']):
        if eachElem['content']:    
            eachElem['content'] = eachElem['content'].split('…')[0]
    #print(data_3)
    collection_countries.insert_one(data)
    
    
payload ['country'] = ''
sources = ["bbc-news","cnn","the-hindu"]
for source in sources:
    payload['sources'] = source
    print("sources :" + source)
    response = requests.get(url=top_headlines_url, headers=headers, params=payload)
    
    resp = response.json()
    resp_dump = json.dumps(resp,indent=2, ensure_ascii=False)
    data = json.loads(resp_dump)
    data['source'] = source

    for i,eachElem in enumerate (data['articles']):
        if eachElem['content']:    
            eachElem['content'] = eachElem['content'].split('…')[0]
    #print(data)
    collection_sources.insert_one(data)
 