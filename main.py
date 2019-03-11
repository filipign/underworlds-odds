#!/usr/bin/python3
import logging
from lib.characteristics import Attack
from lib.characteristics import Defence
from lib.odds import RollCharacteristic
from lib.odds import calculate_odds
from lib.odds import AttackModificators
from lib.odds import generate_dice_characterstic
from collections import defaultdict


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('main_logger')

def generate_odds(modificators=AttackModificators()):
    '''
    Result_dict structure:
    [atk_characteristic][atk_dices][def_characteristics][def_dices]->
    [atk_support][def_support][modificators][result]
    '''
    nested_dict = lambda: defaultdict(nested_dict)
    result_dict = nested_dict()
    max_attack_dices = 2
    max_def_dices = 2
    combination = [
        [Attack.swords, Defence.shield],
        [Attack.hammer, Defence.shield],
        [Attack.swords, Defence.dodge],
        [Attack.hammer, Defence.dodge],
    ]

    for c in combination:
        for i in range(1, max_attack_dices + 1):
            for j in range(1, max_def_dices + 1):
                for s in range(3):  # atk support
                    atk = RollCharacteristic(generate_dice_characterstic(c[0], s), i)
                    deff = RollCharacteristic(generate_dice_characterstic(c[1], 0), j)
                    result = calculate_odds(atk, deff, modificators)
                    result_dict[c[0].value]['atk_dice_' + str(i)][c[1].value] \
                    ['def_dice_' + str(j)]['atk_support_' + str(s)]['def_support_0']['mod_'] = result
                    # logger.info('%s %i +%i/%s %i: success %.2f; db: %.2f; crit_succ: %.2f' %
                    #     (c[0], i, s, c[1], j, result['success'], result['driven_back'],
                    #     result['critical_success']))
                for s in range(3):  # def support
                    atk = RollCharacteristic(generate_dice_characterstic(c[0], 0), i)
                    deff = RollCharacteristic(generate_dice_characterstic(c[1], s), j)
                    result = calculate_odds(atk, deff, modificators)
                    result_dict[c[0].value]['atk_dice_' + str(i)][c[1].value] \
                    ['def_dice_' + str(j)]['atk_support_0']['def_support_' + str(s)]['mod_'] = result
                    # logger.info('%s %i/%s %i +%i: success %.2f; db: %.2f; crit_succ: %.2f' %
                    #     (c[0], i, c[1], j, s, result['success'], result['driven_back'],
                    #     result['critical_success']))

    # dump dict to json file
    import json
    with open('result.json', 'w+') as file_handler:
        json.dump(result_dict, file_handler)

def main():
    generate_odds()

if __name__ == '__main__':
    main()