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
        Pokemonlst.append(Pokemon(statsdataframe.iloc[i],(x[i],y[i])))
    return Pokemonlst

def typetoindex(stat2):
    if stat2 == 'Normal':
        return 0
    elif stat2 == 'Fire':
        return 1
    elif stat2 == 'Water':
        return 2
    elif stat2 == 'Electric':
        return 3
    elif stat2 == 'Grass':
        return 4
    elif stat2 == 'Ice':
        return 5
    elif stat2 == 'Fighting':
        return 6
    elif stat2 == 'Poison':
        return 7
    elif stat2 == 'Ground':
        return 8
    elif stat2 == 'Flying':
        return 9
    elif stat2 == 'Psychic':
        return 10
    elif stat2 == 'Bug':
        return 11
    elif stat2 == 'Rock':
        return 12
    elif stat2 == 'Ghost':
        return 13
    elif stat2 == 'Dragon':
        return 14
    elif stat2 == 'Dark':
        return 15
    elif stat2 == 'Steel':
        return 16
    elif stat2 == 'Fairy':
        return 17
    else:
        raise Exception("unrecognied type in type to index")


def battle(Pokemonlst, index1, index2): #hasnt been debugged yet, also may be cool to add a hp function by which hp reduces over time
    stat1 = Pokemonlst[index1].get_type()
    stat2 = Pokemonlst[index2].get_type() # gets pokemon's primary type
    stat2int = typetoindex(stat2)
    stat1int = typetoindex(stat1)

    firstadv = typechart[stat2][stat1int] #looks up type advantage in typechart, returns number from .5 to 2
    secondadv = typechart[stat1][stat2int]

    stren1 = np.random.normal(loc=1,scale=.8) * Pokemonlst[index1].getstren() * firstadv #adds randomness and type advantage to their calculated strength
    stren2 = np.random.normal(loc=1,scale=.8) * Pokemonlst[index2].getstren() * secondadv

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
    newpos = [Area,Area]
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
    return tuple(newpos)


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
        x = random.sample(range(0, Area),1)
        y = random.sample(range(0, Area),1)
        Pokemonlst.append(Pokemon(statsdataframe.iloc[0],(x[0],y[0])))

    return Pokemonlst

def oneiter(Pokemonlst, NumPokemon, Area,engagedist): #use pdist here, run the move function, and run their oneround functions then call battle function for one that encounter each other
    dists = extractcoordlist(Pokemonlst)
    distmatrix = squareform(pdist(dists))
    np.fill_diagonal(distmatrix,float('inf'))
    conflicts = np.argwhere(distmatrix<engagedist) 
    conflicts = set(conflicts.flatten()) #duplicates removed
    it = iter(conflicts)
    conflicts = list(zip(it,it))
    #print(conflicts)
    for conflict in conflicts:
        if Pokemonlst[conflict[0]].getname() ==  Pokemonlst[conflict[1]].getname():
            Pokemonlst = reproduce(Pokemonlst,conflict[0],conflict[1],Area)
            print("a pokemon was born")
        else:
            Pokemonlst = battle(Pokemonlst,conflict[0],conflict[1])
            print("a pokemon died")
    for pokemon in Pokemonlst:
        pokemon.oneround()
    Pokemonlst = move(Pokemonlst, Area)


def visualize(Pokemonlst,NumPokemon,Area):
    x = extractcoordlist(Pokemonlst)
    plt.scatter(*zip(*x))
    plt.show()
###parameters, can also adjust reproduce cap in pokemonclass.py
NumPokemon = 15
Area = 300
engage_dist = 10
iterations = 20
Pokemonlst = initialize_simulation(NumPokemon,Area)

visualize(Pokemonlst,NumPokemon,Area)
while iterations > 0:
    oneiter(Pokemonlst,NumPokemon,Area,engage_dist)
    iterations-=1
visualize(Pokemonlst,NumPokemon,Area)
        



