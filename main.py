from statistics import variance
from xml.etree.ElementTree import tostring
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform
from Pokemonclass import Pokemon
import random
from matplotlib.pyplot import cm
statsdataframe = pd.read_csv('Pokemon.csv')
typechart = pd.read_csv('Pokemon_Type_Chart.csv')

killnamecounter = [] #appends pokemon name every time it makes a kill

def initialize_simulation(NumPokemon,Numduplicates, Area): #returns a list of each pokemon object, a list of coordinates aswell corresponding to list of pokemon objects
    Pokemonlst = []
    x = random.sample(range(0, Area), NumPokemon*Numduplicates) #gets unique x and y positions for each pokemon in the area, crashes if area too small
    y = random.sample(range(0, Area), NumPokemon*Numduplicates)
    posindex = 0
    for j in range(0,NumPokemon):
        for i in range(Numduplicates):
            Pokemonlst.append(Pokemon(statsdataframe.iloc[j],(x[posindex],y[posindex]),j))
            posindex+=1
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


def battle(Pokemonlst, index1, index2,variance,chance_survive): #hasnt been debugged yet, also may be cool to add a hp function by which hp reduces over time
    stat1 = Pokemonlst[index1].get_type()
    stat2 = Pokemonlst[index2].get_type() # gets pokemon's primary type
    stat2int = typetoindex(stat2)
    stat1int = typetoindex(stat1)

    firstadv = typechart[stat2][stat1int] #looks up type advantage in typechart, returns number from .5 to 2
    secondadv = typechart[stat1][stat2int]

    stren1 = np.random.normal(loc=1,scale=variance) * Pokemonlst[index1].getstren() * firstadv #adds randomness and type advantage to their calculated strength
    stren2 = np.random.normal(loc=1,scale=variance) * Pokemonlst[index2].getstren() * secondadv

    if stren1>stren2: #the battle! one of them is killed, maybe adjust in future so theres a chance that one survives
        #right here need to do chance survival draw
        draw = random.uniform(0,1)
        if draw > chance_survive:
            Pokemonlst[index2].kill()
            print(Pokemonlst[index2].getname()+" killed by "+Pokemonlst[index1].getname())
        #Pokemonlst.pop(index2) #is now done later because was confounding loop through conflicts
        print(Pokemonlst[index2].getname()+" escaped "+Pokemonlst[index1].getname())
        killnamecounter.append(Pokemonlst[index1].getname())
    else:
        draw = random.uniform(0,1)
        if draw > chance_survive:
            Pokemonlst[index1].kill()
            print(Pokemonlst[index1].getname()+" killed by "+Pokemonlst[index2].getname())
        else:
        #Pokemonlst.pop(index1)
            print(Pokemonlst[index1].getname()+" escaped "+Pokemonlst[index2].getname())
        killnamecounter.append(Pokemonlst[index2].getname())
    return Pokemonlst

def gencoords(pos,speed,Area):
    if pos[1] > Area or pos[0] > Area or pos[1] < 0 or pos[0] < 0: #strictk invariant
        raise Exception('position passed out of bounds gencoords')

    dir = random.randint(0,3) #randomly generate a direction
    x = np.random.normal(loc=speed/10,scale=.5) # randomly generate how much to move in that directin
    y = np.random.normal(loc=speed/10,scale=.5)
    newpos = [Area,Area]
    if dir == 0: # 4 different directions, confirmed each one is chosen about equally. problem is witn the if statements
       
        newpos[0] = pos[0] + x
        if newpos[0] > Area or newpos[0] < 0:  #checks to see if out of bounds, changes direction if out of bounds
          newpos[0] = pos[0] - 2 * x  

        newpos[1] = pos[1] + y
        if newpos[1] > Area or newpos[1] < 0: # also checks this coord for out of bounds, changes direction
          newpos[1] = pos[1] - 2 * y

    if dir == 1:
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
def extractnamelist(Pokemonlst):
    namelst = []
    for pokemon in Pokemonlst:
        namelst.append(pokemon.getname())
    return namelst

def reproduce(Pokemonlst,index1,index2,Area):
    if Pokemonlst[index1].can_reproduce() == True and Pokemonlst[index2].can_reproduce() == True:
        Pokemonlst[index1].reproduce()
        Pokemonlst[index1].reproduce()
        x = random.sample(range(0, Area),1)
        y = random.sample(range(0, Area),1)
        Pokemonlst.append(Pokemon(statsdataframe.loc[Pokemonlst[index1].get_index()],(x[0],y[0]),index1))

    return Pokemonlst

def oneiter(Pokemonlst, Area,engagedist,var,chance_survive): #use pdist here, run the move function, and run their oneround functions then call battle function for one that encounter each other
    
    dists = extractcoordlist(Pokemonlst)
    distmatrix = squareform(pdist(dists))
    np.fill_diagonal(distmatrix,float('inf')) #create distance matrix between all pokemon
    conflicts = np.argwhere(distmatrix<engagedist)  # where pokemon are closer than engeagedist, there is a conflict
    conflicts = set(conflicts.flatten()) #duplicates removed from conflicts
    it = iter(conflicts)
    conflicts = list(zip(it,it))
    
    for conflict in conflicts: # problem, pokemonlst gets shortened by each battle so conflict indexes change, will change their status to is dead, then after for loop remove all isdead from list
        if Pokemonlst[conflict[0]].getname() ==  Pokemonlst[conflict[1]].getname():
            Pokemonlst = reproduce(Pokemonlst,conflict[0],conflict[1],Area)
            print(Pokemonlst[conflict[0]].getname()+" was born")
        else:
            Pokemonlst = battle(Pokemonlst,conflict[0],conflict[1],var,chance_survive)
    
    Pokemonlst[:] = [x for x in Pokemonlst if x.isAlive == True]

    for pokemon in Pokemonlst:
        pokemon.oneround()

    Pokemonlst = move(Pokemonlst, Area) 


def visualize(Pokemonlst,Area,iter):
    x = extractcoordlist(Pokemonlst)
    # plt.scatter(*zip(*x))
    # plt.show()
    plt.title("positions of pokemon at: "+str(iter)+" iterations")
    names = extractnamelist(Pokemonlst)
    labels,freq = np.unique(names,return_counts=True)
    color = cm.rainbow(np.linspace(0,1,len(labels)))
    for index in range(len(labels)):
        indiciesforonepokemon = [c for c,k in enumerate(names) if k == labels[index]]
        xplot = [x[i] for i in indiciesforonepokemon]  
        plt.scatter(*zip(*xplot), color=color[index]) #gives unique colors if there are enough colors to each pokemon in scatterplot
    plt.legend(labels)
    plt.show()
    plt.title("population distribution of pokemon at: "+str(iter)+" iterations")
    for index in range(len(labels)):
        plt.scatter(labels[index],freq[index],color=color[index])
    plt.legend(labels)
    plt.show()
    names,killfreq = np.unique(killnamecounter,return_counts=True)
    plt.title("win distribution: at: "+str(iter)+" iterations")
    color = cm.rainbow(np.linspace(0,1,len(names)))
    for index in range(len(names)):
        plt.scatter(names[index],killfreq[index], color=color[index]) #gives unique colors if there are enough colors to each pokemon in scatterplot
    plt.legend(names)
    plt.show()


###PARAMETERS, CAN ALSO ADJUST STRENGHT CALCULATION AND REPRODUCE CAP IN POKEMON CLASS########################
#HIGHLY RECOMMEND ADJUST REPRODUCE CAP DEPENDING ON HOW LOW HP POKEMON COMPARE TO MEGAEX.
NumPokemon = 50
Numduplicates = 5 #number of duplicates made of each pokemon
Area = 400 #keep this large or not enough unique spots to start for pokemon
engage_dist = 5
iterations = 100 #killf
Pokemonlst = initialize_simulation(NumPokemon,Numduplicates,Area)
var = .5 #from 0 to 1, how much variation do you want in pokemon battle outcomes
vis_every_iters = iterations/2 #set this to however often you want to visualize the simulation. for example 150 means visualizes every 150 iterations, eg at 150,300,450 etc
chance_survive = .5 # set this to values from 0 to 1, is chance a loser of battle escapes helps out the types that have low hp

############################################################

vis_every_iters = int(vis_every_iters) #just in case are dividing iterations
copyiter = iterations
visualize(Pokemonlst,Area,0) #visualizes once at beginning
while iterations > 0:
    oneiter(Pokemonlst,Area,engage_dist,var,chance_survive) #runs one iteration of the simulation
    iterations-=1
    if iterations % vis_every_iters ==0:
        visualize(Pokemonlst,Area,copyiter - iterations)


#visualize(Pokemonlst,Area)
     

