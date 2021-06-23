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
        if all(this):# every size out ot stock
            continue
        result.append(url)
    return result # [] if nothing in stock

# reload(sys)
# sys.setdefaultencoding('utf8')

session = requests.Session()

count=0
while True:
    count+=1
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    try:
        for stock in check_items():
            del products[stock]
            message=create_message('me','jasonzhang0619ca@gmail.com','zara',stock)
            send_message(service,'me',message)
            print(url,' in stock') 
        
        print(count,'-th check at',current_time)
        time.sleep(180) # Sleep for 300 seconds

    except:
        print("Current Time =", current_time)
        time.sleep(180) # Sleep for 300 seconds
        session.close()
        session = requests.Session()

