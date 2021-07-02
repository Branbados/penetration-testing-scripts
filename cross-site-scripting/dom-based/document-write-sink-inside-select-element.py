"""
https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-document-write-sink-inside-select-element
"""

import sys
import requests

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()
