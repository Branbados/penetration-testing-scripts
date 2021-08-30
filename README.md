# Table of Contents
* [Introduction](#Introduction)
* [Technologies](#Technologies)
* [Installation](#Installation)
* [License](#License)

# Introduction
These are a collection of penetration testing scripts that are designed to leverage vulnerabilities on Portswigger websites found [here](https://portswigger.net/web-security/all-labs). Examples of these vulnerabilities include SQL injection, cross-site scripting, or CSRF. These vulnerabilities are leveraged to elevate privileges and exfiltrate data.

# Technologies
These scripts are written in Python. The requests package is used to create sessions on the vulnerable sites, and to send and receive HTML requests. The sites' HTML is parsed and searched using BeautifulSoup and re. Some scripts use multiprocessing or async to run concurrent brute-force attacks.

# Installation
The following command will install the project.
```
git clone https://github.com/brandonaltermatt/penetration-testing-scripts/
```
You will need a PortSwigger account to access the labs. You can make one [here](https://portswigger.net/users/register).  
With an account, you must go to the selected lab page and generate the lab website. The lab page corresponding to the script can be found in a comment at the top of the script.  
Make sure that you have Python 3 installed. Once you have generated the lab website, run the script on the lab website's randomly generated url.
```
python3 basic-origin-reflection-attack.py https://ac1a1fd31e3d4f0680c069e9009600b0.web-security-academy.net/
```
Note that not all scripts automatically complete the lab, but many do.  
# License
This work is released under the MIT License. Please see the file LICENSE.md in this distribution for license terms.
