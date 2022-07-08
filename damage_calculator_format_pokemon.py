from poke_env.data import POKEDEX
from poke_env.environment.pokemon import Pokemon
import random

class DamageCalculatorFormatPokemon():
    def __init__(
        self,
        pokemon: Pokemon
    ) -> None:
        pokedex_entry = POKEDEX[pokemon.species]
        print(pokedex_entry)
        self.species = pokedex_entry.get('name')

        if pokemon.ability is None:
            # Don't know ability, so randomly pick one from possible options.
            poss_abilities = list(pokedex_entry.get('abilities').values())
            print(poss_abilities)
            self.ability = random.choice(poss_abilities)
        else:
            self.ability = pokemon.ability

        self.item = pokemon.item
        self.level = 50

    def formatted(self):
        return {
            "species": self.species, #species name AS IT IS IN THE POKEDEX  [REQUIRED]
            "ability": self.ability, #ability [REQUIRED]
            "item": self.item,  #item [REQUIRED]
            "level": 50, #level [REQUIRED], must be a number
        }

