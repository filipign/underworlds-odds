from enum import Enum


class Attack(Enum):
    hammer = 'hammer'
    swords = 'swords'
    single_support = 'single_support'
    double_support = 'double_support'
    crit = 'crit_attack'

class Defence(Enum):
    shield = 'shield'
    dodge = 'dodge'
    single_support = 'single_support'
    double_support = 'double_support'
    crit = 'crit_defence'