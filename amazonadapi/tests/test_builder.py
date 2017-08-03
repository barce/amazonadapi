from unittest import TestCase

import amazonadapi
from amazonadapi import AmazonClient


class TestAmazonClient(TestCase):
    def test_config(self):
        b = amazonadapi.AmazonClient()
        self.assertTrue(isinstance(b, AmazonClient))

    # assumes primed connection
    def test_profiles(self):
        b = amazonadapi.AmazonClient()
        json_profile = b.profiles()
        self.assertTrue('USD', json_profile[0]['currencyCode'])

    
