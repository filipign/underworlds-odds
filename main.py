#!/usr/bin/python3
import logging
from lib.characteristics import Attack
from lib.characteristics import Defence
from lib.odds import RollCharacteristic
from lib.odds import calculate_odds
from lib.odds import AttackModificators
from lib.odds import generate_dice_characterstic
from collections import defaultdict
from itertools import product


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('main_logger')

def generate_odds(modificators=AttackModificators(cleave=True)):
    '''
    Result_dict structure:
    [atk_characteristic][atk_dices][def_characteristics][def_dices]->
    [atk_support][def_support][modificators][result]
    '''
    nested_dict = lambda: defaultdict(nested_dict)
    result_dict = nested_dict()

    # These two values are configurable
    max_attack_dices = 1
    max_def_dices = 1

    characteristic_combination = [
        [Attack.swords, Defence.shield],
        [Attack.hammer, Defence.shield],
        [Attack.swords, Defence.dodge],
        [Attack.hammer, Defence.dodge],
    ]
    support_combination = ((0, 0), (0, 1), (0, 2), (1, 0), (2, 0))
    modificators = product([True, False], repeat=3)

    for m in modificators:
        mod = AttackModificators.from_bool_list(m)
        for c in characteristic_combination:
            for i in range(1, max_attack_dices + 1):
                for j in range(1, max_def_dices + 1):
                    for s in support_combination:
                        atk = RollCharacteristic(generate_dice_characterstic(c[0], s[0]), i)
                        deff = RollCharacteristic(generate_dice_characterstic(c[1], s[1]), j)
                        result = calculate_odds(atk, deff, mod)
                        result_dict[c[0].value]['atk_dice_' + str(i)][c[1].value] \
                        ['def_dice_' + str(j)]['atk_support_' + str(s[0])] \
                        ['def_support_' + str(s[1])]['mod_' + str(mod)] = result

    # dump dict to json file
    import json
    with open('result.json', 'w+') as file_handler:
        json.dump(result_dict, file_handler)

def main():
    generate_odds()

if __name__ == '__main__':
    main()