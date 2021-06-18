import requests
import sys
from bs4 import BeautifulSoup, Tag
import time
import json
import pandas as pd
from pandas import json_normalize
from GmailApi import *
from uniqlo_items import *

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
    "Accept-Language":"en-ca"}


baseUrl = "https://www.uniqlo.com/ca/api/commerce/v3/en/products/"
product_url="https://www.uniqlo.com/ca/en/products/"

session = requests.Session()

# uniqplo bs4
def get_item_df(code):
    req = session.get(baseUrl+code, headers=headers)
    item_json=json.loads(req.text)
    item_json=item_json['result']['items'][0]['l2s']
    item_df=pd.json_normalize(item_json).set_index(['color.code','size.name'])
    return item_df

def check_items():
    for code, attr in products.items():
        item_df=get_item_df(code)
        for col, size in attr:
            if item_df.loc[(col,size),'stock.quantity']>0:
                return code
        time.sleep(2)
    return False

# reload(sys)
# sys.setdefaultencoding('utf8')

session = requests.Session()

count=0
while True:
    code=check_items()
    count+=1
    print(count,'-th check')
    if code:
        break
    
    time.sleep(5*60) # Sleep for 300 seconds
    
    session.close()
    session = requests.Session()
    

message=create_message('me','sujiayun2009@hotmail.com','uniqlo',product_url+code)
send_message(service,'me',message)