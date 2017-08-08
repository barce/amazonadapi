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
order.startDateTime = 1502164800000
order.endDateTime = 1502251140000
order.advertiserId = '4609051190001'
order.name = 'API Test Created Order'
client.create_order(order)

# create a line item
line_item = AmazonLineItem()
line_item.orderId = '5727422190201'
line_item.name = 'Test API Line Item Creation'
line_item.type = 'NON GUARANTEED DISPLAY'
line_item.startDateTime = 1502164800000
line_item.endDateTime = 1502251140000
line_item.status = 'INACTIVE'
line_item.budget['amount'] = 0.8
line_item.budget['deliveryProfile'] = 'FRONTLOADED'
line_item.budget['deliveryBuffer'] = 1
line_item.deliveryCaps['amount'] = 0.8
line_item.deliveryCaps['recurrenceType'] = 'DAILY'
client.create_line_item(line_item)

