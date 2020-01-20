# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 01:32:33 2019

@author: Prathamesh
"""

# -*- coding: utf-8 -*-
import requests
from datetime import date, timedelta

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


# Sample URL
#
# http://content.guardianapis.com/search?from-date=2016-01-02&
# to-date=2016-01-02&order-by=newest&show-fields=all&page-size=200
# &api-key=your-api-key-goes-here

MY_API_KEY = open("creds_guardian.txt").read().strip()
API_ENDPOINT = 'http://content.guardianapis.com/search'
my_params = {
    'from-date': "",
    'to-date': "",
    'order-by': "newest",
    'show-fields': 'all',
    'page-size': 200,
    'api-key': MY_API_KEY
}

databaseName = "Trenddit"
collectionName = "guardian"
collection = pythonConnectDB(databaseName, collectionName)

# day iteration from here:
# http://stackoverflow.com/questions/7274267/print-all-day-dates-between-two-dates
start_date = date(2019, 10, 26)
end_date = date(2019,10, 29)
dayrange = range((end_date - start_date).days + 1)
for daycount in dayrange:
    dt = start_date + timedelta(days=daycount)
    datestr = dt.strftime('%Y-%m-%d')
    # then let's download it
    print("Downloading", datestr)
    all_results = []
    my_params['from-date'] = datestr
    my_params['to-date'] = datestr
    current_page = 1
    total_pages = 1
    while current_page <= total_pages:
        print("...page", current_page)
        my_params['page'] = current_page
        resp = requests.get(API_ENDPOINT, my_params)
        data = resp.json()
        all_results.extend(data['response']['results'])
        # if there is more than one page
        current_page += 1
        total_pages = data['response']['pages']
    collection.insert_one(data)
'''
        with open(fname, 'w') as f:
            print("Writing to", fname)

            # re-serialize it for pretty indentation
            f.write(json.dumps(all_results, indent=2))
'''