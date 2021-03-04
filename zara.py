import requests
import sys
from bs4 import BeautifulSoup, Tag
import time
from GmailApi import *

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome"}
products = {
    # "https://www.zara.com/ca/en/double-faced-faux-leather-jacket-p06318351.html": 0,
    "https://www.zara.com/ca/en/contrasting-checkered-coat-p05914659.html": [0],
    # "https://www.zara.com/ca/en/textured-weave-coat-p05719740.html":[0],
    # "https://www.zara.com/ca/en/faux-leather-biker-jacket-p03427301.html":1,
    "https://www.zara.com/ca/en/limited-edition-fringed-jacquard-sweater-p03597330.html":[0,1],
    # "https://www.zara.com/ca/en/jacquard-animal-sweater-p00048301.html" :0,
    "https://www.zara.com/ca/en/satin-effect-textured-trench-coat-p06518320.html?v1=56333332": [0],
    # "https://www.zara.com/ca/en/textured-wool-sweater-p00693305.html?v1=80302140" :[0],
    # "https://www.zara.com/ca/en/double-faced-jacket-p03548300.html":[0],
    "https://www.zara.com/ca/en/relaxed-fit-trench-coat-p07380670.html":[0],
    "https://www.zara.com/ca/en/geometric-sole-leather-ankle-boots-p12014621.html":[2,3],
    "https://www.zara.com/ca/en/limited-edition-sweater-with-scarf-p00693330.html":[0]
}

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
while all(check_items()):
    count+=1
    print(count,'-th check')
    if count%20==0:
        session.close()
        session = requests.Session()
    time.sleep(180) # Sleep for 300 seconds
    
i=0
items=list(products.keys())
stock=[]
for b in check_items():
    if not b:
        stock.append(items[i])
    i+=1

message=create_message('me','jasonzhang0619ca@gmail.com','zara','\n'.join(stock))
send_message(service,'me',message)

