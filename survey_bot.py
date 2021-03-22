#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
import re
import pprint

pp = pprint.PrettyPrinter(indent=4)

secrets = []
with open('secrets.json', 'r') as secrets_file:
    secrets = json.load(secrets_file)

session = requests.Session()
DAILY_SURVEY_URL = 'https://myaccess.southern.edu/mvc/daily/healthsurvey'

headers = {
    "Accept": "text/html,application/xhtml xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Upgrade-Insecure-Requests": "1",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4202.0 Safari/537.36",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-User": "?1",
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Fetch-Mode": "navigate"
}

response_myaccess = session.get("https://myaccess.southern.edu/", headers=headers)
soup = BeautifulSoup(response_myaccess.content, features='lxml')
form_element = soup.find('form')
adfs_url = form_element.get('action')
saml_element = soup.find('input', attrs={'name':'SAMLRequest'})
relaystate_element = soup.find('input', attrs={'name':'RelayState'})

post_params = {
    'SAMLRequest': saml_element.get('value'),
    'RelayState': relaystate_element.get('value')
}

response_auth_post1 = session.post(url=adfs_url, data=post_params)

soup = BeautifulSoup(response_auth_post1.content, features='lxml')

login_url = soup.find('form', id='options').get('action')
login_post_params = {
    'UserName':   secrets['username'],
    'Password':   secrets['password'],
    'as_sfid':    soup.find('input', attrs={'name':'as_sfid'}).get('value'),
    'as_fid':     soup.find('input', attrs={'name':'as_fid'}).get('value'),
    'AuthMethod': 'FormsAuthentication'
}

response_login_post = session.post(url=login_url, data=login_post_params)

soup = BeautifulSoup(response_login_post.content, features='lxml')

saml_url = soup.find('form').get('action')
saml_post_params = {
    'as_sfid':      soup.find('input', attrs={'name':'as_sfid'}).get('value'),
    'as_fid':       soup.find('input', attrs={'name':'as_fid'}).get('value'),
    'RelayState':   soup.find('input', attrs={'name':'RelayState'}).get('value'),
    'SAMLResponse': soup.find('input', attrs={'name':'SAMLResponse'}).get('value')
}

response_saml_post = session.post(url=saml_url, data=saml_post_params)

soup = BeautifulSoup(response_saml_post.content, features='lxml')

last_auth_url = soup.find('form').get('action')
last_auth_params = {
    'wresult': soup.find('input', attrs={'name':'wresult'}).get('value'),
    'wa':      soup.find('input', attrs={'name':'wa'}).get('value'),
    'wctx':    soup.find('input', attrs={'name':'wctx'}).get('value'),
    'as_sfid': soup.find('input', attrs={'name':'as_sfid'}).get('value'),
    'as_fid':  soup.find('input', attrs={'name':'as_fid'}).get('value'),
}
response_last_auth_post = session.post(url=last_auth_url, data=last_auth_params)

print("Status code:   %i" % response_last_auth_post.status_code)
print("Authentication Complete :) In theory successfully too :)")

response_daily_survey = session.get(DAILY_SURVEY_URL)

soup = BeautifulSoup(response_daily_survey.content, features='lxml')

survey_post_url = 'https://myaccess.southern.edu/mvc/daily/HealthSurvey/Daily'
daily_survey_params = {}

survey_inputs = soup.find('form').find_all('input')
for survey_input in survey_inputs:
    daily_survey_params[survey_input.get('name')] = survey_input.get('value')

for key in daily_survey_params.keys():
    if re.search(r'\.Answer', key):
        if not ((daily_survey_params[key] == "No") or (daily_survey_params[key] == "I Agree")):
            daily_survey_params[key] = 'No'

print("Survey Params to Submit")
pp.pprint(daily_survey_params)
response_daily_survey_post = session.post(url=survey_post_url, data=daily_survey_params)
print("Status code:   %i" % response_daily_survey_post.status_code)
print(f"Now on page {response_daily_survey_post.url}")