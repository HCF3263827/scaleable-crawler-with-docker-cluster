from .tasks import longtime_add
from .tasks import request_url
from .tasks import parse_url_archive
from .tasks import preprocess_and_download_url

import sys
import time
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('database', 27017) # change the ip and port to your mongo database's

db = client["contamehistorias"]

try:
    db["url_data"].ensure_index("url", unique=True)
except:
    pass

def load_urls(domain, offset = 0):
    #return collection.find({},timeout=False)[20:25]
    collection = db[domain]
    db["crawled_urls"].create_index("url", unique=True)

    return collection.find({},no_cursor_timeout=True).batch_size(1000)
    
if __name__ == '__main__':
    domain = None
    offset = 0

    print ('Number of arguments:', len(sys.argv), 'arguments.')
    print ('Argument List:', str(sys.argv))


    if(len(sys.argv) >= 2 ):
        domain = str(sys.argv[1])

    urls_cursor = load_urls(domain)
    
    c = 0
    for i in urls_cursor:
        c = c + 1
        if(c % 10000 == 0):
            print(c)

        url = i
        del url["_id"]
        #longtime_add.apply_async(args=[url])
        preprocess_and_download_url.apply_async(args=[url])
