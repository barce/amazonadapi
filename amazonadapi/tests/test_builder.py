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
        self.assertTrue('"msg_type": "success"', json_profile)

    def test_get_order(self):
        b = amazonadapi.AmazonClient()
        b.token = os.environ['AMZN_TOKEN']
        order = b.get_order('7287373481448')
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
        order.name = 'amazon api test {}'.format(time.time())
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
