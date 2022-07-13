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

        if target_ability == "Oblivious":
            if move.volatile_status == "attract":
                return True
            if move.volatile_status == "taunt":
                return True

        return False

    def move_heals_user(self, move):
        return move.heal > 0 or "heal" in move.flags

    def move_drops_target_speed(self, move):
        if move.target == "self":
            return False

        move_affects_speed_primary = move.boosts != None and "spe" in move.boosts.keys()
        move_affects_speed_secondary = len(move.secondary) > 0 and move.secondary[0].get("boosts", None) != None and "spe" in move.secondary[0].get("boosts").keys()

        if not move_affects_speed_primary and not move_affects_speed_secondary:
            return False

        primary_boost = 0
        secondary_boost = 0

        if move_affects_speed_primary:
            primary_boost = move.boosts["spe"]

        if move_affects_speed_secondary:
            secondary_boost = move.secondary[0].get("boosts")["spe"]

        if not primary_boost < 0 and not secondary_boost < 0:
            # Doesn't debuff speed.
            return False

        if move_affects_speed_secondary and move.secondary[0].get("chance") < 100:
            return False

        return True

    def calculate_stat_fraction(self, stage: int):
        if stage < -6 or stage > 6:
            return [2, 2]

        nominator = 2
        denominator = 2

        if stage < 0:
            denominator = denominator + abs(stage)
        else:
            nominator = nominator + stage

        return [nominator, denominator]

    def get_iv_from_stat_block(self, stat_block, stat: str):
        ivs = {}
        iv = 31
        
        if "ivs" in stat_block.keys():
            ivs = stat_block["ivs"]

        if stat in ivs.keys():
            iv = int(ivs[stat])

        return iv

    def get_ev_from_stat_block(self, stat_block, stat: str):
        evs = {}
        ev = 0
        
        if "evs" in stat_block.keys():
            evs = stat_block["evs"]

        if stat in evs.keys():
            ev = int(evs[stat])

        return ev

    def get_mod_for_nature(self, nature: str, stat: str):
        # I'm really lazy so I'm only checking speed for now. What? It's late!
        match stat:
            case "spe":
                match nature:
                    case "Timid":
                        return 1.1
                    case "Jolly":
                        return 1.1
                    case "Hasty":
                        return 1.1
                    case "Naive":
                        return 1.1
                    case "Brave":
                        return 0.9
                    case "Relaxed":
                        return 0.9
                    case "Quiet":
                        return 0.9
                    case "Sassy":
                        return 0.9

        return 1.0

    def move_does_no_damage(self, move):
        print("Checking if move does damage...")
        if move.damage == 0 and move.base_power == 0:
            print("Move does not do damage.")
            return True

        print("Move does damage.")
        return False

    def is_useable_setup_move(self, user, move):
        if move.target != "self":
            return False

        if move.boosts is None:
            return False

        attack_boost = 0
        special_attack_boost = 0

        if "atk" in move.boosts.keys():
            attack_boost = move.boosts["atk"]

        if "spa" in move.boosts.keys():
            special_attack_boost = move.boosts["spa"]

        if attack_boost < 1 and special_attack_boost < 1:
            return False

        user_attack_stage = 0
        user_special_attack_stage = 0

        if "atk" in user.boosts.keys():
            user_attack_stage = user.boosts["atk"]

        if "spa" in user.boosts.keys():
            user_special_attack_stage = user.boosts["spa"]        

        boosted_atk = min(user_attack_stage + attack_boost, 6)
        boosted_spa = min(user_special_attack_stage + special_attack_boost, 6)

        if boosted_atk == user_attack_stage and boosted_spa == user_special_attack_stage:
            # In other words, would boosting effectively do nothing at all to either
            # stat?
            return False

        return True