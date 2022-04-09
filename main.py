import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform
from Pokemonclass import Pokemon
import random

statsdataframe = pd.read_csv('Pokemon.csv')
typechart = pd.read_csv('Pokemon_Type_Chart.csv')

def initialize_simulation(NumPokemon, Area): #returns a list of each pokemon object, a list of coordinates aswell corresponding to list of pokemon objects
    Pokemonlst = []
    x = random.sample(range(0, Area), NumPokemon)
    y = random.sample(range(0, Area), NumPokemon)
    for i in range(NumPokemon):
        Pokemonlst.append(Pokemon(statsdataframe.iloc[0],(x[i],y[i])))
    return Pokemonlst
    
def battle(Pokemonlst, index1, index2): #hasnt been debugged yet, also may be cool to add a hp function by which hp reduces over time
    stat1 = Pokemonlst[index1].get_type()
    stat2 = Pokemonlst[index2].get_type() # gets pokemon's primary type
    
    firstadv = typechart.loc[stat2].loc[stat1] #looks up type advantage in typechart, returns number from .5 to 2
    secondadv = typechart.loc[stat1].loc[stat2]

    stren1 = np.random.normal(loc=1,scale=.8) * Pokemonlst.getstren() * firstadv #adds randomness and type advantage to their calculated strength
    stren2 = np.random.normal(loc=1,scale=.8) * Pokemonlst.getstren() * secondadv

    if stren1>stren2: #the battle! one of them is killed, maybe adjust in future so theres a chance that one survives
        Pokemonlst[index2].kill()
        Pokemonlst.pop(index2)

    else:
        Pokemonlst[index1].kill()
        Pokemonlst.pop(index1)
    return Pokemonlst

def gencoords(pos,speed,Area):
    if pos[1] > Area or pos[0] > Area or pos[1] < 0 or pos[0] < 0: #strictk invariant
        raise Exception('position passed out of bounds gencoords')

    dir = random.randint(0,4) #randomly generate a direction
    x = np.random.normal(loc=speed/10,scale=.5) # randomly generate how much to move in that directin
    y = np.random.normal(loc=speed/10,scale=.5)
    newpos = (Area,Area)
    if dir == 0: # 4 different directions
        newpos[0] = pos[0] + x
        if newpos[0] > Area or newpos[0] < 0:  #checks to see if out of bounds, changes direction if out of bounds
          newpos[0] = pos[0] - 2 * x  

        newpos[1] = pos[1] + y
        if newpos[1] > Area or newpos[1] < 0: # also checks this coord for out of bounds, changes direction
          newpos[1] = pos[1] - 2 * y

    elif dir == 1:
        newpos[0] = pos[0] - x
        if newpos[0] > Area or newpos[0] < 0:  #checks to see if out of bounds, changes direction if out of bounds
          newpos[0] = pos[0] + 2 * x  

        newpos[1] = pos[1] - y
        if newpos[1] > Area or newpos[1] < 0: # also checks this coord for out of bounds, changes direction
          newpos[1] = pos[1] + 2 * y 

    elif dir == 2:
        newpos[0] = pos[0] - x
        if newpos[0] > Area or newpos[0] < 0:  #checks to see if out of bounds, changes direction if out of bounds
          newpos[0] = pos[0] + 2 * x  

        newpos[1] = pos[1] + y 
        if newpos[1] > Area or newpos[1] < 0: # also checks this coord for out of bounds, changes direction
          newpos[1] = pos[1] - 2 * y     
    elif dir == 3:
        newpos[0] = pos[0] + x
        if newpos[0] > Area or newpos[0] < 0:  #checks to see if out of bounds, changes direction if out of bounds
          newpos[0] = pos[0] - 2 * x  
        newpos[1] = pos[1] - y
        if newpos[1] > Area or newpos[1] < 0: # also checks this coord for out of bounds, changes direction
          newpos[1] = pos[1] + 2 * y 
    
    
    if pos[1] > Area or pos[0] > Area or pos[1] < 0 or pos[0] < 0: # strict invariant
        raise Exception('position output out of bounds gencoords')
    return newpos


def move(Pokemonlst,Area):
    for pokemon in Pokemonlst:
        speed = pokemon.getstats()[7]
        curpos = pokemon.getpos()
        pokemon.newpos(gencoords(curpos,speed,Area)) #moves pokemon to new coordinates based on their speed and area constraints
    return Pokemonlst

def extractcoordlist(Pokemonlst): # returns lst of coordinates for all pokemon
    coordlst = []
    for pokemon in Pokemonlst:
        coordlst.append(pokemon.getpos())

    return coordlst

def reproduce(Pokemonlst,index1,index2,Area):
    if Pokemonlst[index1].can_reproduce() == True and Pokemonlst[index2].can_reproduce() == True:
        Pokemonlst[index1].reproduce()
        Pokemonlst[index1].reproduce()
        x = random.sample(range(0, Area))
        y = random.sample(range(0, Area))
        Pokemonlst.append(Pokemon(statsdataframe.iloc[0],(x,y)))

    return Pokemonlst

def oneiter(Pokemonlst, NumPokemon, Area,engagedist): #use pdist here, run the move function, and run their oneround functions then call battle function for one that encounter each other
    dists = extractcoordlist(Pokemonlst)
    distmatrix = squareform(pdist(dists))
    np.fill_diagonal(distmatrix,float('inf'))
    conflicts = np.argwhere(distmatrix<engagedist) 
    conflicts = set(conflicts.flatten()) #duplicates removed
    for conflict in conflicts:
        if Pokemonlst[conflict[0]].getname() ==  Pokemonlst[conflict[1]].getname():
            Pokemonlst = reproduce(Pokemonlst,conflict[0],conflict[1],Area)
        else:
            Pokemonlst = battle(Pokemonlst,conflict[0],conflict[1])
    for pokemon in Pokemonlst:
        pokemon.oneround()
    Pokemonlst = move(Pokemonlst, Area)

    #first we find closeby pokemon, then they fight or fuck
    #then oneround for cooldowns
    #them move

def visualize(Pokemonlst,NumPokemon,Area):
    pass
###parameters, can also adjust reproduce cap in pokemonclass.py
NumPokemon = 15
Area = 300
engage_dist = 10
Pokemonlst = initialize_simulation(NumPokemon,Area)
oneiter(Pokemonlst,NumPokemon,Area,engage_dist)
        



