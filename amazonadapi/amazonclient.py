#!/usr/bin/env python

from future.standard_library import install_aliases
install_aliases()


import json
import jwt
import requests
import time
import os
import sys
import re
from urllib3._collections import HTTPHeaderDict

use_environment_variables = None

try:
    from django.conf import settings
except ImportError:
    use_environment_variables = True

class AmazonOrder:
  id = None
  advertiserId = None
  name = None
  startDateTime = None
  endDateTime = None
  status = None
  budget = {}
  deliveryCaps = []


  def __init__(self):
    self.status = 'INACTIVE'

class AmazonLineItem:
  id = None
  orderId = None
  advertiserId = None
  name = None
  type = None
  startDateTime = None
  endDateTime = None
  status = None
  budget = {}
  deliveryCaps = []

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
  region = None
  region_list = {}
  host = None
  data = None
  page_token = None
  page_size = None
  next_page_url = None
  redirect_uri = None

  def __init__(self):
    self.client_id = os.environ['AMZN_AD_CLIENT_ID']
    self.client_secret = os.environ['AMZN_AD_CLIENT_SECRET']
    # self.auth_url = "https://www.amazon.com/ap/oa?client_id=" + self.client_id + "&scope=advertising::campaign_management&repsonse_type=code&redirect_url=https%3A//www.accuenplatform.com/accounts/login/%3Fnext%3D/backstage/api/advertiser"
    self.auth_url = os.environ['AMZN_AUTH_URL']
    self.profile_id = os.environ['AMZN_DEFAULT_PROFILE_ID']
    self.redirect_uri="https://www.accuenplatform.com/accounts/login/%3Fnext%3D/backstage/api/advertiser"

    try:
      self.refresh_token = os.environ['AMZN_REFRESH_TOKEN']
    except KeyError as e:
      print("error missing:")
      print(e)

    self.region_list = {"UK": "advertising-api-eu.amazon.com", "IN": "advertising-api-eu.amazon.com", "US": "advertising-api.amazon.com", "JP": "advertising-api-fe.amazon.com"}
    try:
      self.host = self.region_list[os.environ['AMZN_REGION']]
    except KeyError as e:
      self.host = 'advertising-api.amazon.com'

  def connect(self):
    get_token_url = "https://api.amazon.com/auth/o2/token"
    payload = "grant_type=authorization_code&code=" + self.amzn_code + "&redirect_uri=" + self.redirect_uri + "&client_id=" + self.client_id + "&client_secret=" + self.client_secret
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
    print("raw_token_results:")
    print(self.raw_token_results)
    self.token = self.raw_token_results['access_token']
    self.refresh_token = self.raw_token_results['refresh_token']
    profiles_json = self.get_profiles()
    self.profile_id = str(profiles_json[0]['profileId'])
    return self.token

  def auto_refresh_token(self):
    i_sentinel = 1
    i_counter = 0
    while i_sentinel > 0:
      get_token_url = "https://api.amazon.com/auth/o2/token"
      payload = "grant_type=refresh_token&client_id=" + self.client_id + "&client_secret=" + self.client_secret + "&refresh_token=" + self.refresh_token
      headers = {'Content-Type': 'application/x-www-form-urlencoded'}
      r = requests.post(get_token_url, data=payload, headers=headers)
      results_json = r.json()
      if 'access_token' in results_json:
        self.token = results_json['access_token']
        return results_json
      i_counter += 1
      time.sleep(1)
      if i_counter >= 5:
        i_sentinel = 0
    return results_json

  def set_region(self, region='US'):
    self.region = region
    try:
      self.host = self.region_list[region]
    except KeyError as e:
      self.host = self.region_list["US"]
      self.region = "US"
    return self.host

  # curl -X GET -H "Content-Type:application/json" -H "Authorization: Bearer $AMZN_TOKEN" https://advertising-api.amazon.com/v1/profiles
  def get_profiles(self):
    url = "https://" + self.host + "/v1/profiles"
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.token}
    # r = requests.get(url, headers=headers)
    # results_json = r.json()

    r = self.make_request(url, headers, 'GET')
    return r

  # -H Authorization: Bearer self.token
  # -H Host: advertising-api.amazon
  # -H Amazon-Advertising-API-Scope: PROFILE_ID
  # -H Content-Type: application/json
  # url: https://advertising-api.amazon.com/da/v1/advertisers
  def get_advertisers(self):
    i_sentinel = 1
    ids = []
    response_json = {}
    while i_sentinel == 1:
      if self.page_token == None:
        if self.page_size == None:
          url = "https://" + self.host + "/da/v1/advertisers"
        else:
          url = "https://" + self.host + "/da/v1/advertisers?page_size=" + str(self.page_size)
          self.page_size = None
      else:
        url = "https://" + self.host + "/da/v1/advertisers?page_token=" + self.page_token

      headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.token, 'Host': self.host, 'Amazon-Advertising-API-Scope': self.profile_id}

      r = self.make_request(url, headers, 'GET')
      try:
        print(r.headers['Link'])
        self.next_page_url = r.headers['Link']
      except:
        i_sentinel = 0

      if self.next_page_url != None:
        p = re.compile('.*page_token=(.*)>')
        matches = p.findall(self.next_page_url)
        self.page_token = matches[0]


    self.page_token = None
    self.page_size = None
    return r

  # -H Authorization: Bearer self.token
  # -H Host: advertising-api.amazon
  # -H Amazon-Advertising-API-Scope: PROFILE_ID
  # -H Content-Type: application/json
  # url: https://advertising-api.amazon.com/da/v1/advertisers/AD_ID/orders

  def get_orders(self, ad_id):
    i_sentinel = 1

    while i_sentinel == 1:
      if self.page_token == None:
        if self.page_size == None:
          url = "https://" + self.host + "/da/v1/advertisers/" + str(ad_id) + "/orders"
        else:
          url = "https://" + self.host + "/da/v1/advertisers/" + str(ad_id) + "/orders?page_size=" + str(self.page_size)
          self.page_size = None
      else:
        url = "https://" + self.host + "/da/v1/advertisers/" + str(ad_id) + "/orders?page_token=" + self.page_token
      headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.token, 'Host': self.host, 'Amazon-Advertising-API-Scope': self.profile_id}
      r = self.make_request(url, headers, 'GET')
      try:
        self.next_page_url = r.headers['Link']
      except:
        i_sentinel = 0

      if self.next_page_url != None:
        p = re.compile('.*page_token=(.*)>')
        matches = p.findall(self.next_page_url)
        self.page_token = matches[0]


    self.page_token = None
    self.page_size = None
    return r


  # -H Authorization: Bearer self.token
  # -H Host: advertising-api.amazon
  # -H Amazon-Advertising-API-Scope: PROFILE_ID
  # -H Content-Type: application/json
  # url: https://advertising-api.amazon.com/da/v1/orders/ORDER_ID
  def get_order(self, order_id):

    url = "https://" + self.host + "/da/v1/orders/" + order_id
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.token, 'Host': self.host, 'Amazon-Advertising-API-Scope': self.profile_id}

    r = self.make_request(url, headers, 'GET')
    return r

  # -H Authorization: Bearer self.token
  # -H Host: advertising-api.amazon
  # -H Amazon-Advertising-API-Scope: PROFILE_ID
  # -H Content-Type: application/json
  # url: https://advertising-api.amazon.com/da/v1/orders/ORDER_ID/line-items
  def get_line_items(self, order_id):
    i_sentinel = 1
    ids = []
    response_json = {}
    while i_sentinel == 1:
      if self.page_token == None:
        if self.page_size == None:
          url = "https://" + self.host + "/da/v1/orders/" + order_id + "/line-items"
        else:
          url = "https://" + self.host + "/da/v1/orders/" + order_id + "/line-items?page_size=" + str(self.page_size)
          self.page_size = None
      else:
        url = "https://" + self.host + "/da/v1/orders/" + order_id + "/line-items?page_token=" + self.page_token

      headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.token, 'Host': self.host, 'Amazon-Advertising-API-Scope': self.profile_id}
      r = self.make_request(url, headers, 'GET')

      try:
        self.next_page_url = r.headers['Link']
      except:
        i_sentinel = 0

      if self.next_page_url != None:
        p = re.compile('.*page_token=(.*)>')
        matches = p.findall(self.next_page_url)
        self.page_token = matches[0]


    self.page_token = None
    self.page_size = None
    return r

  def get_line_item(self, line_item_id):
    url = "https://" + self.host + "/da/v1/line-items/" + line_item_id
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.token, 'Host': self.host, 'Amazon-Advertising-API-Scope': self.profile_id}

    r = self.make_request(url, headers, 'GET')
    return r

  def create_order(self, order):
    url = "https://" + self.host + "/da/v1/orders"
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.token, 'Host': self.host, 'Amazon-Advertising-API-Scope': self.profile_id}

    self.data = order

    r = self.make_request(url, headers, 'POST', self.data)
    return r


  def update_order(self, order):
    url = "https://" + self.host + "/da/v1/orders"
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.token, 'Host': self.host, 'Amazon-Advertising-API-Scope': self.profile_id}


    self.data = order

    r = self.make_request(url, headers, 'PUT', self.data)
    return r

  def create_line_item(self, line_item):
    url = "https://" + self.host + "/da/v1/line-items"
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.token, 'Host': self.host, 'Amazon-Advertising-API-Scope': self.profile_id}

    self.data = line_item

    r = self.make_request(url, headers, 'POST', self.data)
    return r


  def update_line_item(self, line_item):
    # url = "https://" + self.host + "/da/v1/line-items/" + line_item.id # <-- expected behavior for update
    url = "https://" + self.host + "/da/v1/line-items"
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.token, 'Host': self.host, 'Amazon-Advertising-API-Scope': self.profile_id}

    self.data = line_item

    r = self.make_request(url, headers, 'PUT', self.data)
    return r

  def error_check_json(self, results_json):
    # if results_json['error']['httpStatusCode'] in ['401'] or results_json['code'] in ['401']:
    refresh_results_json = self.auto_refresh_token()
    return refresh_results_json

  # create response_json method to abstract away the creation of return response that matt wants
  def generate_json_response(self, r, results_json, request_body):

    response_json = {
      'response_code': r.status_code,
      'request_body': request_body
    }
    # if request is successful, ensure msg_type is success
    if r.status_code in [200, 201]:
      response_json['msg_type'] = 'success'
      response_json['msg'] = ''
      response_json['data'] = results_json
    else:
      response_json['msg_type'] = 'error'
      # display the error message that comes back from request
      response_json['msg'] = results_json['error']
      response_json['data'] = results_json['error']

    return response_json

  # make_request(method_type) --> pass in method_type
  def make_request(self, url, headers, method_type, data=None):
    request_body = url, headers, data
    r, results_json = self.make_new_request(url, self.token, method_type, headers, data)

    if r.status_code in [400, 401]:
        # refresh access token
        self.token = self.error_check_json(results_json)['access_token']
        # apply headers with new token, return response and response dict
        r, results_json = self.make_new_request(url, self.token, method_type, headers)

    # use results_json to create updated json dict
    response_json = self.generate_json_response(r, results_json, request_body)

    return json.dumps(response_json)

  def make_new_request(self, url, token, method_type, headers, data=None):

    # modify headers with new access token
    headers['Authorization'] = 'Bearer ' + token
    if method_type == 'GET':
      r = requests.get(url, headers=headers)
    if method_type == 'POST':
      r = requests.post(url, headers=headers, verify=False, data=json.dumps(data))
    if method_type == 'PUT':
      r = requests.put(url, headers=headers, verify=False, data=json.dumps(data))
    results_json = r.json()
    return r, results_json
