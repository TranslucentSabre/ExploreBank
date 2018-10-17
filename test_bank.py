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
      scanEvent = {'BodyName': 'Frey A', 'ScanType': 'Basic', 'StarType': 'AeBe'}
      self.assertTrue(self.bank.scanBody(scanEvent))
      # Remove honk value (even though we don't have a honk here)
      self.assertEqual(782, self.bank.getTotalValue())
      self.assertEqual('Added 1282 to bank for "Frey A"', self.bank.notif_string)

   def test_scan_star_detailed(self):
      locationEvent = {'StarSystem': 'Frey', 'SystemAddress': 234987234659}      
      self.bank.setLocation(locationEvent)
      discoveryEvent = {'SystemAddress': locationEvent['SystemAddress'], 'Bodies' : 14}
      self.assertTrue(self.bank.honk(discoveryEvent))
      scanEvent = {'BodyName': 'Frey A', 'ScanType': 'Detailed', 'StarType': 'AeBe'}
      self.assertTrue(self.bank.scanBody(scanEvent))
      # Remove honk value (even though we don't have a honk here)
      self.assertEqual(9577, self.bank.getTotalValue())
      self.assertEqual('Added 3077 to bank for "Frey A"', self.bank.notif_string)

   def test_scan_star_bad_star_type(self):
      locationEvent = {'StarSystem': 'Frey', 'SystemAddress': 234987234659}      
      self.bank.setLocation(locationEvent)
      discoveryEvent = {'SystemAddress': locationEvent['SystemAddress'], 'Bodies' : 14}
      self.assertTrue(self.bank.honk(discoveryEvent))
      scanEvent = {'BodyName': 'Frey A', 'ScanType': 'Detailed', 'StarType': 'AeBe', 'TerraformState': 'Terraformable'}
      self.assertFalse(self.bank.scanBody(scanEvent))
      # Ensure it's still just honk value
      self.assertEqual(7000, self.bank.getTotalValue())
      self.assertEqual('No value for "Terraformable AeBe"', self.bank.notif_string)

   def test_scan_planet_basic_non_terra(self):
      locationEvent = {'StarSystem': 'Frey', 'SystemAddress': 234987234659}      
      self.bank.setLocation(locationEvent)
      scanEvent = {'BodyName': 'Frey A 2', 'ScanType': 'Basic', 'PlanetClass': 'Water world'}
      self.assertTrue(self.bank.scanBody(scanEvent))
      # Remove honk value (even though we don't have a honk here)
      self.assertEqual(125087, self.bank.getTotalValue())
      self.assertEqual('Added 125587 to bank for "Frey A 2"', self.bank.notif_string)

   def test_scan_planet_detailed_non_terra(self):
      locationEvent = {'StarSystem': 'Frey', 'SystemAddress': 234987234659}      
      self.bank.setLocation(locationEvent)
      discoveryEvent = {'SystemAddress': locationEvent['SystemAddress'], 'Bodies' : 14}
      self.assertTrue(self.bank.honk(discoveryEvent))
      scanEvent = {'BodyName': 'Frey A 2', 'ScanType': 'Detailed', 'PlanetClass': 'Water world'}
      self.assertTrue(self.bank.scanBody(scanEvent))
      # Remove honk value 
      self.assertEqual(307910, self.bank.getTotalValue())
      self.assertEqual('Added 301410 to bank for "Frey A 2"', self.bank.notif_string)

   def test_scan_planet_basic_terra(self):
      locationEvent = {'StarSystem': 'Frey', 'SystemAddress': 234987234659}      
      self.bank.setLocation(locationEvent)
      scanEvent = {'BodyName': 'Frey A 2', 'ScanType': 'Basic', 'PlanetClass': 'Water world', 'TerraformState': 'Terraformable'}
      self.assertTrue(self.bank.scanBody(scanEvent))
      # Remove honk value (even though we don't have a honk here)
      self.assertEqual(289087, self.bank.getTotalValue())
      self.assertEqual('Added 289587 to bank for "Frey A 2"', self.bank.notif_string)

   def test_scan_planet_detailed_terra(self):
      locationEvent = {'StarSystem': 'Frey', 'SystemAddress': 234987234659}      
      self.bank.setLocation(locationEvent)
      discoveryEvent = {'SystemAddress': locationEvent['SystemAddress'], 'Bodies' : 14}
      self.assertTrue(self.bank.honk(discoveryEvent))
      scanEvent = {'BodyName': 'Frey A 2', 'ScanType': 'Detailed', 'PlanetClass': 'Water world', 'TerraformState': 'Terraformable'}
      self.assertTrue(self.bank.scanBody(scanEvent))
      # Remove honk value 
      self.assertEqual(701471, self.bank.getTotalValue())
      self.assertEqual('Added 694971 to bank for "Frey A 2"', self.bank.notif_string)

   def test_scan_planet_bad_planet_class(self):
      locationEvent = {'StarSystem': 'Frey', 'SystemAddress': 234987234659}      
      self.bank.setLocation(locationEvent)
      discoveryEvent = {'SystemAddress': locationEvent['SystemAddress'], 'Bodies' : 14}
      self.assertTrue(self.bank.honk(discoveryEvent))
      scanEvent = {'BodyName': 'Frey A 2', 'ScanType': 'Detailed', 'PlanetClass': 'TWW'}
      self.assertFalse(self.bank.scanBody(scanEvent))
      # Ensure it's still just honk value
      self.assertEqual(7000, self.bank.getTotalValue())
      self.assertEqual('No value for "TWW"', self.bank.notif_string)

   def test_scan_no_type_or_class(self):
      locationEvent = {'StarSystem': 'Frey', 'SystemAddress': 234987234659}      
      self.bank.setLocation(locationEvent)
      scanEvent = {'BodyName': 'Frey A 2', 'ScanType': 'Basic', 'PlanetClasses': 'Water world'}
      self.assertFalse(self.bank.scanBody(scanEvent))
      self.assertEqual(0, self.bank.getTotalValue())
      self.assertEqual('Body "Frey A 2" unidentifiable', self.bank.notif_string)

   def test_scan_multiple_systems(self):
      # a
      #------
      # 5 discovery - 2500
      # K Star, basic - 1216
      # Helium gas giant - 986
      # Metal rich body - 27102 
      #
      # b
      #------
      # 10 discovery - 5000
      # M Star, basic - 1208
      # Earthlike body  - 261619
      # Water giant - 760
      #
      # c
      #------
      # 2 discovery - 1000
      # N(eutron) star, basic - 22814
      # Terraformable High metal content body - 171770
      verifyDict = {'a': 30304, 'b': 267087, 'c': 194584}
      self.bank.setLocation({'StarSystem': 'a', 'SystemAddress': 1})
      self.assertTrue(self.bank.honk({'SystemAddress': 1, 'Bodies' : 5}))
      self.assertTrue(self.bank.scanBody({'BodyName': 'a', 'ScanType': 'Basic', 'StarType': 'K'}))
      self.assertTrue(self.bank.scanBody({'BodyName': 'a 2', 'ScanType': 'Basic', 'PlanetClass': 'Helium gas giant'}))
      self.assertTrue(self.bank.scanBody({'BodyName': 'a 3', 'ScanType': 'Basic', 'PlanetClass': 'Metal rich body'}))

      self.bank.setLocation({'StarSystem': 'b', 'SystemAddress': 1})
      self.assertTrue(self.bank.honk({'SystemAddress': 1, 'Bodies' : 10}))
      self.assertTrue(self.bank.scanBody({'BodyName': 'b', 'ScanType': 'Basic', 'StarType': 'M'}))
      self.assertTrue(self.bank.scanBody({'BodyName': 'b 4', 'ScanType': 'Basic', 'PlanetClass': 'Earthlike body'}))
      self.assertTrue(self.bank.scanBody({'BodyName': 'b 8', 'ScanType': 'Basic', 'PlanetClass': 'Water giant'}))

      self.bank.setLocation({'StarSystem': 'c', 'SystemAddress': 1})
      self.assertTrue(self.bank.honk({'SystemAddress': 1, 'Bodies' : 2}))
      self.assertTrue(self.bank.scanBody({'BodyName': 'c', 'ScanType': 'Basic', 'StarType': 'N'}))
      self.assertTrue(self.bank.scanBody({'BodyName': 'c 1', 'ScanType': 'Basic', 'PlanetClass': 'Terraformable High metal content body'}))

      self.assertEqual(verifyDict, self.bank.exploreBank)
      self.assertEqual(sum(verifyDict.values()), self.bank.getTotalValue())

   def test_sell_all_systems(self):
      # a
      #------
      # 5 discovery - 2500
      # K Star, basic - 1216
      # Helium gas giant - 986
      # Metal rich body - 27102 
      #
      # b
      #------
      # 10 discovery - 5000
      # M Star, basic - 1208
      # Earthlike body  - 261619
      # Water giant - 760
      #
      # c
      #------
      # 2 discovery - 1000
      # N(eutron) star, basic - 22814
      # Terraformable High metal content body - 171770
      verifyDict = {'a': 30304, 'b': 267087, 'c': 194584}
      self.bank.setLocation({'StarSystem': 'a', 'SystemAddress': 1})
      self.assertTrue(self.bank.honk({'SystemAddress': 1, 'Bodies' : 5}))
      self.assertTrue(self.bank.scanBody({'BodyName': 'a', 'ScanType': 'Basic', 'StarType': 'K'}))
      self.assertTrue(self.bank.scanBody({'BodyName': 'a 2', 'ScanType': 'Basic', 'PlanetClass': 'Helium gas giant'}))
      self.assertTrue(self.bank.scanBody({'BodyName': 'a 3', 'ScanType': 'Basic', 'PlanetClass': 'Metal rich body'}))

      self.bank.setLocation({'StarSystem': 'b', 'SystemAddress': 1})
      self.assertTrue(self.bank.honk({'SystemAddress': 1, 'Bodies' : 10}))
      self.assertTrue(self.bank.scanBody({'BodyName': 'b', 'ScanType': 'Basic', 'StarType': 'M'}))
      self.assertTrue(self.bank.scanBody({'BodyName': 'b 4', 'ScanType': 'Basic', 'PlanetClass': 'Earthlike body'}))
      self.assertTrue(self.bank.scanBody({'BodyName': 'b 8', 'ScanType': 'Basic', 'PlanetClass': 'Water giant'}))

      self.bank.setLocation({'StarSystem': 'c', 'SystemAddress': 1})
      self.assertTrue(self.bank.honk({'SystemAddress': 1, 'Bodies' : 2}))
      self.assertTrue(self.bank.scanBody({'BodyName': 'c', 'ScanType': 'Basic', 'StarType': 'N'}))
      self.assertTrue(self.bank.scanBody({'BodyName': 'c 1', 'ScanType': 'Basic', 'PlanetClass': 'Terraformable High metal content body'}))

      self.assertEqual(verifyDict, self.bank.exploreBank)
      self.assertEqual(sum(verifyDict.values()), self.bank.getTotalValue())

      self.bank.sellData({'Systems': ['a','b','c'], 'BaseValue': 500000})
      self.assertEqual('Banked value is 98.39% of reported base value.', self.bank.notif_string)

   def test_sell_some_systems(self):
      # a
      #------
      # 5 discovery - 2500
      # K Star, basic - 1216
      # Helium gas giant - 986
      # Metal rich body - 27102 
      #
      # b
      #------
      # 10 discovery - 5000
      # M Star, basic - 1208
      # Earthlike body  - 261619
      # Water giant - 760
      #
      # c
      #------
      # 2 discovery - 1000
      # N(eutron) star, basic - 22814
      # Terraformable High metal content body - 171770
      verifyDict = {'a': 30304, 'b': 267087, 'c': 194584}
      self.bank.setLocation({'StarSystem': 'a', 'SystemAddress': 1})
      self.assertTrue(self.bank.honk({'SystemAddress': 1, 'Bodies' : 5}))
      self.assertTrue(self.bank.scanBody({'BodyName': 'a', 'ScanType': 'Basic', 'StarType': 'K'}))
      self.assertTrue(self.bank.scanBody({'BodyName': 'a 2', 'ScanType': 'Basic', 'PlanetClass': 'Helium gas giant'}))
      self.assertTrue(self.bank.scanBody({'BodyName': 'a 3', 'ScanType': 'Basic', 'PlanetClass': 'Metal rich body'}))

      self.bank.setLocation({'StarSystem': 'b', 'SystemAddress': 1})
      self.assertTrue(self.bank.honk({'SystemAddress': 1, 'Bodies' : 10}))
      self.assertTrue(self.bank.scanBody({'BodyName': 'b', 'ScanType': 'Basic', 'StarType': 'M'}))
      self.assertTrue(self.bank.scanBody({'BodyName': 'b 4', 'ScanType': 'Basic', 'PlanetClass': 'Earthlike body'}))
      self.assertTrue(self.bank.scanBody({'BodyName': 'b 8', 'ScanType': 'Basic', 'PlanetClass': 'Water giant'}))

      self.bank.setLocation({'StarSystem': 'c', 'SystemAddress': 1})
      self.assertTrue(self.bank.honk({'SystemAddress': 1, 'Bodies' : 2}))
      self.assertTrue(self.bank.scanBody({'BodyName': 'c', 'ScanType': 'Basic', 'StarType': 'N'}))
      self.assertTrue(self.bank.scanBody({'BodyName': 'c 1', 'ScanType': 'Basic', 'PlanetClass': 'Terraformable High metal content body'}))

      self.assertEqual(verifyDict, self.bank.exploreBank)
      self.assertEqual(sum(verifyDict.values()), self.bank.getTotalValue())

      self.bank.sellData({'Systems': ['a','b'], 'BaseValue': 350000})
      self.assertEqual('Banked value is 84.97% of reported base value.', self.bank.notif_string)
      self.assertEqual({'c':verifyDict['c']}, self.bank.exploreBank)
      self.assertEqual(verifyDict['c'], self.bank.getTotalValue())

   def test_sell_no_systems(self):
      # a
      #------
      # 5 discovery - 2500
      # K Star, basic - 1216
      # Helium gas giant - 986
      # Metal rich body - 27102 
      #
      # b
      #------
      # 10 discovery - 5000
      # M Star, basic - 1208
      # Earthlike body  - 261619
      # Water giant - 760
      #
      # c
      #------
      # 2 discovery - 1000
      # N(eutron) star, basic - 22814
      # Terraformable High metal content body - 171770
      verifyDict = {'a': 30304, 'b': 267087, 'c': 194584}
      self.bank.setLocation({'StarSystem': 'a', 'SystemAddress': 1})
      self.assertTrue(self.bank.honk({'SystemAddress': 1, 'Bodies' : 5}))
      self.assertTrue(self.bank.scanBody({'BodyName': 'a', 'ScanType': 'Basic', 'StarType': 'K'}))
      self.assertTrue(self.bank.scanBody({'BodyName': 'a 2', 'ScanType': 'Basic', 'PlanetClass': 'Helium gas giant'}))
      self.assertTrue(self.bank.scanBody({'BodyName': 'a 3', 'ScanType': 'Basic', 'PlanetClass': 'Metal rich body'}))

      self.bank.setLocation({'StarSystem': 'b', 'SystemAddress': 1})
      self.assertTrue(self.bank.honk({'SystemAddress': 1, 'Bodies' : 10}))
      self.assertTrue(self.bank.scanBody({'BodyName': 'b', 'ScanType': 'Basic', 'StarType': 'M'}))
      self.assertTrue(self.bank.scanBody({'BodyName': 'b 4', 'ScanType': 'Basic', 'PlanetClass': 'Earthlike body'}))
      self.assertTrue(self.bank.scanBody({'BodyName': 'b 8', 'ScanType': 'Basic', 'PlanetClass': 'Water giant'}))

      self.bank.setLocation({'StarSystem': 'c', 'SystemAddress': 1})
      self.assertTrue(self.bank.honk({'SystemAddress': 1, 'Bodies' : 2}))
      self.assertTrue(self.bank.scanBody({'BodyName': 'c', 'ScanType': 'Basic', 'StarType': 'N'}))
      self.assertTrue(self.bank.scanBody({'BodyName': 'c 1', 'ScanType': 'Basic', 'PlanetClass': 'Terraformable High metal content body'}))

      self.assertEqual(verifyDict, self.bank.exploreBank)
      self.assertEqual(sum(verifyDict.values()), self.bank.getTotalValue())

      self.bank.sellData({'Systems': ['e','f','g'], 'BaseValue': 500000})
      checkString = "\n".join(
         ['System "e" not in bank',
          'System "f" not in bank',
          'System "g" not in bank',
          'Banked value is 0.00% of reported base value.'])
      self.assertEqual(checkString, self.bank.notif_string)

      

if __name__ == "__main__":
    unittest.main()
