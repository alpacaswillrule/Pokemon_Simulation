import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist
from Pokemonclass import Pokemon
import random

statsdataframe = pd.read_csv('Pokemon.csv')
typechart = pd.read_csv('Pokemon_Type_Chart.csv')

def initialize_simulation(NumPokemon = 15, Area = 300): #returns a list of each pokemon object, a list of coordinates aswell corresponding to list of pokemon objects
    Pokemonlst = []
    x = random.sample(range(0, Area), NumPokemon)
    y = random.sample(range(0, Area), NumPokemon)
    for i in range(NumPokemon):
        Pokemonlst.append(Pokemon(statsdataframe.iloc[0],(x[i],y[i])))
    return Pokemonlst
    
def battle(Pokemonlst, index1, index2): #hasnt been debugged yet, also may be cool to add a hp function by which hp reduces over time
    stat1 = Pokemonlst[index1].getstats()
    stat2 = Pokemonlst[index2].getstats() # gets pokemon stats
    
    firstadv = typechart.loc[stat2[1]].loc[stat1[1]] #looks up type advantage in typechart, returns number from .5 to 2
    secondadv = typechart.loc[stat1[1]].loc[stat2[1]]

    stren1 = np.random.normal(loc=1,scale=.8) * stat1[3] * stat1[2] * stat1[4] * stat1[5] * stat1[7] * firstadv #calculates their strenghts, adds randomness
    stren2 = np.random.normal(loc=1,scale=.8) * stat2[3] * stat2[2] * stat2[4] * stat2[5] * stat2[7] * secondadv

    if stren1>stren2: #the battle! one of them is killed, maybe adjust in future so theres a chance that one survives
        Pokemonlst[index2].kill()
        Pokemonlst.pop(index2)

    else:
        Pokemonlst[index1].kill()
        Pokemonlst.pop(index1)


def move(Pokemonlst,Area):
    for pokemon in Pokemonlst:
        pokemon.getstats()[7]
        pokemon.newpos()

def extractcoordlist(Pokemonlst): # helper for oneiter, will return list of coordinates of living pokemon so can use pdist and determine closeby pokemon
    pass

def oneiter(Pokemonlst, NumPokemon, Area): #use pdist here, run the move function, and run their oneround functions then call battle function for one that encounter each other
    pass

def visualize(Pokemonlst,NumPokemon,Area):
    pass

initialize_simulation()
        



