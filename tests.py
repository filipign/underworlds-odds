import unittest
from characteristics import Attack
from characteristics import Defence
from odds import check_success
from odds import Result

class OddsTests(unittest.TestCase):

    def setUp(self):
        self.shields = (Defence.shield, Defence.crit)
        self.dodges = (Defence.dodge, Defence.crit)
        self.hammers = (Attack.hammer, Attack.crit)
        self.swords = (Attack.swords, Attack.crit)

    def tearDown(self):
        pass

    def test_atk_failed(self):
        # critical def
        attack_result = (Attack.hammer, Attack.crit, Attack.hammer)
        def_result = (Defence.shield, Defence.crit, Defence.crit)
        result = check_success(attack_result, def_result, self.hammers, self.shields)
        self.assertEqual(result, Result.failed)

        # crit draw, success def
        attack_result = (Attack.hammer, Attack.crit, Attack.swords)
        def_result = (Defence.shield, Defence.crit, Defence.shield)
        result = check_success(attack_result, def_result, self.hammers, self.shields)
        self.assertEqual(result, Result.failed)

        # success def
        attack_result = (Attack.hammer, Attack.swords, Attack.hammer)
        def_result = (Defence.shield, Defence.shield, Defence.shield)
        result = check_success(attack_result, def_result, self.hammers, self.shields)
        self.assertEqual(result, Result.failed)

        # cleave but dodge success
        attack_result = (Attack.hammer, Attack.crit)
        def_result = (Defence.dodge, Defence.dodge, Defence.crit)
        result = check_success(attack_result, def_result, self.hammers, self.dodges, cleave=True)
        self.assertEqual(result, Result.failed)

        # cleave on crit fail
        attack_result = (Attack.swords, Attack.swords, Attack.hammer)
        def_result = (Defence.shield, Defence.shield, Defence.shield)
        result = check_success(attack_result, def_result, self.swords, self.shields, cleave_on_crit=True)
        self.assertEqual(result, Result.failed)

    def test_atk_success(self):
        # crital atk
        attack_result = (Attack.hammer, Attack.crit)
        def_result = (Defence.dodge, Defence.dodge)
        result = check_success(attack_result, def_result, self.hammers, self.dodges)
        self.assertEqual(result, Result.success)

        # crit draw, success atk
        attack_result = (Attack.hammer, Attack.crit)
        def_result = (Defence.dodge, Defence.crit)
        result = check_success(attack_result, def_result, self.hammers, self.shields)
        self.assertEqual(result, Result.success)

        # success atk
        attack_result = (Attack.swords, Attack.swords)
        def_result = (Defence.shield, Defence.dodge)
        result = check_success(attack_result, def_result, self.swords, self.dodges)
        self.assertEqual(result, Result.success)

        # cleave success
        attack_result = (Attack.swords, Attack.swords)
        def_result = (Defence.shield, Defence.shield)
        result = check_success(attack_result, def_result, self.swords, self.shields, cleave=True)
        self.assertEqual(result, Result.success)

        # cleave on crit success
        attack_result = (Attack.swords, Attack.swords, Attack.crit)
        def_result = (Defence.shield, Defence.shield, Defence.crit)
        result = check_success(attack_result, def_result, self.swords, self.shields, cleave_on_crit=True)
        self.assertEqual(result, Result.success)

    def test_driven_back(self):
        # crit success
        attack_result = (Attack.swords, Attack.crit)
        def_result = (Defence.shield, Defence.crit)
        result = check_success(attack_result, def_result, self.swords, self.shields)
        self.assertEqual(result, Result.driven_back)

        # normal success
        attack_result = (Attack.swords, Attack.swords)
        def_result = (Defence.shield, Defence.shield)
        result = check_success(attack_result, def_result, self.swords, self.shields)
        self.assertEqual(result, Result.driven_back)

    def test_supports(self):
        # attack with one support success
        attack_result = (Attack.single_support,)
        atk_support_char = self.swords + (Attack.single_support,)
        def_result = (Defence.dodge,)
        result = check_success(attack_result, def_result, atk_support_char, self.shields)
        self.assertEqual(result, Result.success)

        # double support defence success
        attack_result = (Attack.swords, Attack.swords)
        def_result = (Defence.double_support, Defence.single_support, Defence.shield)
        def_support_char = self.shields + (Defence.double_support, Defence.single_support)
        result = check_success(attack_result, def_result, self.swords, def_support_char)
        self.assertEqual(result, Result.failed)

if __name__ == '__main__':
    unittest.main()
