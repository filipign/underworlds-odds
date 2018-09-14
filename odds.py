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

class RollResult():
    '''Stores result of single roll of 2 players'''
    def __init__(self, attack_dices=[], defence_dices=[]):
        self.attack_dices = attack_dices
        self.defence_dices = defence_dices


attack_dice = [Attack.hammer, Attack.hammer, Attack.swords,
               Attack.single_support, Attack.double_support, Attack.crit]
defence_dice = [Defence.shield, Defence.shield, Defence.dodge,
                Defence.single_support, Defence.double_support, Defence.crit]

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

# def generate_rolls(attack_roll_characteristic, defence_roll_characteristic):
#     '''
#     Generate list of all possible outcomes of dices rolls

#     Args:
#         attack_roll_characteristic(obj of RollCharacteristic): characteristic of roll for attacker,
#             what is consdered success and how many dices
#         defence_roll_characteristic(obj of RollCharacteristic): characteristic of roll for defender,
#             what is consdered success and how many dices
#     '''

def generate_rolls(no_attack_dices, no_defence_dices):
    '''
    Generate list of all possible outcomes of dices rolls

    Args:
        no_attack_dices(int): number of attacking dices
        no_defence_dices(int): number of defending dices

    Returns:
        List of obj of RollResult: all possible outcomes of dices roll
    '''
    import itertools

    rolls = []
    all_attack_dices = []
    all_defence_dices = []

    all_attack_dices = [attack_dice for i in range(no_attack_dices)]
    all_defence_dices = [defence_dice for i in range(no_defence_dices)]

    for attack_roll in itertools.product(*all_attack_dices):
        for defence_roll in itertools.product(*all_defence_dices):
            roll = RollResult(attack_roll, defence_roll)
            rolls.append(roll)

    # TODO: to delete, left for debugging purposes
    for i, roll in enumerate(rolls):
        print('-- #%d --' % i)
        print(roll.attack_dices)
        print(roll.defence_dices)
        print('--------')
    print(len(rolls))

    return rolls

def calculate_odds():
    pass

def main():
    generate_rolls(2, 1)

if __name__ == '__main__':
    main()