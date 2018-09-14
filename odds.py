#!/usr/bin/python3
from enum import Enum
from characteristics import Attack
from characteristics import Defence

class CombatResult(Enum):
    success = 1
    driven_back = 0
    failed = -1

class AttackModificators():
    '''Stores values of attack modificators such as cleave'''
    def __init__(self, cleave=False, cleave_on_crit=False):
        self.cleave = cleave
        self.cleave_on_crit = cleave_on_crit

class RollCharacteristic():
    '''Stores values of roll characteristics for generating purposes'''
    def __init__(self, characteristic, number_of_dices, supports=0):
        self.number_of_dices = number_of_dices
        self.characteristic = characteristic
        self.supports = supports


attack_dice = (Attack.hammer, Attack.hammer, Attack.swords,
               Attack.single_support, Attack.double_support, Attack.crit)
defence_dice = (Defence.shield, Defence.shield, Defence.dodge,
                Defence.single_support, Defence.double_support, Defence.crit)

def check_success(attack_result, defence_result, attack_characteristic, def_characteristic,
                  modificators):
    '''
    For given attack and defensive characteristics, and dices result, check
    if attack is successfull, failed or failed but targeted fighter may be driven back
    Args:
        attack_result(list of strings): result of dice roll for attacker
        defence_result(list of strings): result of dice roll for defnder
        attack_characteris(list of strings): what counts as success for attacker
        def_characteris(list of strings): what counts as success for defender
        modificators(obj of AttackModificators): bools of atack modificators such as cleave

    Returns:
        obj of CombatResult: one of Result values
    '''
    atk_critical_success = 0
    atk_success = 0
    def_critical_success = 0
    def_success = 0

    for attack in attack_result:
        if attack in attack_characteristic:
            if attack == Attack.crit:
                atk_critical_success += 1
            else:
                atk_success += 1

    if not modificators.cleave:
        modificators.cleave = atk_critical_success > 0 and modificators.cleave_on_crit

    for defence in defence_result:
        if defence in def_characteristic:
            if defence == Defence.crit:
                def_critical_success += 1
            elif not (modificators.cleave and defence == Defence.shield):
                def_success += 1

    # TODO: Left for debugging purposes, to delete
    # print('atk: %s/%s; def: %s/%s' % (atk_critical_success, atk_success, def_critical_success, def_success))
    if atk_critical_success > def_critical_success:
        return CombatResult.success
    if atk_critical_success == def_critical_success:
        if atk_success > def_success:
            return CombatResult.success
        if atk_success == def_success:
            return CombatResult.driven_back
        return CombatResult.failed
    else:
        return CombatResult.failed

def generate_rolls(attack_dices, defence_dices):
    '''
    Generate list of all possible outcomes of dices rolls

    Args:
        attack_dices(int):
        defence_dices(int):

    Returns:
        List of lists: all possible outcomes of dices roll
    '''

def find_odds():
    pass

def main():
    pass

if __name__ == '__main__':
    main()