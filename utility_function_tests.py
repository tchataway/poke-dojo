from utils import UtilityFunctions
from poke_env.environment.move import Move
import unittest

class UtilityFunctionTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.utils = UtilityFunctions()
        super(UtilityFunctionTests, self).__init__(*args, **kwargs)

    def test_move_targets_single_pokemon_success(self):
        self.assertTrue(self.utils.move_targets_single_pokemon("adjacentAlly"))
        self.assertTrue(self.utils.move_targets_single_pokemon("adjacentAllyOrSelf"))
        self.assertTrue(self.utils.move_targets_single_pokemon("adjacentFoe"))
        self.assertTrue(self.utils.move_targets_single_pokemon("any"))
        self.assertTrue(self.utils.move_targets_single_pokemon("normal"))
        self.assertTrue(self.utils.move_targets_single_pokemon("randomNormal"))
        self.assertTrue(self.utils.move_targets_single_pokemon("scripted"))
        self.assertTrue(self.utils.move_targets_single_pokemon("self"))
        self.assertFalse(self.utils.move_targets_single_pokemon("all"))
        self.assertFalse(self.utils.move_targets_single_pokemon("allAdjacent"))
        self.assertFalse(self.utils.move_targets_single_pokemon("allAdjacentFoes"))
        self.assertFalse(self.utils.move_targets_single_pokemon("allies"))
        self.assertFalse(self.utils.move_targets_single_pokemon("allySide"))
        self.assertFalse(self.utils.move_targets_single_pokemon("allyTeam"))
        self.assertFalse(self.utils.move_targets_single_pokemon("foeSide"))

    def test_is_move_negated_by_ability_success(self):
        # Own Tempo
        confuse_ray = Move("confuseray")
        self.assertFalse(self.utils.is_move_negated_by_ability(confuse_ray, "Mold Breaker", "Own Tempo"))
        self.assertTrue(self.utils.is_move_negated_by_ability(confuse_ray, "Adaptability", "Own Tempo"))

        # Oblivious
        attract = Move("attract")
        self.assertFalse(self.utils.is_move_negated_by_ability(attract, "Mold Breaker", "Oblivious"))
        self.assertTrue(self.utils.is_move_negated_by_ability(attract, "Adaptability", "Oblivious"))
        taunt = Move("taunt")
        self.assertFalse(self.utils.is_move_negated_by_ability(taunt, "Mold Breaker", "Oblivious"))
        self.assertTrue(self.utils.is_move_negated_by_ability(taunt, "Adaptability", "Oblivious"))

    def test_move_drops_speed_success(self):
        # Scary Face (expect true)
        scary_face = Move("scaryface")
        self.assertTrue(self.utils.move_drops_target_speed(scary_face))

        # Rock Tomb (expect true, secondary but 100% chance)
        rock_tomb = Move("rocktomb")
        self.assertTrue(self.utils.move_drops_target_speed(rock_tomb))

        # Flamethrower (expect false)
        flamethrower = Move("flamethrower")
        self.assertFalse(self.utils.move_drops_target_speed(flamethrower))

        # Bubble (expect false, it can drop speed but isn't guaranteed to)
        bubble = Move("bubble")
        self.assertFalse(self.utils.move_drops_target_speed(bubble))

    def test_calculate_stat_fraction_success(self):
        self.assertEqual(self.utils.calculate_stat_fraction(-6), [2, 8])
        self.assertEqual(self.utils.calculate_stat_fraction(-5), [2, 7])
        self.assertEqual(self.utils.calculate_stat_fraction(-4), [2, 6])
        self.assertEqual(self.utils.calculate_stat_fraction(-3), [2, 5])
        self.assertEqual(self.utils.calculate_stat_fraction(-2), [2, 4])
        self.assertEqual(self.utils.calculate_stat_fraction(-1), [2, 3])
        self.assertEqual(self.utils.calculate_stat_fraction(0), [2, 2])
        self.assertEqual(self.utils.calculate_stat_fraction(1), [3, 2])
        self.assertEqual(self.utils.calculate_stat_fraction(2), [4, 2])
        self.assertEqual(self.utils.calculate_stat_fraction(3), [5, 2])
        self.assertEqual(self.utils.calculate_stat_fraction(4), [6, 2])
        self.assertEqual(self.utils.calculate_stat_fraction(5), [7, 2])
        self.assertEqual(self.utils.calculate_stat_fraction(6), [8, 2])
