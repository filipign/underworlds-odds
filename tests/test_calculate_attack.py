#!/usr/bin/python3
import unittest
from lib.characteristics import Attack
from lib.characteristics import Defence
from lib.odds import calculate_attack_result
from lib.odds import CombatResult
from lib.odds import AttackModificators

class CalculateAttackResultTests(unittest.TestCase):
    '''Test cases for calculate_attack_result function'''
    def setUp(self):
        self.shields = (Defence.shield, Defence.crit)
        self.dodges = (Defence.dodge, Defence.crit)
        self.hammers = (Attack.hammer, Attack.crit)
        self.swords = (Attack.swords, Attack.crit)
        self.default_modificators = AttackModificators()

    def tearDown(self):
        pass

    def test_attack_result_failed(self):
        '''calculate_attack_result should return CombatResult.failed'''
        # critical def
        attack_result = (Attack.hammer, Attack.crit, Attack.hammer)
        def_result = (Defence.shield, Defence.crit, Defence.crit)
        result = calculate_attack_result(attack_result, def_result, self.hammers, self.shields,
                                         self.default_modificators)
        self.assertEqual(result, CombatResult.failed)

        # crit draw, success def
        attack_result = (Attack.hammer, Attack.crit, Attack.swords)
        def_result = (Defence.shield, Defence.crit, Defence.shield)
        result = calculate_attack_result(attack_result, def_result, self.hammers, self.shields,
                               self.default_modificators)
        self.assertEqual(result, CombatResult.failed)

        # success def
        attack_result = (Attack.hammer, Attack.swords, Attack.hammer)
        def_result = (Defence.shield, Defence.shield, Defence.shield)
        result = calculate_attack_result(attack_result, def_result, self.hammers, self.shields,
                               self.default_modificators)
        self.assertEqual(result, CombatResult.failed)

    def test_attack_result_ok(self):
        '''calculate_attack_result should return CombatResult.success'''
        # crital atk
        attack_result = (Attack.hammer, Attack.crit)
        def_result = (Defence.dodge, Defence.dodge)
        result = calculate_attack_result(attack_result, def_result, self.hammers, self.dodges,
                               self.default_modificators)
        self.assertEqual(result, CombatResult.critical_success)

        # crit draw, success atk
        attack_result = (Attack.hammer, Attack.crit)
        def_result = (Defence.dodge, Defence.crit)
        result = calculate_attack_result(attack_result, def_result, self.hammers, self.shields,
                               self.default_modificators)
        self.assertEqual(result, CombatResult.critical_success)

        # success atk
        attack_result = (Attack.swords, Attack.swords)
        def_result = (Defence.shield, Defence.dodge)
        result = calculate_attack_result(attack_result, def_result, self.swords, self.dodges,
                               self.default_modificators)
        self.assertEqual(result, CombatResult.success)

    def test_driven_back(self):
        '''calculate_attack_result should return CombatResult.driven_back'''
        # crit success
        attack_result = (Attack.swords, Attack.crit)
        def_result = (Defence.shield, Defence.crit)
        result = calculate_attack_result(attack_result, def_result, self.swords, self.shields,
                               self.default_modificators)
        self.assertEqual(result, CombatResult.driven_back)

        # normal success
        attack_result = (Attack.swords, Attack.swords)
        def_result = (Defence.shield, Defence.shield)
        result = calculate_attack_result(attack_result, def_result, self.swords, self.shields,
                               self.default_modificators)
        self.assertEqual(result, CombatResult.driven_back)

    def test_supports_failed(self):
        '''calculate_attack_result should return CombatResult.success (testing with support modifications)'''
        # single support defence success
        attack_result = (Attack.swords,)
        def_result = (Defence.single_support, Defence.single_support)
        def_support_char = self.shields + (Defence.single_support,)
        result = calculate_attack_result(attack_result, def_result, self.swords, def_support_char,
                               self.default_modificators)
        self.assertEqual(result, CombatResult.failed)

        # double support defence success
        attack_result = (Attack.swords, Attack.swords)
        def_result = (Defence.double_support, Defence.single_support, Defence.shield)
        def_support_char = self.shields + (Defence.double_support, Defence.single_support)
        result = calculate_attack_result(attack_result, def_result, self.swords, def_support_char,
                               self.default_modificators)
        self.assertEqual(result, CombatResult.failed)

    def test_supports_ok(self):
        '''calculate_attack_result should return CombatResult.success (testing with support modifications)'''
        # attack with one support success
        attack_result = (Attack.single_support,)
        atk_support_char = self.swords + (Attack.single_support,)
        def_result = (Defence.dodge,)
        result = calculate_attack_result(attack_result, def_result, atk_support_char, self.shields,
                               self.default_modificators)
        self.assertEqual(result, CombatResult.success)

        # attack with two support success
        attack_result = (Attack.single_support, Attack.double_support)
        atk_support_char = self.swords + (Attack.single_support, Attack.double_support)
        def_result = (Defence.dodge,)
        result = calculate_attack_result(attack_result, def_result, atk_support_char, self.shields,
                               self.default_modificators)
        self.assertEqual(result, CombatResult.success)

    def test_attack_result_modificators(self):
        '''calculate_attack_result modificators'''
        # cleave success
        attack_result = (Attack.swords, Attack.swords)
        def_result = (Defence.shield, Defence.shield)
        modificators = AttackModificators(cleave=True)
        result = calculate_attack_result(attack_result, def_result, self.swords, self.shields, modificators)
        self.assertEqual(result, CombatResult.success)

        # cleave on crit success
        attack_result = (Attack.swords, Attack.swords, Attack.crit)
        def_result = (Defence.shield, Defence.shield, Defence.crit)
        modificators = AttackModificators(cleave_on_crit=True)
        result = calculate_attack_result(attack_result, def_result, self.swords, self.shields,
                               modificators)
        self.assertEqual(result, CombatResult.critical_success)

        # cleave but dodge success
        attack_result = (Attack.hammer, Attack.crit)
        def_result = (Defence.dodge, Defence.dodge, Defence.crit)
        modificators = AttackModificators(cleave=True)
        result = calculate_attack_result(attack_result, def_result, self.hammers, self.dodges, modificators)
        self.assertEqual(result, CombatResult.failed)

        # cleave on crit fail
        attack_result = (Attack.swords, Attack.swords, Attack.hammer)
        def_result = (Defence.shield, Defence.shield, Defence.shield)
        modificators = AttackModificators(cleave_on_crit=True)
        result = calculate_attack_result(attack_result, def_result, self.swords, self.shields, modificators)
        self.assertEqual(result, CombatResult.failed)

if __name__ == '__main__':
    unittest.main()
