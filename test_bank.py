#!/usr/bin/env python2
import unittest
from explore_bank import ExploreBank

class exploreBankTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.bank = ExploreBank() 

    def setUp(self):
        self.bank.clearBank()

    def test_empty_bank(self):
        self.assertEqual(0, self.bank.getTotalValue())

if __name__ == "__main__":
    unittest.main()
