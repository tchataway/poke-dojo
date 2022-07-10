from poke_env.data import POKEDEX
from poke_env.environment.pokemon import Pokemon
from ability_dex import AbilityDex
import random

class DamageCalculatorFormatPokemon():
    def __init__(
        self,
        pokemon: Pokemon
    ) -> None:
        pokedex_entry = POKEDEX[pokemon.species]
        print(pokedex_entry)
        self.species = pokedex_entry.get('name')
        poss_abilities = list(pokedex_entry.get('abilities').values())

        if pokemon.ability is None:
            # Don't know ability, so randomly pick one from possible options.
            print(poss_abilities)
            random_ability = random.choice(poss_abilities)
            print("Randomly selected " + random_ability)
            self.ability = random_ability
        else:
            # poke_env Pokemon have condensed ability IDs, but the damage calculator
            # needs the verbose version, so convert that here.
            ability_dex = AbilityDex()
            self.ability = ability_dex.get_ability(pokemon.ability)

        if pokemon.item is None:
            # API requires a non-null value for hold item.
            self.item = "no_item"
        else:
            self.item = pokemon.item

        self.level = 50

    def formatted(self):
        return {
            "species": self.species, #species name AS IT IS IN THE POKEDEX  [REQUIRED]
            "ability": self.ability, #ability [REQUIRED]
            "item": self.item,  #item [REQUIRED]
            "level": 50, #level [REQUIRED], must be a number
        }

