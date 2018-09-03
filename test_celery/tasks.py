from __future__ import absolute_import
from test_celery.celery import app
import time,requests
from pymongo import MongoClient
from bson.objectid import ObjectId
import pymongo
#from bs4 import BeautifulSoup

#client = MongoClient('10.1.1.234', 27017) # change the ip and port to your mongo database's
client = MongoClient('database', 27017) # change the ip and port to your mongo database's

db = client["arquivopt"]

@app.task(bind=True,default_retry_delay=10) # set a retry delay, 10 equal to 10s
def longtime_add(self,url):
    print 'long time task begins'
    try:
        print("task.requesting",url)
        r = requests.get(url)
        html_doc = r.text
        
        db["crawled_urls"].insert({ "url":url, 
                                    'html':html_doc, 
                                    'status':r.status_code,
                                    "timestamp":time.time()}) # store status code and current time to mongodb

     #   db["urls"].update_one({'_id': ObjectId(_id)},
     #       {'$set': {"url":url,"crawled":True}})

        print 'long time task finished'
    
    #except pymongo.errors.DuplicateKeyError:
        # skip document because it already exists in new collection
    #    pass
    
    except Exception as exc:
     #   raise self.retry(exc=exc)
        pass
    
    #return r.status_code
    return 'ok'
