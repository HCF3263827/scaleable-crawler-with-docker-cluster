from .tasks import longtime_add
import time
from pymongo import MongoClient

#3client = MongoClient('10.1.1.234', 27017) # change the ip and port to your mongo database's
client = MongoClient('database', 27017) # change the ip and port to your mongo database's

db = client["arquivopt"]
collection = db["urls"]
db["url_contents"].create_index("url", unique=True)

def load_urls():
    #return collection.find({},timeout=False)[20:25]
    return collection.find({},no_cursor_timeout=True).batch_size(100)
    
if __name__ == '__main__':
    urls_cursor = load_urls()
    
    for i in urls_cursor:
        
        url = i["url"]
        print("requesting url",url)
        result = longtime_add.delay(url, i["_id"])
        print 'Task result:',result.result
