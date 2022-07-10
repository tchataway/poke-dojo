from damage_calc_by_post import SimpleDamageCalculator
import unittest

class TestDamageCalculator(unittest.TestCase):
    def test_calc_abilities_affect_damage_success(self):
        calculator = SimpleDamageCalculator()

        attacker_object = {
            "species": "Bulbasaur", #species name AS IT IS IN THE POKEDEX  [REQUIRED]
            "ability": "Overgrow", #ability [REQUIRED]
            "item": "None",  #item [REQUIRED]
            "level": 50, #level [REQUIRED], must be a number
        }

        defender_object_with_sap_sipper = {
            "species": "Marill", #species name AS IT IS IN THE POKEDEX  [REQUIRED]
            "ability": "Sap Sipper", #ability [REQUIRED]
            "item": "None",  #item [REQUIRED]
            "level": 50, #level [REQUIRED], must be a number
        }

        defender_object_without_sap_sipper = {
            "species": "Marill", #species name AS IT IS IN THE POKEDEX  [REQUIRED]
            "ability": "Huge Power", #ability [REQUIRED]
            "item": "None",  #item [REQUIRED]
            "level": 50, #level [REQUIRED], must be a number
        }

        sap_sipper_result = calculator.calculate(attacker_object, defender_object_with_sap_sipper, "Razor Leaf")
        huge_power_result = calculator.calculate(attacker_object, defender_object_without_sap_sipper, "Razor Leaf")

        self.assertEqual(sap_sipper_result, 0)
        self.assertNotEqual(huge_power_result, 0)

    def test_calc_items_affect_damage_success(self):
        calculator = SimpleDamageCalculator()

        attacker_object = {
            "species": "Gliscor", #species name AS IT IS IN THE POKEDEX  [REQUIRED]
            "ability": "Poison Heal", #ability [REQUIRED]
            "item": "None",  #item [REQUIRED]
            "level": 50, #level [REQUIRED], must be a number
        }

        defender_object_with_air_balloon = {
            "species": "Marill", #species name AS IT IS IN THE POKEDEX  [REQUIRED]
            "ability": "Huge Power", #ability [REQUIRED]
            "item": "Air Balloon",  #item [REQUIRED]
            "level": 50, #level [REQUIRED], must be a number
        }

        defender_object_without_air_balloon = {
            "species": "Marill", #species name AS IT IS IN THE POKEDEX  [REQUIRED]
            "ability": "Huge Power", #ability [REQUIRED]
            "item": "None",  #item [REQUIRED]
            "level": 50, #level [REQUIRED], must be a number
        }

        air_balloon_result = calculator.calculate(attacker_object, defender_object_with_air_balloon, "Earthquake")
        without_air_balloon_result = calculator.calculate(attacker_object, defender_object_without_air_balloon, "Earthquake")

        self.assertEqual(air_balloon_result, 0)
        self.assertNotEqual(without_air_balloon_result, 0)