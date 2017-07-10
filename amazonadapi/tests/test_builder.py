from unittest import TestCase

import aopclient
from aopclient import AOLClient


class TestAOLClient(TestCase):
    def test_config(self):
        b = aopclient.AOLClient()
        self.assertTrue(isinstance(b, AOLClient))
