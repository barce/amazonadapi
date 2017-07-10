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


class AOLClient:
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
    self.client_id = os.environ['AOP_CLIENT_ID']
    self.client_secret = os.environ['AOP_CLIENT_SECRET']
    self.api_key = os.environ['AOP_API_KEY']
    self.id_host = os.environ['AOP_ID_HOST']
    self.one_host = os.environ['AOP_ONE_HOST']

  def connect(self):
    self.set_payload()
    self.encode_payload()
    self.set_oauth_url()
    self.set_payload_url()
    self.set_headers()
    return self.get_token()

  def show_config(self):
    print(self.client_id)
    print(self.client_secret)
    print(self.api_key)
    print(self.id_host)
    print(self.one_host)


  def set_payload(self):
    now = int(time.time())
    self.payload = {
      "aud": "https://{0}/identity/oauth2/access_token?realm=aolcorporate/aolexternals".format(self.id_host),
      "iss": self.client_id,
      "sub": self.client_id,
      "exp": now + 3600,
      "iat": now ,
    }
    return self.payload

  def encode_payload(self):
    self.encoded_payload = jwt.encode(self.payload, self.client_secret, algorithm='HS256')
    return self.encoded_payload


  def set_oauth_url(self):
    self.oauth_url = "https://{0}/identity/oauth2/access_token".format(self.id_host)

  def set_payload_url(self):
    self.payload_url = "grant_type=client_credentials&scope=one&realm=aolcorporate/aolexternals&client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer&client_assertion={0}".format(bytes.decode(self.encoded_payload))
    return self.payload_url

  def set_headers(self):
    self.headers = {
      "Content-Type": "application/x-www-form-urlencoded",
      "Accept": "application/json"
    }

  def get_token(self):
    response = requests.post(self.oauth_url, headers=self.headers, data=self.payload_url)
    json_response = json.loads(response.text)
    print(json_response)
    self.token = json_response['access_token']
    self.authorized_headers = {'Authorization': "Bearer " + self.token}

    self.authorized_headers['Content-Type'] = 'application/json'
    self.authorized_headers['x-api-key'] = self.api_key

  def get_organizations(self):
    url = "https://{0}/advertiser/organization-management/v1/organizations/".format(self.one_host)
    response = requests.get(url, headers=self.authorized_headers, verify=False)
    return json.loads(response.text)

  def get_campaigns(self, org_id=0):
    url = "https://{0}/advertiser/campaign-management/v1/organizations/{1}/advertisers/campaigns".format(self.one_host, org_id)
    response = requests.get(url, headers=self.authorized_headers, verify=False)
    return json.loads(response.text)


  def get_campaigns_by_advertiser(self, org_id=0, ad_id=0):
    url = "https://{0}/advertiser/campaign-management/v1/organizations/{1}/advertisers/{2}/campaigns".format(self.one_host, org_id, ad_id)
    response = requests.get(url, headers=self.authorized_headers, verify=False)
    return json.loads(response.text)

  def get_campaigns_by_advertiser_by_campaign(self, org_id=0, ad_id=0, campaign_id=0):
    url = "https://{0}/advertiser/campaign-management/v1/organizations/{1}/advertisers/{2}/campaigns/{3}".format(self.one_host, org_id, ad_id, campaign_id)
    response = requests.get(url, headers=self.authorized_headers, verify=False)
    return json.loads(response.text)

  def get_tactics_by_campaign(self, org_id=0, ad_id=0, campaign_id=0):
    url = "https://{0}/advertiser/campaign-management/v1/organizations/{1}/advertisers/{2}/campaigns/{3}/tactics".format(self.one_host, org_id, ad_id, campaign_id)
    response = requests.get(url, headers=self.authorized_headers, verify=False)
    return json.loads(response.text)

  def get_tactic_by_id(self, org_id=0, ad_id=0, campaign_id=0, tactic_id=0):
    url = "https://{0}/advertiser/campaign-management/v1/organizations/{1}/advertisers/{2}/campaigns/{3}/tactics/{4}".format(self.one_host, org_id, ad_id, campaign_id, tactic_id)
    response = requests.get(url, headers=self.authorized_headers, verify=False)
    return json.loads(response.text)

  def get_creative_assignments(self, org_id=0, ad_id=0, campaign_id=0, tactic_id=0):
    url = "https://{0}/advertiser/campaign-management/v1/organizations/{1}/advertisers/{2}/campaigns/{3}/tactics/{4}/creativeassignments".format(self.one_host, org_id, ad_id, campaign_id, tactic_id)
    response = requests.get(url, headers=self.authorized_headers, verify=False)
    print("{}".format(json.loads(response.text)))
    return json.loads(response.text)
