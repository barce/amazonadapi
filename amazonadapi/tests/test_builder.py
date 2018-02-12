from unittest import TestCase

import os
import amazonadapi
from amazonadapi import *
import json


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
        # b.token = b.auto_refresh_token()['access_token']
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
