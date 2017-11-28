#!/usr/bin/env python

from amazonadapi import AmazonClient
import os
client = AmazonClient()
client.refresh_token = os.environ['AMZN_REFRESH_TOKEN']
client.auto_refresh_token()
client.set_region()
client.get_profiles()
client.profile_id = '3586026682031981'
# orders = client.get_orders(dsp_advertiser_id)
# client.page_size = 20
ads = client.get_advertisers()
print('ads:')
print(len(ads))
print(ads)

client.page_size = 1
orders = client.get_orders('3678742709207')
print('orders:')
print(len(orders))
print(orders)

line_items = client.get_line_items('7287373481448')
print('line items:')
print(len(line_items))
print(line_items)

print('testing CR & U')
print('--------------')
line_item = {PUT_ANYTHING_IN_HER}

result = client.create_line_item(line_item)
print(result)
