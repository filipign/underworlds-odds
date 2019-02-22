#!/usr/bin/python3
import logging
from lib.characteristics import Attack
from lib.characteristics import Defence
from lib.odds import RollCharacteristic
from lib.odds import calculate_odds
from lib.odds import AttackModificators
from lib.odds import generate_dice_characterstic


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('main_logger')

def generate_odds(modificators=AttackModificators()):
    max_attack_dices = 3
    max_def_dices = 2
    combination = [
        [Attack.swords, Defence.shield],
        [Attack.hammer, Defence.shield],
        [Attack.swords, Defence.dodge],
        [Attack.hammer, Defence.dodge]
    ]

    for c in combination:
        for i in range(1, max_attack_dices):
            for j in range(1, max_def_dices):
                for s in range(3):  # atk support
                    atk = RollCharacteristic(generate_dice_characterstic(c[0], s), i)
                    deff = RollCharacteristic(generate_dice_characterstic(c[1], 0), j)
                    result = calculate_odds(atk, deff, modificators)
                    logger.info('%s %i +%i/%s %i: success %.2f; db: %.2f; crit_succ: %.2f' %
                        (c[0], i, s, c[1], j, result['success'], result['driven_back'],
                        result['critical_success']))
                for s in range(3):  # def support
                    atk = RollCharacteristic(generate_dice_characterstic(c[0], 0), i)
                    deff = RollCharacteristic(generate_dice_characterstic(c[1], s), j)
                    result = calculate_odds(atk, deff, modificators)
                    logger.info('%s %i/%s %i +%i: success %.2f; db: %.2f; crit_succ: %.2f' %
                        (c[0], i, c[1], j, s, result['success'], result['driven_back'],
                        result['critical_success']))

def main():
    # atk = RollCharacteristic(generate_dice_characterstic(Attack.swords, 1), 2)
    # deff = RollCharacteristic(generate_dice_characterstic(Defence.shield, 0), 1)
    # modificators = AttackModificators()
    # logger.info(calculate_odds(atk, deff, modificators))
    generate_odds()

if __name__ == '__main__':
    main()