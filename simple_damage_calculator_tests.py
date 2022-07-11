from damage_calc_by_post import SimpleDamageCalculator
from showdown_team_parser import ShowdownTeamParser
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

    def test_showdown_format_parser_success(self):
        calculator = SimpleDamageCalculator()

        team = """
Milotic @ Salac Berry
Ability: Marvel Scale
Level: 50
EVs: 148 HP / 148 Def / 148 SpA
Bold Nature
- Dragon Pulse
- Hypnosis
- Hydro Pump
- Recover

Rhyperior @ Expert Belt
Ability: Solid Rock
Level: 50
EVs: 148 HP / 148 Atk / 148 SpA
Quiet Nature
- Rock Wrecker
- Ice Beam
- Thunderbolt
- Flamethrower
        """

        showdown_team_parser = ShowdownTeamParser()
        team_dict = showdown_team_parser.parse_team(team)
        print("Team Dict is:")
        print(team_dict)

        result = calculator.calculate(
            team_dict["Milotic"],
            team_dict["Rhyperior"],
            "Hydro Pump")

        self.assertTrue(result > 0)