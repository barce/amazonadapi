#!/usr/bin/env python

from amazonadapi import AmazonClient
import os
client = AmazonClient()
client.refresh_token = os.environ['AMZN_REFRESH_TOKEN']
client.auto_refresh_token()
client.set_region()
client.get_profiles()
client.profile_id = '3586026682031981'
client.page_size = 20
ads = client.get_advertisers()
print('results:')
print(len(ads))
print(ads)
