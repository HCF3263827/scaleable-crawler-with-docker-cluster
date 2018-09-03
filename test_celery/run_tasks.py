from .tasks import longtime_add
import time
from pymongo import MongoClient
import sys

#3client = MongoClient('10.1.1.234', 27017) # change the ip and port to your mongo database's
client = MongoClient('database', 27017) # change the ip and port to your mongo database's

db = client["arquivopt"]
collection = db["urls"]
db["crawled_urls"].create_index("url", unique=True)

page_size = 1000000

def load_urls(offset = 0):
    #return collection.find({},timeout=False)[20:25]
    return collection.find({},no_cursor_timeout=True).skip(offset).limit(page_size).batch_size(1000)
    
if __name__ == '__main__':
    

    offset = 0

    print ('Number of arguments:', len(sys.argv), 'arguments.')
    print ('Argument List:', str(sys.argv))

    if(len(sys.argv) >= 2 ):
        offset = int(sys.argv[1])

    urls_cursor = load_urls(offset)
    for i in urls_cursor:
        
        url = i["url"]
        print("requesting url",url)
        result = longtime_add.delay(url)
        #print 'Task result:',result.result
