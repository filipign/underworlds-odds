'''This module contains all needed calculation functions.

Algorithm is based on Warhammer Underworlds: Shadespire rulebook.
Word "Success" has two meanings: Single success reffered as result of dice roll,
but attack is a success when attacker rolled more successes than defender (basically).
'''
from enum import Enum
import logging
from lib.characteristics import Attack
from lib.characteristics import Defence

logger = logging.getLogger()

class CombatResult(Enum):
    critical_success = 2
    success = 1
    driven_back = 0
    failed = -1

class AttackModificators():
    '''Stores values of attack modificators such as cleave'''
    def __init__(self, cleave=False, cleave_on_crit=False, light_armor=False):
        self.cleave = cleave
        self.cleave_on_crit = cleave_on_crit
        self.light_armor = light_armor

    @classmethod
    def from_bool_list(cls, bool_list):
            return cls(bool_list[0], bool_list[1], bool_list[2])

    def __str__(self):
        repr_string = ''
        repr_string += 'cleave_' if self.cleave else ''
        repr_string += 'cleaveoncrit_' if self.cleave_on_crit else ''
        repr_string += 'light_armor_' if self.light_armor else ''
        return repr_string

class RollCharacteristic():
    '''Stores values of roll characteristics for generating purposes'''
    def __init__(self, characteristic, number_of_dices):
        self.number_of_dices = number_of_dices
        self.characteristic = characteristic

class RollResult():
    '''Stores result of single roll of 2 players'''
    def __init__(self, attack_dices=[], defence_dices=[]):
        self.attack_dices = attack_dices
        self.defence_dices = defence_dices


ATTACK_DICE = [Attack.hammer, Attack.hammer, Attack.swords,
               Attack.single_support, Attack.double_support, Attack.crit]
DEFENCE_DICE = [Defence.shield, Defence.shield, Defence.dodge,
                Defence.single_support, Defence.double_support, Defence.crit]

def count_successes(attack_result, defence_result, attack_characteristic, def_characteristic,
                    modificators):
    '''
    For given attack and defensive characteristics, and dices result, count number of
    successes for attacker and defender

    Args:
        attack_result(list of strings): result of dice roll for attacker
        defence_result(list of strings): result of dice roll for defnder
        attack_characteris(list of strings): what counts as success for attacker
        def_characteris(list of strings): what counts as success for defender
        modificators(obj of AttackModificators): bools of atack modificators such as cleave

    Returns:
        obj of dictionary: dictionary with number of successes
            Example:
            {
                'atk_critical_success': 0,
                'atk_success': 1,
                'def_critical_success': 2,
                'def_success': 3,
            }
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
            if defence == Defence.crit and (modificators.light_armor is False):
                def_critical_success += 1
            elif not (modificators.cleave and defence == Defence.shield):
                def_success += 1
    # TODO: Left for debugging purposes, to delete
    # logger.info('(crit/normal) atk: %s/%s; def: %s/%s' %
    #         (atk_critical_success, atk_success, def_critical_success, def_success))
    return {
        'atk_critical_success': atk_critical_success,
        'atk_success': atk_success,
        'def_critical_success': def_critical_success,
        'def_success': def_success,
    }

def check_success(successes):
    '''
    Based on roll successes, check if attack is successfull, failed or draw (driving back
    possibility)

    Args:
        successes(dict): dictionary with number of successes
            Exmaple:
            {
                'atk_critical_success': 0,
                'atk_success': 1,
                'def_critical_success': 2,
                'def_success': 3,
            }

    Returns:
        obj of CombatResult: one of Result values
    '''

    if successes['atk_critical_success'] > successes['def_critical_success']:
        return CombatResult.critical_success

    if successes['atk_critical_success'] == successes['def_critical_success']:
        if successes['atk_success'] > successes['def_success']:
            return (CombatResult.critical_success if successes['atk_critical_success'] > 0
                    else CombatResult.success)
        if (successes['atk_success'] == successes['def_success']
                and (successes['atk_success'] > 0 or successes['atk_critical_success'] > 0)):
            return CombatResult.driven_back
    return CombatResult.failed

def calculate_attack_result(attack_result, defence_result, attack_characteristic,
                            def_characteristic, modificators):
    '''
    For given attack and defensive characteristics, and dices result, count number of
    successes for attacker and defender and determine success of an attack.

    Args:
        attack_result(list of strings): result of dice roll for attacker
        defence_result(list of strings): result of dice roll for defnder
        attack_characteris(list of strings): what counts as success for attacker
        def_characteris(list of strings): what counts as success for defender
        modificators(obj of AttackModificators): bools of atack modificators such as cleave

    Returns:
        obj of CombatResult: one of Result values
    '''
    successes = count_successes(attack_result, defence_result, attack_characteristic,
                                def_characteristic, modificators)
    return check_success(successes)

# TODO: consider using python generators
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

    all_attack_dices = [ATTACK_DICE for i in range(no_attack_dices)]
    all_defence_dices = [DEFENCE_DICE for i in range(no_defence_dices)]

    for attack_roll in itertools.product(*all_attack_dices):
        for defence_roll in itertools.product(*all_defence_dices):
            roll = RollResult(attack_roll, defence_roll)
            rolls.append(roll)

    return rolls

def generate_dice_characterstic(characteristic, supports=0):
    '''
    Determine what is considered success based on main characteristics

    Args:
        characteristic(Attack/Defence enum): main characteristic of attack/defence

    Returns:
        list of Attack/Defence enum values
    '''
    if isinstance(characteristic, Attack):
        char = [characteristic, Attack.crit]
        if supports > 0:
            char.append(Attack.single_support)
        if supports > 1:
            char.append(Attack.double_support)
    else:
        char = [characteristic, Defence.crit]
        if supports > 0:
            char.append(Defence.single_support)
        if supports > 1:
            char.append(Defence.double_support)
    return char


def calculate_odds(attack_characteristic, defence_characteristic, modificators):
    '''
    Calculate odds of succesfull attack action

    Args:
        attack_characteristic(obj of RollCharacteristic): characteristic of attack roll,
            what is consdered success and how many dices
        defence_characteristic(obj of RollCharacteristic): characteristic of defence roll,
            what is consdered success and how many dices
        modificators(obj of AttackModificators): bools of atack modificators such as cleave

    Returns:
        dict of success, driven back, critical_success probabilities

        Example:
        {
            'success': 0.1,
            'driven_back': 0.2,
            'critical_success': 0.3,
        }
    '''
    rolls = generate_rolls(attack_characteristic.number_of_dices,
                           defence_characteristic.number_of_dices)

    results = {
        CombatResult.success: 0,
        CombatResult.driven_back: 0,
        CombatResult.failed: 0,
        CombatResult.critical_success: 0,
    }

    for roll in rolls:
        outcome = calculate_attack_result(roll.attack_dices, roll.defence_dices,
                                          attack_characteristic.characteristic,
                                          defence_characteristic.characteristic,
                                          modificators)
        results[outcome] += 1

    return {
        'success': ((results[CombatResult.success] + results[CombatResult.critical_success])
                    / len(rolls)),
        'driven_back': results[CombatResult.driven_back] / len(rolls),
        'critical_success': results[CombatResult.critical_success] / len(rolls)
    }
