from unittest import TestCase

import os
import amazonadapi
from amazonadapi import *
import json
import time

class TestAmazonClient(TestCase):

    def test_config(self):
        b = amazonadapi.AmazonClient()
        self.assertTrue(isinstance(b, AmazonClient))

    # assumes primed connection
    def test_profiles(self):
        b = amazonadapi.AmazonClient()
        b.token = os.environ['AMZN_TOKEN']
        json_profile = b.get_profiles()
        json_profile = json.loads(json_profile)
        self.assertTrue('"msg_type": "success"', json_profile)

    def test_get_order(self):
        b = amazonadapi.AmazonClient()
        b.token = os.environ['AMZN_TOKEN']
        order = b.get_order('6817318700601')
        self.assertTrue('"msg_type": "success"', order)

    def test_get_orders(self):
        b = amazonadapi.AmazonClient()
        b.token = os.environ['AMZN_TOKEN']
        orders = b.get_orders('2631082831052')
        self.assertTrue('"msg_type": "success"', orders)

    def test_get_line_item(self):
        b = amazonadapi.AmazonClient()
        b.token = os.environ['AMZN_TOKEN']
        line_item = b.get_line_item('4979603200301')
        self.assertTrue('"msg_type": "success"', line_item)

    def test_get_line_items(self):
        b = amazonadapi.AmazonClient()
        b.token = os.environ['AMZN_TOKEN']
        line_items = b.get_line_items('7287373481448')
        self.assertTrue('"msg_type": "success"', line_items)

    def test_get_advertisers(self):
        b = amazonadapi.AmazonClient()
        b.token = os.environ['AMZN_TOKEN']
        advertisers = b.get_advertisers()
        self.assertTrue('"msg_type": "success"', advertisers)

    def test_create_order(self):
        b = amazonadapi.AmazonClient()
        b.token = os.environ['AMZN_TOKEN']
        order = AmazonOrder()
        order.advertiserId = '3678742709207'
        order.name = 'amazon api testssss {}'.format(time.time())
        order.startDateTime = (int(time.time()) + 3600) * 1000
        order.endDateTime = (int(time.time()) + (3600 * 24)) * 1000  # unix time * 1000

        hash_order = {
            "object": {
                "advertiserId": {
                    "value": order.advertiserId
                },
                "name": order.name,
                "startDateTime": order.startDateTime,
                "endDateTime": order.endDateTime,
                "deliveryActivationStatus": order.status
            }
        }

        new_order = b.create_order(hash_order)
        self.assertTrue('"msg_type": "success"', new_order)

    def test_update_order(self):
        b = amazonadapi.AmazonClient()
        b.token = os.environ['AMZN_TOKEN']
        order = b.get_order('3135287630501')
        order = json.loads(order)
        updated_order = AmazonOrder()
        updated_order.advertiserId = order['data']['object']['advertiserId']['value']
        updated_order.id = order['data']['object']['id']['value']
        updated_order.name = order['data']['object']['name'] = 'amazon api updated test finalssss {}'.format(time.time())
        updated_order.startDateTime = order['data']['object']['startDateTime']
        updated_order.endDateTime = order['data']['object']['endDateTime']
        updated_order.status = order['data']['object']['deliveryActivationStatus']

        hash_order = {
            "object": {
                "advertiserId": {
                    "value": updated_order.advertiserId
                },
                "id": {
                    "value": updated_order.id
                },
                "name": updated_order.name,
                "startDateTime": updated_order.startDateTime,
                "endDateTime": updated_order.endDateTime,
                "deliveryActivationStatus": updated_order.status
            }
        }
        new_order = b.update_order(hash_order)
        self.assertTrue('"msg_type": "success"', new_order)

    def test_create_line_item(self):
        b = amazonadapi.AmazonClient()
        b.token = os.environ['AMZN_TOKEN']
        line_item = AmazonLineItem()
        line_item.orderId = '3135287630501'
        line_item.name = 'aruns test line item'
        line_item.type = 'NON_GUARANTEED_DISPLAY'
        line_item.startDateTime = 1518709035000
        line_item.endDateTime = 1518791835000
        line_item.status = 'INACTIVE'
        line_item.budget = {
            "amount": 3090.0,
            "deliveryProfile": 'EVENLY'
        }
        hash_order = {
            "object": {
                    "orderId": {
                        "value": line_item.orderId
                    },
                    "name": line_item.name,
                    "type": line_item.type,
                    "startDateTime": line_item.startDateTime,
                    "endDateTime": line_item.endDateTime,
                    "deliveryActivationStatus": line_item.status,
                    "budget": line_item.budget
                }
            }

        new_line_item = b.create_line_item(hash_order)
        self.assertTrue('"msg_type": "success"', new_line_item)

    def test_update_line_item(self):
        b = amazonadapi.AmazonClient()
        b.token = os.environ['AMZN_TOKEN']
        line_item = b.get_line_item('1590853620901')
        line_item = json.loads(line_item)
        updated_line_item = AmazonLineItem()
        updated_line_item.orderId = line_item['data']['object']['orderId']['value']
        updated_line_item.id = line_item['data']['object']['id']['value']
        updated_line_item.name = 'aruns test line item final!!!!'
        updated_line_item.type = line_item['data']['object']['type']
        updated_line_item.startDateTime = line_item['data']['object']['startDateTime']
        updated_line_item.endDateTime = line_item['data']['object']['endDateTime']
        updated_line_item.status = 'INACTIVE'

        hash_order = {
            "object": {
                "orderId": {
                    "value": updated_line_item.orderId
                },
                "id": {
                    "value": updated_line_item.id
                },
                "name": updated_line_item.name,
                "type": updated_line_item.type,
                "startDateTime": updated_line_item.startDateTime,
                "endDateTime": updated_line_item.endDateTime,
                "deliveryActivationStatus": updated_line_item.status
            }
        }

        new_line_item = b.update_line_item(hash_order)
        self.assertTrue('"msg_type": "success"', new_line_item)


