from damage_calc_by_post import SimpleDamageCalculator
import unittest

class TestDamageCalculator(unittest.TestCase):
    def test_calc_truncated_abilities_success(self):
        calculator = SimpleDamageCalculator()

        attacker_object = {
            "species": "Bulbasaur", #species name AS IT IS IN THE POKEDEX  [REQUIRED]
            "ability": "Overgrow", #ability [REQUIRED]
            "item": "None",  #item [REQUIRED]
            "level": 50, #level [REQUIRED], must be a number
        }

        defender_object_with_sap_sipper = {
            "species": "Marill", #species name AS IT IS IN THE POKEDEX  [REQUIRED]
            "ability": "sapsipper", #ability [REQUIRED]
            "item": "None",  #item [REQUIRED]
            "level": 50, #level [REQUIRED], must be a number
        }

        defender_object_without_sap_sipper = {
            "species": "Marill", #species name AS IT IS IN THE POKEDEX  [REQUIRED]
            "ability": "hugepower", #ability [REQUIRED]
            "item": "None",  #item [REQUIRED]
            "level": 50, #level [REQUIRED], must be a number
        }

        sap_sipper_result = calculator.calculate(attacker_object, defender_object_with_sap_sipper, "Razor Leaf")
        huge_power_result = calculator.calculate(attacker_object, defender_object_without_sap_sipper, "Razor Leaf")

        self.assertEqual(0, sap_sipper_result)
        self.assertNotEqual(0, huge_power_result)

#damage_calc_tester = DamageCalculatorTests()
#damage_calc_tester.test_that_truncated_abilities_detected_successfully()