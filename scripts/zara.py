import requests
import sys
from bs4 import BeautifulSoup, Tag
import time
from GmailApi import *
from zara_items import products
from datetime import datetime

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome"}
session = requests.Session()
price_records_filename='zara.csv'

def write_price_record(record,filename='zara.csv'):
    file_exist = os.path.exists(filename)
    with open(filename, 'a') as f:
        if not file_exist:
            f.write('url,time,price\n')
        f.write(' , '.join(record)+'\n')
        f.close()


class shop_item:
    def __init__(self, url, sizes):
        self.url=url
        self.price=999.9
        self.price_records = []
        self.sizes = sizes

    def send_email_alert(self):
        message=create_message('me','jasonzhang0619ca@gmail.com','zara', self.url)
        send_message(service,'me',message)

    def refresh_page(self):
        req = session.get(self.url, headers=headers)
        self.sp = BeautifulSoup(req.text, 'html.parser')
        if self.sizes:
            self.check_size_stock()
        self.record_price()
        
    def record_price(self):
        current_price = float(self.sp.find("span",{"class": "price__amount-current"}).text.strip(' CAD'))
        if current_price < self.price:
            write_price_record([self.url,datetime.now().strftime("%d/%m/%Y %H:%M:%S"),str(current_price)])
            self.price = current_price
        
    
    def check_size_stock(self):
        if self.sp.find("button", {"class": "button--secondary"}): # no stock at all
            return 0
        else:
            size_selector=self.sp.find("div", {"class": "product-detail-size-selector__size-list-wrapper"})
            if size_selector: # with size options
                sizes = []
                for s in self.sizes:
                    if 'product-detail-size-selector__size-list-item--out-of-stock' not in size_selector.find_all('li')[s]['class']: # stock with particular size
                        self.send_email_alert()
                    else:
                        sizes.append(s)
                self.sizes=sizes
            else: # no size options
                self.send_email_alert()   


def check_items(items):
    for item in items:
        item.refresh_page()
        time.sleep(2)

# reload(sys)
# sys.setdefaultencoding('utf8')

count=0
items = [shop_item(url,sizes) for url, sizes in products.items()]
while True:
    count+=1
    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y %H:%M:%S")
    try:
        check_items(items)
        print(count,'-th check at',current_time)
        time.sleep(180) # Sleep for 300 seconds

    except:
        print("Current Time =", current_time)
        time.sleep(180) # Sleep for 300 seconds
        session.close()
        session = requests.Session()

