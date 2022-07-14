from poke_env.environment.effect import Effect
from poke_env.environment.status import Status
from poke_env.environment.move_category import MoveCategory
from poke_env.environment.field import Field
from poke_env.environment.pokemon_gender import PokemonGender
from poke_env.player.player import Player
from poke_env.player_configuration import PlayerConfiguration
from poke_env.server_configuration import ServerConfiguration
from poke_env.teambuilder.teambuilder import Teambuilder
from damage_calc_by_post import SimpleDamageCalculator
from poke_env.data import MOVES
from poke_env.data import POKEDEX
from damage_calculator_format_pokemon import DamageCalculatorFormatPokemon
from showdown_team_parser import ShowdownTeamParser
from utils import UtilityFunctions
import random
import math
from typing import Optional, Union
from os import listdir
from os.path import isfile, join
import os.path

class BattleTowerPlayer(Player):
    def __init__(
        self,
        player_configuration: Optional[PlayerConfiguration] = None,
        *,
        avatar: Optional[int] = None,
        battle_format: Optional[str] = None,
        log_level: Optional[int] = None,
        max_concurrent_battles: int = 1,
        save_replays: Union[bool, str] = False,
        server_configuration: Optional[ServerConfiguration] = None,
        start_timer_on_battle_start: bool = False,
        start_listening: bool = True,
        team: Optional[Union[str, Teambuilder]] = None,
    ):
        # Cache our own team deets for use in damage calculation later.
        showdown_team_parser = ShowdownTeamParser()
        self.team_directory = showdown_team_parser.parse_team(team)
        self.opponent_team_directory = {}
        self.active_pokemon_turn_counter = 0
        self.utility_functions = UtilityFunctions()

        super().__init__(
            player_configuration=player_configuration,
            avatar=avatar,
            battle_format=battle_format,
            log_level=log_level,
            max_concurrent_battles=max_concurrent_battles,
            save_replays=save_replays,
            server_configuration=server_configuration,
            start_timer_on_battle_start=start_timer_on_battle_start,
            start_listening=start_listening,
            team=team,
        )

    def choose_move(self, battle):
        self.active_pokemon_turn_counter = self.active_pokemon_turn_counter + 1
        # switch if about to faint due to Perish Song
        if Effect.PERISH1 in battle.active_pokemon.effects:
            if battle.available_switches:
                self.logger.debug("Found perish1, switching")
                return self.create_order(random.choice(battle.available_switches))

        top_priority_moves = [] # preferred moves are the tactical chefs' kiss. If
                             # any moves are in this list after assessing options,
                             # one of them will be chosen.
        status_moves = [] # Any status category moves (moves that don't deal damage)
        high_priority_moves = [] # Moves like Attract, Will-O-Wisp, etc.

        damage_calculator = SimpleDamageCalculator()
        if battle.available_moves:
            print(battle.available_moves)
            active_pokemon_stats = self.team_directory[self.pokemon_species(battle.active_pokemon.species)]
            opponent_active_pokemon_stats = DamageCalculatorFormatPokemon(battle.opponent_active_pokemon).formatted()

            print("Checking if opponent_team_directory is populated...")
            if len(self.opponent_team_directory.keys()) > 0:
                print("It is:")
                print(self.opponent_team_directory)
                # Use challenger's team stats to help with damage calculation.
                opponent_active_pokemon_stats = self.opponent_team_directory[self.pokemon_species(battle.opponent_active_pokemon.species)]

                # The AI knows everything about the opposing Pokemon... unless its
                # species has more than one ability to choose from. Get or guess that
                # here.
                opponent_active_pokemon_stats["ability"] = self.utility_functions.get_or_guess_ability(battle.opponent_active_pokemon)

            best_move = None
            best_damage = 0
            print("Iterating over available_moves, which are currently:")
            print(battle.available_moves)
            for move in battle.available_moves:
                print("Evaluating " + move.id + "...")
                if move.current_pp == 0:
                    # Skip if out of PP.
                    print("Out of PP.")
                    continue

                if move.id not in MOVES.keys():
                    # Might be a forced "move" like recharging after a Hyper Beam
                    print("Couldn't find move in dict.")
                    continue

                # Special handling for status moves.
                if move.category == MoveCategory.STATUS:
                    # If it's a move we can use, add it to status moves list.
                    print("It's a status move...")
                    
                    if Effect.TAUNT in battle.active_pokemon.effects:
                        # Can't use status moves while taunted.
                        print("Taunted, can't use.")
                        continue

                    if self.utility_functions.move_heals_user(move) and self.utility_functions.move_does_no_damage(move):
                        # Heal logic is handled elsewhere.
                        print("Healing move, handle elsewhere.")
                        continue

                    if move.target != "self" and not self.move_works_against_target(move, battle.active_pokemon, battle.opponent_active_pokemon):
                        # Skip if move targets a foe but foe is immune to it.
                        print("Foe immune to move.")
                        continue
                    elif move.target == "self" and not self.move_works_against_target(move, battle.active_pokemon, battle.active_pokemon):
                        # Skip if we can't use move on ourself (e.g. Substitute while Substitute is active)
                        print("Can't use this move on ourselves for some reason.")
                        continue

                    if move.weather != None and move.weather in battle.weather.keys():
                        # Don't use weather move if weather for move already active.
                        print("Weather already active.")
                        continue

                    if move.pseudo_weather != None and self.is_id_in_enum_dict(move.pseudo_weather, battle.fields):
                        # E.g. don't use Trick Room when it's already up.
                        print("pseudo_weather already active.")
                        continue

                    if move.side_condition != None and self.is_id_in_enum_dict(
                        move.side_condition, battle.side_conditions):
                        # E.g. don't use light screen when it's already up.
                        print("Side condition already active.")
                        continue

                    # TODO: Check slot condition (e.g. Wish)

                    if move.boosts != None and self.utility_functions.move_boosts_are_useless(battle.active_pokemon, move):
                        # This move boosts stats, but all of the stats it boosts
                        # are already at maximum boost level.
                        print("Move boosts stats, but all stats it boosts are already maxed. Skipping.")
                        continue

                    if self.utility_functions.move_drops_target_speed(move) and self.is_target_faster_than_user(battle.opponent_active_pokemon, battle.active_pokemon) and self.get_boost_for_stat(battle.opponent_active_pokemon.boosts, "spe") > -6:
                        # This move drops the opponent's speed, they're faster than us, AND they're not
                        # at minimum speed yet.
                        print("It controls speed, opponent is faster, and opponent isn't at min speed. Adding to high priority moves.")
                        high_priority_moves.append(move)
                        continue

                    if self.utility_functions.is_useable_setup_move(battle.active_pokemon, move) and self.is_user_able_to_survive_turn(battle.active_pokemon, active_pokemon_stats, opponent_active_pokemon_stats):
                        # If we have a setup move, and our opponent can't KO us this turn,
                        # add to high priorities.
                        high_priority_moves.append(move)
                        continue

                    if move.status != None or move.volatile_status != None:
                        print("It inflicts either a primary or secondary status.")
                        if self.is_high_priority_status_move(move, battle.active_pokemon, battle.opponent_active_pokemon):
                            print("Status is high priority. Adding to high priority moves.")
                            high_priority_moves.append(move)
                            continue

                    print("Normal, viable status move. Adding to status move list.")
                    status_moves.append(move)
                    continue

                if move.id == "fakeout" and self.active_pokemon_turn_counter > 1:
                    # Fake Out only works on the first turn, so skip.
                    print("It's fake out. Skipping due to turn counter.")
                    continue
                elif move.id == "fakeout":
                    # Otherwise, use it! One of the few scenarios where we want
                    # to use it even if we have a potential KO.
                    return self.create_order(move)

                move_data = MOVES[move.id]
                if "ohko" in move_data.keys() and move_data.get("ohko"):
                    # Treat OHKO moves as status moves priority; i.e.,
                    # equal chance to come out as best move, other status moves,
                    # but not favoured over high priority moves and staying
                    # alive.
                    status_moves.append(move)
                    continue

                print("Simulating damage roll for " + move.id)
                move_name = MOVES[move.id].get("name", None)
                print("Simulating damage for " + move_name)
                simulated_damage = 0

                # Check for calculated or fixed damage.
                if move.damage == "level":
                    simulated_damage = battle.opponent_active_pokemon.level
                elif move.damage > 0:
                    simulated_damage = move.damage
                else:
                    num_hits = random.randint(move.n_hit[0], move.n_hit[1])
                    simulated_damage = 0
                    hit_count = 0

                    while hit_count < num_hits:
                        simulated_damage = simulated_damage + damage_calculator.calculate(active_pokemon_stats, opponent_active_pokemon_stats, move_name)
                        hit_count = hit_count + 1

                if not simulated_damage > 0 and self.move_works_against_target(
                    move, battle.active_pokemon, battle.opponent_active_pokemon) and damage_calculator.check_for_error(active_pokemon_stats, opponent_active_pokemon_stats, move_name) == "OK":
                    # If damage is 0, but move seems like it should work, the
                    # calculator may be missing something, so treat it as a
                    # normal status move for now.
                    print(move.id + " simulated 0 damage but seems like it should do something. Adding as status option.")
                    status_moves.append(move)

                print("Damage simulated was " + str(simulated_damage))

                if simulated_damage >= self.guess_current_hp(battle.opponent_active_pokemon):
                    # Does this move knock out our opponent? If so, add to preferred moves.
                    top_priority_moves.append(move)
                    continue

                if self.utility_functions.move_drops_target_speed(move) and self.is_target_faster_than_user(battle.opponent_active_pokemon, battle.active_pokemon) and self.get_boost_for_stat(battle.opponent_active_pokemon.boosts, "spe") > -6:
                    # Speed control is second only to potential KOs.
                    print("Judged target to be faster than us, and " + move.id + " seems to lower speed. Adding to high priority moves.")
                    high_priority_moves.append(move)
                    continue

                if simulated_damage > best_damage:
                    print("Which is greater than current best, which was " + str(best_damage) + ", updating best move to " + move_name)
                    best_damage = simulated_damage
                    best_move = move

            if len(top_priority_moves) > 0:
                print("Selecting a potential KO move from " + str(len(top_priority_moves)) + " top priority moves:")
                print(top_priority_moves)
                return self.create_order(random.choice(top_priority_moves))

            # We don't see any potential KOs at present, so combine best damage move
            # with status moves into a single pool and set that as our current
            # best move.
            move_options = status_moves

            if best_move is not None:
                move_options.append(best_move)
            
            print("Normal move options at this point are ")
            print(move_options)

            if len(move_options) > 0:
                best_move = random.choice(move_options)

            if battle.active_pokemon.current_hp_fraction < 0.5:
                # We're damaged; check for healing moves.
                print("Below 50% HP; checking for healing moves...")
                best_heal = 0
                best_heal_move = None
                all_heals = []
                for move in battle.available_moves:
                    if move.current_pp == 0:
                        continue

                    if not self.utility_functions.move_heals_user(move):
                        continue

                    all_heals.append(move)

                    if move.heal > best_heal:
                        best_heal_move = move
                        best_heal = move.heal

                if best_heal > 0:
                    print("Determined " + MOVES[best_heal_move.id].get("name", None) + " is best heal, using it.")
                    return self.create_order(best_heal_move)
                elif len(all_heals) > 0:
                    # We don't have a move that literally heals us for a
                    # percentage of our max hp, but we do have one or more
                    # healing moves (maybe a drain move), so pick one at random.
                    print("No great heals, but have sub-heals. Choosing one.")
                    print(all_heals)
                    sub_heal = random.choice(all_heals)
                    print("Randomly chose " + sub_heal.id + " from options.")
                    return self.create_order(sub_heal)

            if len(high_priority_moves) > 0:
                print("1 or more high priority moves found:")
                print(high_priority_moves)
                print("Selecting one.")
                return self.create_order(random.choice(high_priority_moves))

            if best_move is None:
                print("No good moves! Trying to switch...")
                if len(battle.available_switches) > 0:
                    self.active_pokemon_turn_counter = 0
                    return self.create_order(self.make_smart_switch(
                    battle.opponent_active_pokemon, battle.available_switches))

                print("No switches available! Choose random move.")
                return self.choose_random_move(battle)

            print("Randomly selected " + best_move.id + " from move options")            
            return self.create_order(best_move)
        elif len(battle.available_switches) > 0:
            self.active_pokemon_turn_counter = 0
            return self.create_order(self.make_smart_switch(
                battle.opponent_active_pokemon, battle.available_switches))
        else:
            # Random switch.
            self.active_pokemon_turn_counter = 0
            return self.choose_random_move(battle)

    def make_smart_switch(self, opponent_pokemon, available_switches):
        if len(available_switches) == 1:
            # It may not be the smart choice, but it's our only choice.
            return available_switches[0]

        good_switch_ins = []
        for switch_option in available_switches:
            for move in switch_option.moves.values():
                if opponent_pokemon.damage_multiplier(move) > 1:
                    # This Pokemon has a super effective move against the
                    # opponent. Add to our good switch-in list.
                    good_switch_ins.append(switch_option)

        if len(good_switch_ins) > 0:
            # We have at least one good switch-in! Choose one at random.
            return random.choice(good_switch_ins)

        # Otherwise... choose anything. It's all the same.
        return random.choice(available_switches)

    def teampreview(self, battle):
        # Try to cache opponent's team's stats for damage calculation.
        opponent_team_path = ".\\config\\Challenger Teams"
        print("Attempting to find opponent's team on disk...")
        if os.path.exists(opponent_team_path):
            print("Team path found...")
            showdown_team_parser = ShowdownTeamParser()
            print("Gathering file names...")
            team_files = [f for f in listdir(opponent_team_path) if isfile(join(opponent_team_path, f))]
            print(str(len(team_files)) + " found:")
            print(team_files)

            for team_file in team_files:
                print("Reading " + team_file + "...")
                lines = []
                team = ""
                with open(opponent_team_path + "\\" + team_file) as f:
                    #lines = f.readlines()
                    team = f.read()
                
                print("Parsing team...")
                team_dir = showdown_team_parser.parse_team(team)
                find_count = 0

                print("Iterating over opponent's team in preview...")
                for opponent_pokemon in battle.opponent_team.values():
                    print("Checking pokemon species in team dir's keys...")
                    print("Opponent pokemon species is: " + self.pokemon_species(opponent_pokemon.species))
                    print("Team dir's keys are:")
                    print(team_dir.keys())
                    if self.pokemon_species(opponent_pokemon.species) in team_dir.keys():
                        print("Pokemon found! Incrementing find count to " + str(find_count))
                        find_count = find_count + 1
                    else:
                        print("No match. Wrong file.")
                        break

                print("Checking find count (it's " + str(find_count) + ")")
                if find_count == len(battle.opponent_team.values()):
                    print("They're all here! Update opponent_team_directory.")
                    # Found the whole team in this showdown file.
                    self.opponent_team_directory = team_dir
                    print("opponent_team_directory is:")
                    print(self.opponent_team_directory)
                    break

        return "/team 123"

    def pokemon_species(self, species_id):
        if species_id not in POKEDEX.keys():
            return species_id

        return POKEDEX[species_id].get('name')

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
        iv = 31
        ev = 0

        if pokedex_entry.get('name') in self.opponent_team_directory.keys():
            # We have the exact stats for this one. Use those instead.
            directory_pokemon = self.opponent_team_directory[pokedex_entry.get('name')]
            
            ev = self.utility_functions.get_ev_from_stat_block(directory_pokemon, "hp")
            iv = self.utility_functions.get_iv_from_stat_block(directory_pokemon, "hp")

        return math.floor(0.01 * (2 * hp_base + iv + math.floor(0.25 * ev)) * pokemon.level) + pokemon.level + 10

    def move_works_against_target(self, move, user, target):
        if move.status is not None and target.status is not None:
            # Pokemon can only have one major status ailment at a time.
            return False

        if move.volatile_status is not None:
            # E.g. confusion, taunted, leech seed -- can't have same one twice.
            target_effects = list(target.effects.keys())
            for effect in target_effects:
                if self.id_from_enum_value(effect) == move.volatile_status:
                    return False
                
            if move.volatile_status == "followme":
                # Singles only, so follow me won't work either.
                return False

            if move.volatile_status == "encore" and target.first_turn:
                # Don't try to encore when they haven't performed yet.
                return False

            if move.volatile_status == "yawn" and target.status is not None:
                # Yawn doesn't work if the opponent can't sleep.
                return False

        if not (target.damage_multiplier(move) > 0):
            # Move doesn't work due to typing.
            return False

        print("Checking abilities...")
        if self.utility_functions.is_move_negated_by_ability(move,
            self.utility_functions.get_or_guess_ability(user),
            self.utility_functions.get_or_guess_ability(target)):
            return False

        # TODO: Check item.

        if move.volatile_status == "attract" and not self.genders_are_attract_compatible(user.gender, target.gender):
            return False

        if move.target != "self" and Effect.SUBSTITUTE in list(target.effects.keys()):
            if move.category == MoveCategory.STATUS and self.utility_functions.move_targets_single_pokemon(move.target):
                # Status moves don't work on substitutes of other Pokemon.
                return False

        return True

    def genders_are_attract_compatible(self, gender1, gender2):
        if gender1 == PokemonGender.MALE:
            return gender2 == PokemonGender.FEMALE

        if gender1 == PokemonGender.FEMALE:
            return gender2 == PokemonGender.MALE

        return False

    def is_id_in_enum_dict(self, id_text, enum_dict):
        for enum_value in enum_dict.keys():
            if id_text == self.id_from_enum_value(enum_value):
                return True

        return False

    def id_from_enum_value(self, enum_value):
        enum_value_text = enum_value.name
        enum_value_text = enum_value_text.lower()
        return enum_value_text.replace("_", "")

    def is_high_priority_status_move(self, move, user, target):
        if move.status != None:
            # All primary status is good.
            return True

        if move.volatile_status == "attract":
            return True

        if move.volatile_status == "confusion":
            return True

        if move.volatile_status == "partiallyTrapped":
            return True

        return False

    def is_target_faster_than_user(self, target, user):
        target_speed_nom_and_dom = [2, 2]
        if target.boosts != None and "spe" in target.boosts.keys():
            target_speed_nom_and_dom = self.utility_functions.calculate_stat_fraction(target.boosts["spe"])

        user_speed_nom_and_dom = [2, 2]
        if user.boosts != None and "spe" in user.boosts.keys():
            user_speed_nom_and_dom = self.utility_functions.calculate_stat_fraction(user.boosts["spe"])

        target_speed_factor = target_speed_nom_and_dom[0] / target_speed_nom_and_dom[1]
        user_speed_factor = user_speed_nom_and_dom[0] / user_speed_nom_and_dom[1]

        target_base_speed = self.calculate_speed_stat(target, False)
        user_base_speed = self.calculate_speed_stat(user, True)

        target_actual_speed = math.floor(target_base_speed * target_speed_factor)
        print("Calculated target's actual speed at " + str(target_actual_speed))

        user_actual_speed = math.floor(user_base_speed * user_speed_factor)
        print("Calculated user's actual speed at " + str(user_actual_speed))

        return target_actual_speed > user_actual_speed

    def calculate_speed_stat(self, pokemon, is_own):
        stat_block = {}
        pokemon_name = self.pokemon_species(pokemon.species)

        if is_own:
            stat_block = self.team_directory[self.pokemon_species(pokemon.species)]
        else:
            stat_block = self.opponent_team_directory[self.pokemon_species(pokemon.species)]

        base_speed = POKEDEX[pokemon.species].get("baseStats").get("spe")
        iv = self.utility_functions.get_iv_from_stat_block(stat_block, "spe")
        ev = self.utility_functions.get_ev_from_stat_block(stat_block, "spe")

        nature_mod = self.utility_functions.get_mod_for_nature(stat_block.get("nature"), "spe")

        result = (math.floor(0.01 * (2 * base_speed + iv + math.floor(0.25 * ev)) * pokemon.level) + 5) * nature_mod
        print("Calculated " + pokemon_name + "'s unmodified speed at " + str(int(result)))
        return result

    def get_boost_for_stat(self, boosts, stat):
        print("Getting " + stat + " boost level.")
        if boosts is None:
            return 0

        if stat not in boosts.keys():
            return 0

        print("Found boost. It's " + str(boosts[stat]))
        return boosts[stat]

    def is_user_able_to_survive_turn(self, active_pokemon, active_pokemon_stats, opponent_active_pokemon_stats):
        damage_calculator = SimpleDamageCalculator()

        for move in opponent_active_pokemon_stats["moves"]:
            # Holy crap we're actually using the moves from the stat block.
            simulated_damage = damage_calculator.calculate(opponent_active_pokemon_stats, active_pokemon_stats, move)

            if simulated_damage >= active_pokemon.current_hp:
                # Move could knock us out. RIP.
                return False

        return True