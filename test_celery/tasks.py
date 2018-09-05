from __future__ import absolute_import
from test_celery.celery import app
import time,requests
from pymongo import MongoClient
from urlparse4 import urlparse
from datetime import datetime
#from bs4 import BeautifulSoup

#client = MongoClient('10.1.1.234', 27017) # change the ip and port to your mongo database's
client = MongoClient('database', 27017) # change the ip and port to your mongo database's

db = client["contamehistorias"]

#http://arquivo.pt/noFrame/replay/20080303034847/http://noticias.sapo.pt/lusa/artigo/6921150909eeac31a1a357.html

# extrair datetime
# domain
# url original
# url arquivo
# remover aspas duplas
@app.task(bind=True, default_retry_delay=10) # set a retry delay, 10 equal to 10s
def parse_url_archive(self, url):
    try:

        if("\"" in url):
            return
        
        original_url = url.replace("http://arquivo.pt/noFrame/replay/","")
        datetime_s = original_url.split("/")[0]
        original_url = original_url.split("/")[1:]
        original_url = "/".join(original_url)
        domain = urlparse(original_url).netloc
    
        pubdate = datetime.strptime(datetime_s, '%Y%m%d%H%M%S')        

        doc = {
            "domain":domain,
            "url":url,
            "original_url":original_url,
            "pubdate":pubdate
        }

        db["processed_urls"].insert(doc)

    except Exception as exc:
        raise self.retry(exc=exc)    




@app.task(bind=True, default_retry_delay=10) # set a retry delay, 10 equal to 10s
def extract_page_title(self, archived_url):
    try:

        html = archived_url["html"]

        start_title_tag = "<title>"
        end_title_tag = "</title>"

        start_title_tag_idx = html.find("<title>")
        end_title_tag_idx = html.find("</title>",start_title_tag)

        title = html[start_title_tag_idx + len(start_title_tag):end_title_tag_idx].strip()
        
        del archived_url["html"]
        archived_url["title"] = title

        db["url_titles"].insert(archived_url)

    except Exception as exc:
        raise self.retry(exc=exc)
        
@app.task(bind=True, default_retry_delay=10) # set a retry delay, 10 equal to 10s
def request_url(self, archived_url):
    try:

        r = requests.get(archived_url["url"])
        html_doc = r.text

        doc = archived_url
        doc["html"] = html_doc
        doc["pubdate"] = datetime.strptime(doc["pubdate"], '%Y-%m-%dT%H:%M:%S')
        db["url_contents"].insert(doc)
        
    except Exception as exc:
        raise self.retry(exc=exc)           


@app.task(bind=True, default_retry_delay=10) # set a retry delay, 10 equal to 10s
def longtime_add(self,url,id):
    print 'long time task begins'
    try:
        print("task.requesting",url)
        r = requests.get(url)
        html_doc = r.text
        
        db["crawled_urls"].insert({ "url":url, 
                                    'html':html_doc, 
                                    'status':r.status_code,
                                    "timestamp":time.time()}) # store status code and current time to mongodb

#        db["urls"].update_one({'_id':id},
#            {'$set': {"url":url,"crawled":True})

        print 'long time task finished'
    
    except pymongo.errors.DuplicateKeyError:
        # skip document because it already exists in new collection
        pass
    
    except Exception as exc:
        raise self.retry(exc=exc)    
