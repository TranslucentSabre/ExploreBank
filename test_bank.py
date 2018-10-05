#!/usr/bin/env python2
import unittest
from explore_bank import ExploreBank, BODIES

class exploreBankTest(unittest.TestCase):

   @classmethod
   def setUpClass(cls):
      cls.bank = ExploreBank() 
      
   def setUp(self):
      self.bank.clearBank()
      self.bank.honkValue = 500

   def test_empty_bank(self):
      self.assertEqual(0, self.bank.getTotalValue())

   def test_write_read_db_file_later(self):
      self.bank.exploreBank = { "a" : 1234134, "b": 9238473, "c": 239847 }
      self.assertEqual(10712454, self.bank.getTotalValue())
      self.bank.writeHardBank()
      self.bank = None
      self.bank = ExploreBank(readLater=True)
      self.assertEqual(0, self.bank.getTotalValue())
      self.bank.readHardBank()
      self.assertEqual(10712454, self.bank.getTotalValue())
      
   def test_write_read_db_file_now(self):
      self.bank.exploreBank = { "a" : 1234134, "b": 9238473, "c": 239847 }
      self.assertEqual(10712454, self.bank.getTotalValue())
      self.bank.writeHardBank()
      self.bank = None
      self.bank = ExploreBank()
      self.assertEqual(10712454, self.bank.getTotalValue())
      
   def test_set_location(self):
      event = {'StarSystem': 'Tz Aerietis', 'SystemAddress': 1234}
      self.bank.setLocation(event)
      self.assertEqual('Tz Aerietis', self.bank.currentSystemName)
      self.assertEqual(1234, self.bank.currentSystemAddress)
      self.assertEqual("New system, Tz Aerietis, entered.", self.bank.notif_string)
      event = {'StarSystem': 'Frey', 'SystemAddress': 234987234659}
      self.bank.setLocation(event)
      self.assertEqual('Frey', self.bank.currentSystemName)
      self.assertEqual(234987234659, self.bank.currentSystemAddress)
      self.assertEqual("New system, Frey, entered.", self.bank.notif_string)

   def test_discovery_scan_valid(self):
      locationEvent = {'StarSystem': 'Frey', 'SystemAddress': 234987234659}      
      self.bank.setLocation(locationEvent)
      discoveryEvent = {'SystemAddress': locationEvent['SystemAddress'], 'Bodies' : 14}
      self.assertTrue(self.bank.honk(discoveryEvent))
      self.assertEqual(7000, self.bank.getTotalValue())
      self.assertEqual("Discovery scan in Frey", self.bank.notif_string)

   def test_discovery_scan_valid_changed_value(self):
      self.bank.honkValue = 1000
      locationEvent = {'StarSystem': 'Frey', 'SystemAddress': 234987234659}      
      self.bank.setLocation(locationEvent)
      discoveryEvent = {'SystemAddress': locationEvent['SystemAddress'], 'Bodies' : 14}
      self.assertTrue(self.bank.honk(discoveryEvent))
      self.assertEqual(14000, self.bank.getTotalValue())
      self.assertEqual("Discovery scan in Frey", self.bank.notif_string)

   def test_discovery_scan_invalid(self):
      locationEvent = {'StarSystem': 'Tz Aerietis', 'SystemAddress': 1234}
      self.bank.setLocation(locationEvent)
      discoveryEvent = {'SystemAddress': 234987234659, 'Bodies' : 14}
      self.assertFalse(self.bank.honk(discoveryEvent))
      self.assertEqual(0, self.bank.getTotalValue())
      self.assertEqual("This scan is not in our current system, no value added.", self.bank.notif_string)

   def test_scan_star_basic(self):
      locationEvent = {'StarSystem': 'Frey', 'SystemAddress': 234987234659}      
      self.bank.setLocation(locationEvent)
      scanEvent = {'Bodyname': 'Frey A', 'ScanType': 'Basic', 'StarType': 'AeBe'}
      self.assertTrue(self.bank.scanBody(scanEvent))
      # Remove honk value (even though we don't have a honk here)
      self.assertEqual(782, self.bank.getTotalValue())
      self.assertEqual('Added 1282 to bank for "Frey A"', self.bank.notif_string)


if __name__ == "__main__":
    unittest.main()
