from poke_env.data import POKEDEX
from poke_env.environment.pokemon import Pokemon
from ability_dex import AbilityDex
import random

class UtilityFunctions():
    def move_targets_single_pokemon(self, move_target: str):
        match move_target:
            case "adjacentAlly":
                return True
            case "adjacentAllyOrSelf":
                return True
            case "adjacentFoe":
                return True
            case "any":
                return True
            case "normal":
                return True
            case "randomNormal":
                return True
            case "scripted":
                return True
            case "self":
                return True

        return False

    def get_or_guess_ability(self, pokemon):
        pokedex_entry = POKEDEX[pokemon.species]
        poss_abilities = list(pokedex_entry.get('abilities').values())
        ability = None

        if pokemon.ability is None:
            # Don't know ability, so randomly pick one from possible options for
            # species.
            random_ability = random.choice(poss_abilities)
            ability = random_ability
        else:
            # poke_env Pokemon have condensed ability IDs, but the damage
            # calculator needs the verbose version, so convert that here.
            ability_dex = AbilityDex()
            ability = ability_dex.get_ability(pokemon.ability)

        return ability

    def is_move_negated_by_ability(self, move, user_ability, target_ability):
        print(move)
        print(user_ability)
        print(target_ability)
        if user_ability == "Mold Breaker":
            # Mold Breaker ignores target's ability.
            return False

        if move.volatile_status == "confusion" and target_ability == "Own Tempo":
            return True

        if move.volatile_status == "attract" and target_ability == "Oblivious":
            return True

        return False