from unittest import TestCase

import amazonadapi
from amazonadapi import AmazonClient


class TestAmazonClient(TestCase):
    def test_config(self):
        b = amazonadapi.AmazonClient()
        self.assertTrue(isinstance(b, AmazonClient))
