#!/usr/bin/env python

from amazonadapi import AmazonClient, AmazonOrder, AmazonLineItem
import os
import random
import time

# number of failed tests
i_fail = 0

# logging in test

try:
  client = AmazonClient()
  client.refresh_token = os.environ['AMZN_REFRESH_TOKEN']
  client.auto_refresh_token()
  client.set_region()
  client.get_profiles()
  client.profile_id = '3586026682031981'
except:
  i_fail += 1

# orders = client.get_orders(dsp_advertiser_id)
# client.page_size = 20


try: 
  ads = client.get_advertisers()
except:
  i_fail += 1

  
try:
  client.page_size = 1
  orders = client.get_orders('3678742709207')
except: 
  i_fail += 1

try:
  line_items = client.get_line_items('7287373481448')
except: 
  i_fail += 1

print('testing CR & U')
print('--------------')

print('create order')
try:
  order = AmazonOrder()
  
  order.advertiserId = '3678742709207'
  order.name = 'amazon api test {}'.format(time.time())
  order.startDateTime = 1511909961000 # unix time * 1000
  order.endDateTime = 1512514761000   # unix time * 1000
  
  hash_order = {"object": {
      "advertiserId": {
        "value": order.advertiserId
      },
      "name": order.name,
      "startDateTime": order.startDateTime,
      "endDateTime": order.endDateTime,
      "deliveryActivationStatus": order.status
      }
  }
  
  created_order = client.create_order(hash_order)
except:
  i_fail += 1

print(created_order)
order_id = created_order['object']['id']['value']

try:
  print('update order')

  hash_order = {"object": {
       "id": {
           "value": order_id
       },
       "advertiserId": {
           "value": order.advertiserId
       },
       "name": 'updated api test',
       "startDateTime": order.startDateTime,
       "endDateTime": order.endDateTime,
       "deliveryActivationStatus": order.status
       }
   }

  updated_order = client.update_order(hash_order)
  print('updated order:')
  print('--------------')
  print(updated_order)
  print(updated_order['object']['name'])
except:
  i_fail += 1

if updated_order['object']['name'] != 'updated api test':
  i_fail += 1
else:
  print('update success...')

try: 
  print('create line item')
  line_item = AmazonLineItem()
  line_item.orderId = order_id
  line_item.advertiserId = '3678742709207'
  line_item.type = "NON_GUARANTEED_DISPLAY"
  line_item.name = 'barce line_item'
  line_item.startDateTime = 1511909961000
  line_item.endDateTime = 1512514761000
  line_item.status = 'INACTIVE'
  line_item.budget = { "amount": 100, "deliveryProfile": "FRONTLOADED" }
  line_item.deliveryCaps = [ { "amount": 1.0, "recurrenceType": "DAILY" } ]
  
  
  hashline_item = {"object": {
      "orderId": {
        "value": line_item.orderId
      },
      "advertiserId": {
        "value": line_item.advertiserId
      },
      "name": line_item.name,
      "type": line_item.type,
      "startDateTime": line_item.startDateTime,
      "endDateTime": line_item.endDateTime,
      "deliveryActivationStatus": line_item.status,
      "budget" : line_item.budget,
      "deliveryCaps" : line_item.deliveryCaps
      
    }
  }
  
  created_line_item = client.create_line_item(hashline_item)
  print(created_line_item)
except:
  i_fail += 1


line_item_id = created_line_item['object']['id']['value']
try: 
  hashline_item = {"object": {
       "id": {
           "value": line_item_id
       },
      "orderId": {
        "value": line_item.orderId
      },
      "advertiserId": {
        "value": line_item.advertiserId
      },
      "name": 'updated line item',
      "type": line_item.type,
      "startDateTime": line_item.startDateTime,
      "endDateTime": line_item.endDateTime,
      "deliveryActivationStatus": line_item.status,
      "budget" : line_item.budget,
      "deliveryCaps" : line_item.deliveryCaps

    }
  }

  updated_line_item = client.update_line_item(hashline_item)
  print(updated_line_item)
except:
  i_fail += 1


print("\n\n\n")
print("Tests complete. {} test(s) failed.".format(i_fail))
