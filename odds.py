#!/usr/bin/python3
from enum import Enum
from characteristics import Attack
from characteristics import Defence

class Result(Enum):
    success = 1
    driven_back = 0
    failed = -1

attack_dice = ('hammer', 'hammer', 'swords', 'single_support' 'double_support', 'crit_attack')
defence_dice = ('shield', 'shield', 'dodge', 'single_support' 'double_support', 'crit_defence')

def check_success(attack_result, defence_result, attack_characteristic, def_characteristic, 
                  cleave=False, cleave_on_crit=False):
    '''
    For given attack and defensive characteristics, and dices result, check
    if attack is successfull, failed or failed but targeted fighter may be driven back
    Args:
        attack_result(list of strings): result of dice roll for attacker
        defence_result(list of strings): result of dice roll for defnder
        attack_characteris(list of strings): what counts as success for attacker
        def_characteris(list of strings): what counts as success for defender
        cleave(bool): is attack action with cleave
        cleave_on_crit(bool): is attack action with cleave when attacker rolls crit

    Returns:
        Result: one of Result values
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

    if not cleave:
        cleave = atk_critical_success > 0 and cleave_on_crit

    for defence in defence_result:
        if defence in def_characteristic:
            if defence == Defence.crit:
                def_critical_success += 1
            elif not (cleave and defence == Defence.shield):    
                def_success += 1

    # print('atk: %s/%s; def: %s/%s' % (atk_critical_success, atk_success, def_critical_success, def_success))
    if atk_critical_success > def_critical_success:
        return Result.success
    if atk_critical_success == def_critical_success:
        if atk_success > def_success:
            return Result.success
        if atk_success == def_success:
            return Result.driven_back
        return Result.failed
    else:
        return Result.failed

def main():
    pass

if __name__ == '__main__':
    main()