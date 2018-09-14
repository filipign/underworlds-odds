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
    def __init__(self, cleave=False, cleave_on_crit=False, light_armor=False, guard=False):
        self.cleave = cleave
        self.cleave_on_crit = cleave_on_crit
        self.light_armor = light_armor
        self.guard = guard

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
            # TODO: light armor and guard implementation
            # if defence == Defence.crit and modificators.light_armor not False:
            if defence == Defence.crit:
                def_critical_success += 1
            elif not (modificators.cleave and defence == Defence.shield):
                def_success += 1

    # TODO: Left for debugging purposes, to delete
    print('(crit/normal) atk: %s/%s; def: %s/%s' % (atk_critical_success, atk_success, def_critical_success, def_success))
    if atk_critical_success > def_critical_success:
        return CombatResult.success
    if atk_critical_success == def_critical_success:
        if atk_success > def_success:
            return CombatResult.success
        elif atk_success == def_success and (atk_success > 0 or atk_critical_success > 0):
            return CombatResult.driven_back
        return CombatResult.failed
    else:
        return CombatResult.failed

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

    all_attack_dices = [attack_dice for i in range(no_attack_dices)]
    all_defence_dices = [defence_dice for i in range(no_defence_dices)]

    for attack_roll in itertools.product(*all_attack_dices):
        for defence_roll in itertools.product(*all_defence_dices):
            roll = RollResult(attack_roll, defence_roll)
            rolls.append(roll)

    # TODO: to delete, left for debugging purposes
    # for i, roll in enumerate(rolls):
    #     print('-- #%d --' % i)
    #     print(roll.attack_dices)
    #     print(roll.defence_dices)
    #     print('--------')
    # print(len(rolls))
    return rolls

def generate_dice_characterstic(characteristic):
    '''
    Determine what is considered success based on main characteristics

    Args:
        characteristic(Attack/Defence enum): main characteristic of attack/defence

    Returns:
        list of Attack/Defence enum values
    '''
    if isinstance(characteristic, Attack):
        return [characteristic, Attack.crit]
    else:
        return [characteristic, Defence.crit]


def calculate_odds(attack_characteristic, defence_characteristic, modificators):
    '''
    Calculate odds of succesfull attack action

    Args:
        attack_characteristic(obj of RollCharacteristic): characteristic of attack roll,
            what is consdered success and how many dices
        defence_characteristic(obj of RollCharacteristic): characteristic of defence roll,
            what is consdered success and how many dices
        modificators(obj of AttackModificators): bools of atack modificators such as cleave
    '''
    rolls = generate_rolls(attack_characteristic.number_of_dices,
                           defence_characteristic.number_of_dices)

    results = {
        CombatResult.success: 0,
        CombatResult.driven_back: 0,
        CombatResult.failed: 0
    }
    for roll in rolls:
        outcome = check_success(roll.attack_dices, roll.defence_dices,
                                attack_characteristic.characteristic,
                                defence_characteristic.characteristic,
                                modificators)
        print(outcome)
        results[outcome] += 1
    odds = {
        'success': results[CombatResult.success] / len(rolls),
        'driven_back': (results[CombatResult.driven_back]) / len(rolls)
    }
    return odds


def main():
    atk = RollCharacteristic(generate_dice_characterstic(Attack.swords), 1, 0)
    deff = RollCharacteristic(generate_dice_characterstic(Defence.shield), 1, 0)
    modificators = AttackModificators(cleave=False)
    print(calculate_odds(atk, deff, modificators))

if __name__ == '__main__':
    main()