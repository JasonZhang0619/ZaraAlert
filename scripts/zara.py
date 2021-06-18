import requests
import sys
from bs4 import BeautifulSoup, Tag
import time
from GmailApi import *
from zara_items import *
from datetime import datetime

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome"}


# zara bs4
def get_page(rootUrl):
    req = session.get(rootUrl, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    return soup.find("div", {"class": "product-size-selector__size-list-wrapper"})

def check_items():
    result=[]
    for url, size in products.items():
        size_selector=get_page(url)
        # print(url)
        this=[]
        for s in size:
            this_size=size_selector.find_all('li')[s]
            this.append('product-size-selector__size-list-item--out-of-stock' in this_size['class'])
        time.sleep(2)
        result.append(all(this))
    return result

# reload(sys)
# sys.setdefaultencoding('utf8')

session = requests.Session()

count=0
while True:
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    try:
        if not all(check_items()):
            break
        count+=1
        print(count,'-th check at',current_time)
        time.sleep(180) # Sleep for 300 seconds
        if count%10==0:
            session.close()
            session = requests.Session()
    except:
        print("Current Time =", current_time)
        time.sleep(180) # Sleep for 300 seconds
        session.close()
        session = requests.Session()

    
i=0
items=list(products.keys())
stock=[]
for b in check_items():
    if not b:
        stock.append(items[i])
    i+=1

message=create_message('me','jasonzhang0619ca@gmail.com','zara','\n'.join(stock))
send_message(service,'me',message)

