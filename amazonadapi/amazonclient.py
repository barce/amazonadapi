#!/usr/bin/env python

from future.standard_library import install_aliases
install_aliases()


import json
import jwt
import requests
import time
import os
import sys
from urllib3._collections import HTTPHeaderDict

use_environment_variables = None

try:
    from django.conf import settings
except ImportError:
    use_environment_variables = True

class AmazonOrder:
  advertiserId = None
  name = None
  startDateTime = None
  endDateTime = None
  status = None


  def __init__(self):
    self.status = 'INACTIVE'

class AmazonLineItem:
  orderId = None
  name = None
  type = None
  startDateTime = None
  endDateTime = None
  status = None

  def __init__(self):
    self.status = 'INACTIVE'

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
  refresh_token = None
  profile_id = None
  host = None

  def __init__(self):
    self.client_id = os.environ['AMZN_AD_CLIENT_ID']
    self.client_secret = os.environ['AMZN_AD_CLIENT_SECRET']
    # self.auth_url = "https://www.amazon.com/ap/oa?client_id=" + self.client_id + "&scope=advertising::campaign_management&repsonse_type=code&redirect_url=https%3A//www.accuenplatform.com/accounts/login/%3Fnext%3D/backstage/api/advertiser"
    self.auth_url = os.environ['AMZN_AUTH_URL']
    self.host = 'advertising-api.amazon.com'

  def connect(self):
    get_token_url = "https://api.amazon.com/auth/o2/token"
    payload = "grant_type=authorization_code&code=" + self.amzn_code + "&redirect_uri=https%3A//www.accuenplatform.com/accounts/login/%3Fnext%3D/backstage/api/advertiser&client_id=" + self.client_id + "&client_secret=" + self.client_secret
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    print(get_token_url)
    print(payload)
    print(headers)
    r = requests.post(get_token_url, data=payload, headers=headers)
    results_json = r.json()
    return results_json

  def get_amazon_auth_url(self):
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
    # print("raw_token_results:")
    # print(self.raw_token_results)
    self.token = self.raw_token_results['access_token']
    self.refresh_token = self.raw_token_results['refresh_token']
    profiles_json = self.get_profiles()
    self.profile_id = str(profiles_json[0]['profileId'])
    return self.token

  def refresh_token(self):
    get_token_url = "https://api.amazon.com/auth/o2/token"
    payload = "grant_type=refresh_token&client_id=" + self.client_id + "&client_secret=" + self.client_secret + "&refresh_token=" + self.refresh_token
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(get_token_url, data=payload, headers=headers)
    results_json = r.json()
    self.token = results_json['access_token']
    return results_json

  # curl -X GET -H "Content-Type:application/json" -H "Authorization: Bearer $AMZN_TOKEN" https://advertising-api.amazon.com/v1/profiles
  def get_profiles(self):
    url = "https://advertising-api.amazon.com/v1/profiles"
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.token}
    r = requests.get(url, headers=headers)
    results_json = r.json()
    return results_json

  # -H Authorization: Bearer self.token
  # -H Host: advertising-api.amazon
  # -H Amazon-Advertising-API-Scope: PROFILE_ID
  # -H Content-Type: application/json
  # url: https://advertising-api.amazon.com/da/v1/orders/ORDER_ID
  def get_order(self, order_id):
    url = "https://advertising-api.amazon.com/da/v1/orders/" + order_id
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.token, 'Host': self.host, 'Amazon-Advertising-API-Scope': self.profile_id}
    r = requests.get(url, headers=headers)
    print(r)
    print(r.url)
    print(r.text)
    results_json = r.json()
    return results_json

  def get_line_item(self, line_item_id):
    url = "https://advertising-api.amazon.com/da/v1/line_items/" + line_item_id
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.token, 'Host': self.host, 'Amazon-Advertising-API-Scope': self.profile_id}
    r = requests.get(url, headers=headers)
    results_json = r.json()
    return results_json
      
  def create_order(self, order):
    url = "https://advertising-api.amazon.com/da/v1/orders/"
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.token, 'Host': self.host, 'Amazon-Advertising-API-Scope': self.profile_id}

    data = {"object": {
        "advertiserId": {
            "value": order.advertiserId
        },
        "name": order.name,
        "startDateTime": order.startDatetime,
        "endDateTime": order.endDateTime,
        "deliveryActiviationStatus": order.status
        }
    }
    
    response = requests.post(url, headers=self.authorized_headers, verify=False, data=data)
    print("{}".format(json.loads(response.text)))
    return json.loads(response.text)


  def create_line_item(self, line_item):
    url = "https://advertising-api.amazon.com/da/v1/line-items/"
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.token, 'Host': self.host, 'Amazon-Advertising-API-Scope': self.profile_id}

    data = {"object": {
        "orderId": {
            "value": line_item.orderId
        },
        "name": line_item.name,
        "startDateTime": line_item.startDatetime,
        "endDateTime": line_item.endDateTime,
        "deliveryActivationStatus": line_item.status
        }
    }
    
    response = requests.post(url, headers=self.authorized_headers, verify=False, data=data)
    print("{}".format(json.loads(response.text)))
    return json.loads(response.text)
    
