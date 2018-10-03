# amazonadapi
Client for the Amazon Ad API

# Notes:
# 
# The Amazon Ad API pulls only the IDs for each ad tech object.
# E.G. client.get_orders('AD_ID') just returns the order IDs.
# Take the array of order IDs and call client.get_order('ORDER_ID').
# 
order_ids = client.get_orders('AD_ID')
for order_id in order_ids:
  order = client.get_order(order_id)


# FOR ETL or automated job servers, e.g. SMP, use the following to initialize:
from amazonadapi import AmazonClient
import os
client = AmazonClient()
client.refresh_token = os.environ['AMZN_REFRESH_TOKEN']
client.auto_refresh_token()
client.set_region()
client.get_profiles()
client.profile_id = 'BE_SURE_TO_SET_THIS_FOR_YOUR_ORGANIZATION'
client.get_advertisers()
client.get_orders('AD_ID')
client.get_order('ORDER_ID')

# Sample code for using browser and command-line to auth:
from amazonadapi import AmazonClient
client = AmazonClient()
client.cli_auth_dance()
client.get_profiles()
client.profile_id = 'BE_SURE_TO_SET_THIS'


# create an order
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

# create a line item
line_item = AmazonLineItem()
line_item.orderId = 'ORDER_ID'
line_item.advertiserId = 'AD_ID'
line_item.name = 'Test API Line Item Creation'

# types: NON_GUARANTEED_DISPLAY,NON_GUARANTEED_MOBILE_APP,NON_GUARANTEED_VIDEO
line_item.type = 'NON_GUARANTEED_DISPLAY'

line_item.startDateTime = 1506873006000
line_item.endDateTime = 1507045806000
line_item.status = 'INACTIVE'
line_item.budget['amount'] = 100
line_item.budget['deliveryProfile'] = 'FRONTLOADED'
line_item.budget['deliveryBuffer'] = 1

# recurrenceTypes: DAILY, MONTHLY, LIFETIME
line_item.deliveryCaps.append({'amount': 0.9, 'recurrenceType': 'DAILY'})

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

result = client.create_line_item(hashline_item)
client.create_line_item(hashline_item)

