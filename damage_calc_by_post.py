import requests
import random

class SimpleDamageCalculator():
    # Expected format:
#    attackerObject = {
#    "species": "Serperior", //species name AS IT IS IN THE POKEDEX  [REQUIRED]
#    "ability": "Contrary", //ability [REQUIRED]
#    "item": "Leftovers",  //item [REQUIRED]
#    "level": 100, //level [REQUIRED], must be a number
#    "nature": "Modest", //not required, defaults to serious
#    "evs": {"spa": 252, "spe": 252},  //not required, defaults to 0 in all stats. Valid stats are "hp", "atk", "spa", "def", "spd", "spe"
#    "ivs": {"atk": 0} //not required, defaults to 31 in any stat not specified
#}
    def calculate(self, attacker, defender, move):
        #attackerObject = {
        #    "species": attacker.species, #species name AS IT IS IN THE POKEDEX  [REQUIRED]
        #    "ability": attacker.ability, #ability [REQUIRED]
        #    "item": attacker.item,  #item [REQUIRED]
        #    "level": 50, #level [REQUIRED], must be a number
        #}

        #defenderObject = {
        #    "species": defender.species, #species name AS IT IS IN THE POKEDEX  [REQUIRED]
        #    "ability": defender.ability, #ability [REQUIRED]
        #    "item": defender.item,  #item [REQUIRED]
        #    "level": 50, #level [REQUIRED], must be a number
        #}

        print(attacker)
        print(defender)
        url = "https://calc-api.herokuapp.com/calc-api"
        payload = { 'attacker': attacker, 'defender': defender, 'move': move }
        result = requests.post(url, json = payload)
        jsonResult = result.json()
        print(jsonResult)

        if 'error' in jsonResult:
            # Something went wrong. Print error and return 0.
            print (jsonResult['error'])
            return 0

        return random.choice(jsonResult['damage'])

    def check_for_error(self, attacker, defender, move):
        url = "https://calc-api.herokuapp.com/calc-api"
        payload = { 'attacker': attacker, 'defender': defender, 'move': move }
        result = requests.post(url, json = payload)
        jsonResult = result.json()

        if 'error' in jsonResult:
            # Something went wrong. Print error and return 0.
            return jsonResult['error']

        return "OK"