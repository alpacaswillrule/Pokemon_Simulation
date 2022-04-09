#import stats in main

class Pokemon(object):
    def __init__(self, stats):
        self.name = stats['Name']
        self.type1 =   stats['Type 1']
        self.hp = stats['HP']
        self.attack = stats['Attack']
        self.defense = stats['Defense']
        self.spattack = stats['Sp.Atk']
        self.spdefense = stats['Sp.Def']
        self.speed = stats['Speed']
        self.islegendary = stats['Legendary']