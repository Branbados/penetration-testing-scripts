"""
https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-jquery-href-attribute-sink
"""

import sys
import requests

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()

