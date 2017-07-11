#!/usr/bin/env python

from future.standard_library import install_aliases
install_aliases()


import json
import jwt
import requests
import time
import os


use_environment_variables = None

try:
    from django.conf import settings
except ImportError:
    use_environment_variables = True


class AmazonClient:
  client_id = None
  client_secret = None
  api_key = None
  id_host = None
  one_host = None
  aud = None
  payload = None
  encoded_payload = None
  oauth_url = None
  payload_url = None
  headers = None
  authorized_headers = None
  token = None


  def __init__(self):
    self.client_id = os.environ['AMZN_AD_CLIENT']
    self.client_secret = os.environ['AMZN_AD_CLIENT_SECRET']
    self.auth_url = os.environ['AMZN_AUTH_URL']

  def connect(self):
    get_token_url = "https://api.amazon.com/auth/o2/token"
    payload = "grant_type=authorization_code&code=" + self.amzn_code + "&redirect_uri=https%3A//www.accuenplatform.com/accounts/login/%3Fnext%3D/backstage/api/advertiser&client_id=" + self.client_id + "&client_secret=" + self.client_secret
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': "Basic " + self.base64auth().decode('utf-8')}
    print(get_token_url)
    print(payload)
    print(headers)
    r = requests.post(get_token_url, data=payload, headers=headers)
    results_json = r.json()
    return results_json

  def get_amazon_auth_url():
    print("Go to this URL:")
    print(self.auth_url)


  def cli_auth_dance(self):
    self.get_amazon_auth_url()
    if sys.version_info < (3, 0):
      self.amzn_code = raw_input("Enter Amazon auth code: ")
    else:
      self.amzn_code = input("Enter Amazon auth code: ")

    print("Auth code, {}, entered.".format(self.amzn_code))
    self.raw_token_results = self.connect()
    print("raw_token_results:")
    print(self.raw_token_results)
    self.token = ''
        
