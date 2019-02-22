import unittest
from lib.characteristics import Attack
from lib.characteristics import Defence
from lib.odds import calculate_odds
from lib.odds import generate_dice_characterstic
from lib.odds import RollCharacteristic
from lib.odds import AttackModificators


class CalculateOddsTests(unittest.TestCase):
    '''Test cases for proper calculating odds'''
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_odds_ok(self):
        # 2 swords vs 1 shield
        atk = RollCharacteristic(generate_dice_characterstic(Attack.swords, 0), 2)
        deff = RollCharacteristic(generate_dice_characterstic(Defence.shield, 0), 1)
        result = calculate_odds(atk, deff, AttackModificators())
        expected_result = {
            'success': 0.40,
            'driven_back': 0.11,
            'critical_success': 0.27,
        }

        self.assertAlmostEqual(result['success'], expected_result['success'], places=2)
        self.assertAlmostEqual(result['driven_back'], expected_result['driven_back'], places=2)
        self.assertAlmostEqual(result['critical_success'], expected_result['critical_success'], places=2)

    def test_odds_failed(self):
        # 2 swords vs 1 shield
        atk = RollCharacteristic(generate_dice_characterstic(Attack.swords, 0), 2)
        deff = RollCharacteristic(generate_dice_characterstic(Defence.shield, 0), 1)
        result = calculate_odds(atk, deff, AttackModificators())
        expected_false_results = {
            'success': 0.30,
            'driven_back': 0.1,
            'critical_success': 0.25,
        }

        self.assertNotAlmostEqual(result['success'], expected_false_results['success'], places=2)
        self.assertNotAlmostEqual(result['driven_back'], expected_false_results['driven_back'], places=2)
        self.assertNotAlmostEqual(result['critical_success'], expected_false_results['critical_success'], places=2)


if __name__ == '__main__':
    unittest.main()
