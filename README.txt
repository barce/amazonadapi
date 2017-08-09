# amazonadapi
Client for the Amazon Ad API

Sample code:

from amazonadapi import AmazonClient
client = AmazonClient()
client.cli_auth_dance()
client.get_profiles()
client.profile_id = 'BE_SURE_TO_SET_THIS'

# create an order
order = AmazonOrder()
order.startDateTime = 1504972206000
order.endDateTime = 1507564206000
order.advertiserId = '4609051190001'
order.name = 'API Test Created 9/9/2017 to 10/9/2017 Order'
client.create_order(order)

# create a line item
line_item = AmazonLineItem()
line_item.orderId = 'ORDER_ID'
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
client.create_line_item(line_item)

