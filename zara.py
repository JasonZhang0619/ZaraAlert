import requests
import sys
from bs4 import BeautifulSoup, Tag
import time

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome"}
products = {
    "https://www.zara.com/ca/en/double-faced-faux-leather-jacket-p06318351.html": 0,
    "https://www.zara.com/ca/en/contrasting-checkered-coat-p05914659.html":0,
    "https://www.zara.com/ca/en/textured-weave-coat-p05719740.html":0,
    # "https://www.zara.com/ca/en/jacquard-animal-sweater-p00048301.html" :0,
    "https://www.zara.com/ca/en/satin-effect-textured-trench-coat-p06518320.html?v1=56333332": 0,
    "https://www.zara.com/ca/en/textured-wool-sweater-p00693305.html?v1=80302140" :0,
    # "https://www.zara.com/ca/en/double-faced-jacket-p03548300.html":0
}


import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
from email.mime.text import MIMEText

def create_message(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

    Returns:
    An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    message=message.as_string()
    return {'raw': base64.urlsafe_b64encode(message.encode("utf-8")).decode("utf-8")}

def send_message(service, user_id, message):
    message = (service.users()
    .messages()
    .send(userId=user_id, 
    body=message)
    .execute())
    print ('Message Id: %s' % message['id'])
    return message

# zara bs4
def get_page(rootUrl):
    req = session.get(rootUrl, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    return soup.find("div", {"class": "product-size-selector__size-list-wrapper"})

def check_items(size=0):
    result=[]
    for url, size in products.items():
        size_selector=get_page(url)
        # print(url)
        smallest_size=size_selector.find_all('li')[size]
        result.append('product-size-selector__size-list-item--out-of-stock' in smallest_size['class'])
        time.sleep(2)
    return result

# reload(sys)
# sys.setdefaultencoding('utf8')

## google gamil api
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('gmail', 'v1', credentials=creds)

session = requests.Session()

count=0
while all(check_items()):
    count+=1
    print(count,'-th check')
    if count%20==0:
        session = requests.Session()
    time.sleep(180) # Sleep for 300 seconds
    
i=0
items=list(products.keys())
stock=[]
for b in check_items():
    if not b:
        stock.append(items[i])
    i+=1

message=create_message('jasonzhang0619ca@gmail.com','jasonzhang0619ca@gmail.com','zara','\n'.join(stock))
send_message(service,'me',message)

