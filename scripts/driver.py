#!/usr/bin/env python

from amazonadapi import AmazonClient, AmazonOrder, AmazonLineItem
import os
import random
import time

# number of failed tests
i_fail = 0

# logging in test

client = None
created_order = None

try:
  print('login test')
  os.environ['AMZN_DEFAULT_PROFILE_ID'] = '3586026682031981'
  client = AmazonClient()
  client.refresh_token = os.environ['AMZN_REFRESH_TOKEN']
  client.auto_refresh_token()
  client.set_region()
  client.get_profiles()
  client.profile_id == '3586026682031981'
except:
  print('------------------------------------------------------- failed login')
  i_fail += 1

# orders = client.get_orders(dsp_advertiser_id)
# client.page_size = 20


try: 
  ads = client.get_advertisers()
except:
  print('------------------------------------------------------- failed get_advertisers')
  i_fail += 1

  
try:
  client.page_size = 1
  orders = client.get_orders('3678742709207')
except: 
  print('------------------------------------------------------- failed get_orders')
  i_fail += 1

try:
  line_items = client.get_line_items('7287373481448')
except: 
  print('------------------------------------------------------- failed get_line_items')
  i_fail += 1

print('testing CR & U')
print('--------------')

print('create order')
created_order = None
try:
  order = AmazonOrder()
  
  order.advertiserId = '3678742709207'
  order.name = 'amazon api test {}'.format(time.time())
  order.startDateTime = (int(time.time()) + 3600) * 1000
  order.endDateTime = (int(time.time()) + (3600 * 24 )) * 1000 # unix time * 1000
  
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
  print('------------------------------------------------------- failed create')
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
  print('------------------------------------------------------- failed update')
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
  line_item.startDateTime = (int(time.time()) + (3600 * 2)) * 1000
  line_item.endDateTime = (int(time.time()) + (3600 * 23 )) * 1000 # unix time * 1000
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
  print('------------------------------------------------------- failed create_line_item')
  i_fail += 1

print("i_fail: {}".format(i_fail))

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
  print('------------------------------------------------------- failed update')
  i_fail += 1

if updated_line_item['object']['name'] != 'updated line item':
  print('------------------------------------------------------- failed update')
  i_fail += 1
else:
  print('update success...')


try:
  print('getting Canada data')
  os.environ['AMZN_DEFAULT_PROFILE_ID'] = '4285459679297609'
  client = AmazonClient()
  client.refresh_token = os.environ['AMZN_REFRESH_TOKEN']
  client.auto_refresh_token()
  client.set_region()
  print('--- canada header ---')
  print(client.headers)
  print('--- get profiles ---')
  client.get_profiles()
  advertisers = client.get_advertisers()
  print('--- advertisers ---')
  print(advertisers)
  orders = client.get_orders('3196388450901')
  print('--- orders ---')
  print(orders)
  order = client.get_order('6458183380401')
  print('--- order 6458183380401 ---')
  print(order)
except Exception, e:
  print('------------------------------------------------------- failed Canada')
  print(e.message)
  i_fail += 1


print("\n\n\n")
print("Tests complete. {} test(s) failed.".format(i_fail))
