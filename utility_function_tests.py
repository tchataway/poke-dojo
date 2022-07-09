from utils import UtilityFunctions
import unittest

class UtilityFunctionTests(unittest.TestCase):
    def test_move_targets_single_pokemon(self):
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