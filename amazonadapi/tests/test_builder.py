from unittest import TestCase

import os
import amazonadapi
from amazonadapi import AmazonClient


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

    
