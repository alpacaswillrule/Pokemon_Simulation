#import stats in main
from logging import raiseExceptions
import numpy as np
import pandas as pd


class Pokemon(object):
    def __init__(self, stats,pos,index): #initalizing a pokemon, stores stats in statlst. 
        self.index = index
        self.statlst = []
        self.statlst.append(stats['Name'])#0
        self.statlst.append(stats['Type 1'])#1
        self.statlst.append(stats['HP'])#2
        self.statlst.append(stats['Attack'])#3
        self.statlst.append(stats['Defense'])#4
        self.statlst.append(stats['Sp. Atk'])#5
        self.statlst.append(stats['Sp. Def'])#6
        self.statlst.append(stats['Speed'])#7
        self.statlst.append(stats['Legendary'])#8

        self.strength = self.statlst[3] * self.statlst[2] * self.statlst[4] * self.statlst[5] * self.statlst[7]
        self.position = pos
        self.isAlive = True
        self.reproducecap = self.statlst[2]/20
        self.reproducecounter = 0 # their cooldown is based on hp/10, when counter hits their cap they can reproduce
    
    def get_index(self):
        return self.index

    def getname(self):
        return self.statlst[0]

    def kill(self):
        self.isAlive = False #need to remeber to ensure that dead pokemon are ignored in pdist calculations.
        self.position = (-1,-1) 

    def getstren(self):
        return self.strength

    def get_type(self):
        return self.statlst[1]

    def oneround(self): #just reduces cooldown on reproduce
        if self.isAlive == True:
            self.reproducecounter += 1
        else:
            raise Exception("dead pokemon in oneround")

    def newpos(self,pos):
        if self.isAlive == True:
            self.position = pos
        else:
            raise Exception("dead pokemon moved")

    def can_reproduce(self):  #both pokemon need to return true for it to happen
        if self.reproducecounter > self.reproducecap:
            return True
        else:
            return False
    
    def reproduce(self):
        if self.isAlive == True:
            self.reproducecounter = 0
        else:
            raise Exception("dead pokemon reproduced")

    def getstats(self):
        if self.isAlive == True:
            return self.statlst
        else:
            raise Exception("dead stats accessed")

    def getpos(self):
        if self.isAlive == True:
            return self.position
        else:
            raise Exception("dead position accessed")

    def isAlive(self):
        if self.isAlive == True:
            return True
        else:
            return False