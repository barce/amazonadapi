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
        order = b.get_order('6198741030901')
        self.assertTrue('"msg_type": "success"', order)

    def test_get_orders(self):
        b = amazonadapi.AmazonClient()
        b.token = os.environ['AMZN_TOKEN']
        orders = b.get_orders('2631082831052')
        self.assertTrue('"msg_type": "success"', orders)

    def test_get_line_item(self):
        b = amazonadapi.AmazonClient()
        b.token = os.environ['AMZN_TOKEN']
        line_item = b.get_line_item('1590853620901')
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
        order.name = 'amazon api testsss {}'.format(time.time())
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
        new_order = json.loads(new_order)
        self.assertTrue('"msg_type": "success"', new_order)

    def test_update_order(self):
        b = amazonadapi.AmazonClient()
        b.token = os.environ['AMZN_TOKEN']
        order = b.get_order('5052675470301')
        order = json.loads(order)
        updated_order = AmazonOrder()
        updated_order.advertiserId = order['data'][0]['object']['advertiserId']['value']
        updated_order.id = order['data'][0]['object']['id']['value']
        updated_order.name = order['data'][0]['object']['name'] = 'amazon api updated test finalssss {}'.format(time.time())
        updated_order.startDateTime = order['data'][0]['object']['startDateTime']
        updated_order.endDateTime = order['data'][0]['object']['endDateTime']
        updated_order.status = order['data'][0]['object']['deliveryActivationStatus']

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
