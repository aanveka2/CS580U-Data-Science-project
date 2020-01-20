import requests
import json
import datetime
from os.path import join, exists
from datetime import date, timedelta
from urllib.request import urlopen
import math

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
collectionName = "newsapi"
collection = pythonConnectDB(databaseName, collectionName)

#top_headlines_url = 'https://newsapi.org/v2/top-headlines'
everything_news_url = 'https://newsapi.org/v2/everything'

headers ={'Authorization' : 'ae1b243f56474b719185f6f51783cfa2'}

everything_payload = {'q': '', 'language': 'en','source': '', 'sortBy': 'publishedAt','pageSize': 100,'from_param'
                      :'',
                     'to':''}

start_date = date(2019, 10, 29)
end_date = datetime.date.today()
dayrange = range((end_date - start_date).days + 1)
for daycount in dayrange:
    dt = start_date + timedelta(days=daycount)
    datestr = dt.strftime('%Y-%m-%d')
    #fname = join(ARTICLES_DIR, datestr + '.json')
    everything_payload['from_param'] = datestr
    everything_payload['to'] = datestr
    keyword = ["sports","business","entertainment","health","technology","science"]
    for q in keyword:                     
        everything_payload['q'] = q
        sources = ["bbc-news","cnn","the-hindu"]
        for source in sources:
            everything_payload['sources'] = source
            print("sources :" + source)
            response = requests.get(url=everything_news_url, headers=headers, params=everything_payload)
            print("q :" + q)
            #print(response.json())
            data_1 = response.json()
            data_2 = json.dumps(data_1)
            data_3 = json.loads(data_2)
            #for articles in data_3.items:
            #print(data_3['articles'][0]['content'])
            for i,eachElem in enumerate(data_3['articles']):
                if eachElem['content']:
                #print(eachElem['content'].split('…')[0])
                    eachElem['content'] = eachElem['content'].split('…')[0]
                
                print(datestr)
            #print(data_3)
            #total_pages = (data_1['totalResults']/100)
            collection.insert_one(data_3)
            
'''
with open(fname, 'w') as f:
    print("Writing to", fname)

        # re-serialize it for pretty indentation
    f.write(json.dumps(data_3, indent=2, ensure_ascii=False))
'''
