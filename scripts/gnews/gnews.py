import urllib.request as url
import datetime

# user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'

# # header variable
# headers = { 'User-Agent' : user_agent }

# # creating request
# req = url.Request(gUrl, None, headers)

# page = url.urlopen(req).read().decode('utf-8')

# # body = re.findall(r'/<body[^>]*>(.*?)<\/body>/is', html)

# # print(body[0:1000])

#
#class RelatedArticleClass:
#    def __init__(self, url, time, source, text):
#       self.url = url
#       self.time = time
#       self.source = source
#       self.text = text
#
#class NewsArticleClass:
#    def __init__(self, text, relatedArticles):
#       self.text = text
#       self.relatedArticles = relatedArticles



# for parsing string to date format
def convertDateToJson( date ):
    from dateutil import parser as dateParser
    import datetime
    if isinstance( date, str):
        date = dateParser.parse(date)
    if isinstance(date, datetime.datetime):
        return date.__str__()

# string utils
def removeMinWordsFromListOfString( listSring , noOfWords = 1):
    return  ' '.join([ eachLine for eachLine in listSring if len(str(eachLine).split()) > noOfWords])

# Mongo db utils
# python -> mongo connect
def pythonConnectDB( databaseName, collectionName):
    import pymongo
    myClient = pymongo.MongoClient("mongodb://localhost:27017/")
    myDB = myClient[databaseName]
    dbList = myClient.list_database_names()
    if databaseName in dbList:
        print(databaseName + " database exists.")
    else:
        raise ValueError(databaseName + " database does not exist")
    if isinstance(collectionName, list):
        return [ myDB[eachCollection] for eachCollection in collectionName] 
    return myDB[collectionName]


def gNewsCrawl(gNewsUrl):
    from lxml import html
    import requests

#    session = requests.Session()  # so connections are recycled

    page = requests.get(gNewsUrl).content
    tree = html.fromstring(page)

    outputNewsArr = []
    news = tree.xpath('.//*[@class="xrnccd"]')
    relatedNewsHtml =  tree.xpath('.//*[@class="SbNwzf"]')
    for index, relatedNews in enumerate(relatedNewsHtml):
        aggregatedText = ''
        articles = relatedNews.xpath('.//article')
        firstNews = relatedNews.xpath('./parent::*/article')[0]
        txt = firstNews.xpath('.//text()')
        txt = removeMinWordsFromListOfString(txt)
        aggregatedText += txt + "."
        articles.append(firstNews)
        relatedArticles = []
        for eachArticleIndex, eachArticle  in enumerate(articles):
            href = eachArticle.xpath('./*[@class="VDXfz"][1]/@href')[0]
    #        resp = session.head(baseGUrl +href[2:], allow_redirects=True)
    #        print(resp.url)
            time = convertDateToJson(eachArticle.xpath('.//time[1]/@datetime')[0])
            source = eachArticle.xpath('.//*[@class="SVJrMe"][1]/a[1]')[0].text_content()
            text  = eachArticle.xpath('.//text()')
            text = removeMinWordsFromListOfString(text)
            aggregatedText += text + "."
            relatedArticles.append({
			"index": eachArticleIndex,
                        "href": href,
                        "time": time,
                        "source": source,
                        "text:": text,
                    })
        outputNewsArr.append({
                "text": txt, 
                "relatedArticles": relatedArticles,
                "AggregatedText" : aggregatedText
                })

    json_data ={
            "news": outputNewsArr,
            "scriptTime": convertDateToJson(datetime.datetime.now())
            }


    print("text : " + str(outputNewsArr[0]['text']))

    print("Done")
    return json_data



def scheduleJob():
    from apscheduler.schedulers.blocking import BlockingScheduler
    
    databaseName = "Trenddit"
    collectionName = "gnews"
    listOfCountries = ['US', 'IN', 'CA', 'IL','GB', 'PK', 'SG', 'AU']
    collection = pythonConnectDB(databaseName, [ collectionName + "_" + eachCountry  for eachCountry in listOfCountries])

    def saveGNewsData():
        print ("job Started")
        # USA, INDIA, CANADA, Israel, England, Pakistan, Singapore, Australia

        dumpData = {
            "version" : 1,
            "scriptTime": convertDateToJson(datetime.datetime.now())
        }
        print("parsing each countries data")
        for index in range(len(listOfCountries)):
            eachCountry = listOfCountries[index]
            print(eachCountry)
            json_data = gNewsCrawl("https://news.google.com/?hl=en-" + eachCountry + "&gl=" + eachCountry + "&ceid=" + eachCountry + ":en")
            dumpData[eachCountry] = json_data
            collection[index].insert_one(dumpData)
        print ("job Ended")

    scheduler = BlockingScheduler()
    scheduler.add_job(saveGNewsData, 'interval',  minutes=1)
    scheduler.start()

scheduleJob()
