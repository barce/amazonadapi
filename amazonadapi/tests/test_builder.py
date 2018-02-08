from unittest import TestCase

import os
import amazonadapi
from amazonadapi import *


class TestAmazonClient(TestCase):
    def test_config(self):
        b = amazonadapi.AmazonClient()
        self.assertTrue(isinstance(b, AmazonClient))

    # assumes primed connection
    def test_profiles(self):
        b = amazonadapi.AmazonClient()
        b.token = os.environ['AMZN_TOKEN']
        json_profile = b.get_profiles()
        self.assertTrue('USD', json_profile[0]['currencyCode'])

    def test_get_order(self):
        b = amazonadapi.AmazonClient()
        # get api token that was set by auto_refresh_token()
        b.token = os.environ['AMZN_TOKEN']
        order = b.get_order('7287373481448')
        self.assertTrue('success', order['msg_type'])

