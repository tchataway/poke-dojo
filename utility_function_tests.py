from utils import UtilityFunctions
from poke_env.environment.move import Move
import unittest

class UtilityFunctionTests(unittest.TestCase):
    def test_move_targets_single_pokemon_success(self):
        utils = UtilityFunctions()
        self.assertTrue(utils.move_targets_single_pokemon("adjacentAlly"))
        self.assertTrue(utils.move_targets_single_pokemon("adjacentAllyOrSelf"))
        self.assertTrue(utils.move_targets_single_pokemon("adjacentFoe"))
        self.assertTrue(utils.move_targets_single_pokemon("any"))
        self.assertTrue(utils.move_targets_single_pokemon("normal"))
        self.assertTrue(utils.move_targets_single_pokemon("randomNormal"))
        self.assertTrue(utils.move_targets_single_pokemon("scripted"))
        self.assertTrue(utils.move_targets_single_pokemon("self"))
        self.assertFalse(utils.move_targets_single_pokemon("all"))
        self.assertFalse(utils.move_targets_single_pokemon("allAdjacent"))
        self.assertFalse(utils.move_targets_single_pokemon("allAdjacentFoes"))
        self.assertFalse(utils.move_targets_single_pokemon("allies"))
        self.assertFalse(utils.move_targets_single_pokemon("allySide"))
        self.assertFalse(utils.move_targets_single_pokemon("allyTeam"))
        self.assertFalse(utils.move_targets_single_pokemon("foeSide"))

    def test_is_move_negated_by_ability_success(self):
        utils = UtilityFunctions()

        # Own Tempo
        confuse_ray = Move("confuseray")
        self.assertFalse(utils.is_move_negated_by_ability(confuse_ray, "Mold Breaker", "Own Tempo"))
        self.assertTrue(utils.is_move_negated_by_ability(confuse_ray, "Adaptability", "Own Tempo"))

        # Oblivious
        attract = Move("attract")
        self.assertFalse(utils.is_move_negated_by_ability(attract, "Mold Breaker", "Oblivious"))
        self.assertTrue(utils.is_move_negated_by_ability(attract, "Adaptability", "Oblivious"))