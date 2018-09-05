from .tasks import longtime_add
from .tasks import request_url
from .tasks import parse_url_archive
from .tasks import parse_page

import sys
import time
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('database', 27017) # change the ip and port to your mongo database's

db = client["contamehistorias"]

try:
    db["url_titles"].ensure_index("url", unique=True)
except:
    pass


def load_urls(domain):
    #return collection.find({},timeout=False)[20:25]
    return db["url_contents"].find({"domain":{"$regex": ".*"+domain+".*"}},no_cursor_timeout=True).batch_size(200)
    
if __name__ == '__main__':
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
        parse_page.apply_async(args=[url])
