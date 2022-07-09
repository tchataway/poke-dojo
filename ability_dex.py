from poke_env.data import POKEDEX

class AbilityDex():
    def __init__(self):
        self.ability_dex = {}

        for pokemon in POKEDEX.values():
            abilities = pokemon.get('abilities').values()

            for ability in abilities:
                ability_key = ability.lower().replace(" ", "")

                if ability_key not in self.ability_dex.keys():
                    self.ability_dex[ability_key] = ability

    def get_ability(self, key):
        if key not in self.ability_dex.keys():
            print("Key '" + key + "' not found in ability dex.")
            return key

        return self.ability_dex[key]