from poke_env.environment.effect import Effect
from poke_env.player.player import Player
from damage_calc_by_post import SimpleDamageCalculator
from poke_env.data import MOVES
from poke_env.data import POKEDEX
from damage_calculator_format_pokemon import DamageCalculatorFormatPokemon
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

        damage_calculator = SimpleDamageCalculator()
        if battle.available_moves:
            active_formatter = DamageCalculatorFormatPokemon(battle.active_pokemon)
            opponent_formatter = DamageCalculatorFormatPokemon(battle.opponent_active_pokemon)

            print("Simulating damage rolls...")
            best_move = random.choice(battle.available_moves)
            best_damage = 0
            for move in battle.available_moves:
                if move.id not in MOVES.keys():
                    # Might be a forced "move" like recharging after a Hyper Beam
                    continue
                move_name = MOVES[move.id].get("name", None)
                print("Simulating damage for " + move_name)
                simulated_damage = damage_calculator.calculate(active_formatter.formatted(), opponent_formatter.formatted(), move_name)
                print("Damage rolled was " + str(simulated_damage))

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

            if battle.active_pokemon.current_hp_fraction < 0.5:
                # We're damaged; check for healing moves.
                print("Below 50% HP; checking for healing moves...")
                best_heal = 0
                best_heal_move = random.choice(battle.available_moves)
                for move in battle.available_moves:
                    if move.heal > best_heal:
                        best_heal_move = move
                        best_heal = move.heal

                if best_heal > 0:
                    print("Determined " + MOVES[best_heal_move.id].get("name", None) + " is best heal, using it.")
                    best_move = best_heal_move

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
