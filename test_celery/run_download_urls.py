from .tasks import longtime_add
from .tasks import request_url
from .tasks import parse_url_archive

import time
from pymongo import MongoClient

client = MongoClient('database', 27017) # change the ip and port to your mongo database's

db = client["arquivopt"]
#db["crawled_urls"].create_index("url", unique=True)

def load_urls(offset = 0):
    #return collection.find({},timeout=False)[20:25]
    return db["processed_urls"].find({},no_cursor_timeout=True).skip(offset).limit(page_size).batch_size(1000)
    
if __name__ == '__main__':
    offset = 0

    print ('Number of arguments:', len(sys.argv), 'arguments.')
    print ('Argument List:', str(sys.argv))

    if(len(sys.argv) >= 2 ):
        offset = int(sys.argv[1])

    urls_cursor = load_urls(offset)
    
    c = 0
    for i in urls_cursor:
        c = c + 1
        if(c % 10000 == 0):
            print(c)

        url = i["url"]
        del url["_id"]
        #longtime_add.apply_async(args=[url])
        request_url.apply_async(args=[url])
