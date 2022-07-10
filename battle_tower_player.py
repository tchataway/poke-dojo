from poke_env.environment.effect import Effect
from poke_env.environment.move_category import MoveCategory
from poke_env.environment.field import Field
from poke_env.environment.pokemon_gender import PokemonGender
from poke_env.player.player import Player
from damage_calc_by_post import SimpleDamageCalculator
from poke_env.data import MOVES
from poke_env.data import POKEDEX
from damage_calculator_format_pokemon import DamageCalculatorFormatPokemon
from utils import UtilityFunctions
import random
import math

class BattleTowerPlayer(Player):
    def choose_move(self, battle):
        # switch if about to faint due to Perish Song
        if Effect.PERISH1 in battle.active_pokemon.effects:
            if battle.available_switches:
                self.logger.debug("Found perish1, switching")
                return self.create_order(random.choice(battle.available_switches))

        preferred_moves = [] # preferred moves are the tactical chefs' kiss. If
                             # any moves are in this list after assessing options,
                             # one of them will be chosen.
        status_moves = [] # Any status category moves (moves that don't deal damage)
        preferred_status_moves = [] # Moves like Attract, Will-O-Wisp, etc.

        damage_calculator = SimpleDamageCalculator()
        if battle.available_moves:
            print(battle.available_moves)
            active_formatter = DamageCalculatorFormatPokemon(battle.active_pokemon)
            opponent_formatter = DamageCalculatorFormatPokemon(battle.opponent_active_pokemon)

            best_move = random.choice(battle.available_moves)
            best_damage = 0
            for move in battle.available_moves:
                if move.current_pp == 0:
                    # Skip if out of PP.
                    continue

                if move.id not in MOVES.keys():
                    # Might be a forced "move" like recharging after a Hyper Beam
                    continue

                # Special handling for status moves.
                if move.category == MoveCategory.STATUS:
                    # If it's a move we can use, add it to status moves list.
                    
                    if Effect.TAUNT in battle.active_pokemon.effects:
                        # Can't use status moves while taunted.
                        continue

                    if move.heal > 0:
                        # Heal logic is handled elsewhere.
                        continue

                    if move.target != "self" and not self.move_works_against_target(move, battle.active_pokemon, battle.opponent_active_pokemon):
                        # Skip if move targets a foe but foe is immune to it.
                        continue
                    elif move.target == "self" and not self.move_works_against_target(move, battle.active_pokemon, battle.active_pokemon):
                        # Skip if we can't use move on ourself (e.g. Substitute while Substitute is active)
                        continue

                    if move.weather != None and move.weather in battle.weather.keys():
                        # Don't use weather move if weather for move already active.
                        continue

                    if move.pseudo_weather != None and self.is_pseudo_weather_in_fields(move.pseudo_weather, battle.fields):
                        # E.g. don't use Trick Room when it's already up.
                        continue

                    if move.status != None or move.volatile_status != None:
                        # If we have one of these and got to this point,
                        # we want to use it over everything except preferred
                        # moves and staying alive.
                        preferred_status_moves.append(move)
                        continue

                    status_moves.append(move)
                    continue

                if move.id == "fakeout" and not battle.active_pokemon.first_turn:
                    # Fake Out only works on the first turn, so skip.
                    continue

                print("Simulating damage rolls...")
                move_name = MOVES[move.id].get("name", None)
                print("Simulating damage for " + move_name)
                simulated_damage = 0

                # Check for calculated or fixed damage.
                if move.damage == "level":
                    simulated_damage = battle.opponent_active_pokemon.level
                elif move.damage > 0:
                    simulated_damage = move.damage
                else:
                    simulated_damage = damage_calculator.calculate(active_formatter.formatted(), opponent_formatter.formatted(), move_name)

                print("Damage simulated was " + str(simulated_damage))

                if simulated_damage > self.guess_current_hp(battle.opponent_active_pokemon):
                    # Does this move knock out our opponent? If so, add to preferred moves.
                    preferred_moves.append(move)

                if simulated_damage > best_damage:
                    print("Which is greater than current best, which was " + str(best_damage) + ", updating best move to " + move_name)
                    best_damage = simulated_damage
                    best_move = move

            if len(preferred_moves) > 0:
                print("Selecting a potential KO move from " + str(len(preferred_moves)) + " preferred moves:")
                print(preferred_moves)
                return self.create_order(random.choice(preferred_moves))

            # We don't see any potential KOs at present, so combine best damage move
            # with status moves into a single pool and set that as our current
            # best move.
            move_options = status_moves
            move_options.append(best_move)
            print("Move options at this point are ")
            print(move_options)
            best_move = random.choice(move_options)
            print("Randomly selected " + best_move.id + " from move options")            

            if battle.active_pokemon.current_hp_fraction < 0.5:
                # We're damaged; check for healing moves.
                print("Below 50% HP; checking for healing moves...")
                best_heal = 0
                best_heal_move = random.choice(battle.available_moves)
                for move in battle.available_moves:
                    if move.current_pp == 0:
                        continue

                    if move.heal > best_heal:
                        best_heal_move = move
                        best_heal = move.heal

                if best_heal > 0:
                    print("Determined " + MOVES[best_heal_move.id].get("name", None) + " is best heal, using it.")
                    return self.create_order(best_heal_move)

            if len(preferred_status_moves) > 0:
                return self.create_order(random.choice(preferred_status_moves))

            return self.create_order(best_move)
        # If no attack is available, a random switch will be made
        else:
            return self.choose_random_move(battle)

    def teampreview(self, battle):
        return "/team 123"

    def guess_current_hp(self, pokemon):
        print("Guessing " + pokemon.species + "'s current HP.")
        max_hp = self.guess_max_hp(pokemon)
        print("Max HP (guess): " + str(max_hp))
        current_hp =  (pokemon.current_hp_fraction) * max_hp
        print("Current HP (guess): " + str(current_hp))
        return current_hp

    def guess_max_hp(self, pokemon):
        pokedex_entry = POKEDEX[pokemon.species];
        hp_base = pokedex_entry.get('baseStats').get('hp')
        return math.floor(0.01 * (2 * hp_base + 31 + math.floor(0.25 * 0)) * pokemon.level) + pokemon.level + 10

    def move_works_against_target(self, move, user, target):
        if move.status is not None and target.status is not None:
            # Pokemon can only have one major status ailment at a time.
            return False

        if move.volatile_status is not None:
            # E.g. confusion, taunted, leech seed -- can't have same one twice.
            target_effects = list(target.effects.keys())
            for effect in target_effects:
                if effect.name == move.volatile_status.upper(): # TODO: Implement better conversion for volatile status IDs
                    return False
                
            # Singles only, so follow me won't work either.
            if move.volatile_status == "followme":
                return False

        if not (target.damage_multiplier(move) > 0):
            # Move doesn't work due to typing.
            return False

        print("Checking abilities...")
        utils = UtilityFunctions()
        if utils.is_move_negated_by_ability(move,
            utils.get_or_guess_ability(user),
            utils.get_or_guess_ability(target)):
            return False

        # TODO: Check item.
        
        if move.volatile_status == "attract" and not self.genders_are_attract_compatible(user.gender, target.gender):
            return False

        utils = UtilityFunctions()
        if move.target != "self" and Effect.SUBSTITUTE in list(target.effects.keys()):
            if move.category == MoveCategory.STATUS and utils.move_targets_single_pokemon(move.target):
                # Status moves don't work on substitutes of other Pokemon.
                return False

        return True

    def genders_are_attract_compatible(self, gender1, gender2):
        if gender1 == PokemonGender.MALE:
            return gender2 == PokemonGender.FEMALE

        if gender1 == PokemonGender.FEMALE:
            return gender2 == PokemonGender.MALE

        return False

    def is_pseudo_weather_in_fields(self, pseudo_weather, fields):
        for field in fields.keys():
            if pseudo_weather == self.id_from_field(field):
                return True

        return False

    def id_from_field(self, field):
        field_text = field.name
        field_text = field_text.lower()
        return field_text.replace("_", "")