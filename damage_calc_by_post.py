import requests
import random

class SimpleDamageCalculator():
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
        #payload = { 'attacker': attackerObject, 'defender': attackerObject, 'move': move }
        result = requests.post(url, json = payload)
        jsonResult = result.json()
        print(jsonResult)

        if 'error' in jsonResult:
            # Something went wrong. Print error and return 0.
            print (jsonResult['error'])
            return 0

        return random.choice(jsonResult['damage'])