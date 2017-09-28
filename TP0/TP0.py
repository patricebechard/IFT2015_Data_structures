# -*- coding: utf-8 -*-
"""
TP0 - IFT2015 : Conway's Game of Life in color

Hiver 2017 - Université de Montréal

Auteur : Patrice Béchard  P1088418 20019173 BECP30119404

8 février 2017
"""
#-----------------import modules------------------

import sys
import copy

#-------------------Classes-----------------------

class InputError(Exception):
    """If the input entered for a certain function is not ok"""
    pass

class Grid:
    """Grid onto which the game is played"""
    
    def __init__(self,dim):
        self._dimensions=dim                #dimensions of the playing grid
        self._grid=[]                       #the grid where the game is played is initialized
        self._rules_red=[]                  #to store rules for red organisms
        self._rules_green=[]                #same for green
        self._rules_blue=[]                 #and finally blue
        for i in range(self._dimensions[0]):#each node of the grid is a cell
            self._grid.append([Cell(0,[i,j]) for j in range(self._dimensions[1])])    
            
    def show_grid(self):
        """Shows the grid with active organisms with proper template"""
        self._showgrid=''
        for i in range(self._dimensions[0]):
            for j in range(self._dimensions[1]):                
                if self._grid[i][j]._status=='R':   
                    self._showgrid+='R '        #show the red
                elif self._grid[i][j]._status=='G':
                    self._showgrid+='G '        #show the green
                elif self._grid[i][j]._status=='B':
                    self._showgrid+='B '        #show the blue
                else:
                    self._showgrid+='. '        #show the empty cells           
            self._showgrid+='\n'
        print(self._showgrid)
        
    def add_element(self,elem,pos):
        """We add an element to the grid"""
        if elem in ['R','G','B',0]:
            self._grid[pos[0]][pos[1]]=Cell(elem,pos)
        else:
            raise InputError('Not a legitimate element to enter in grid')
        
    def add_rules(self,type,rules):
        """We add rules to the game for the three colors"""
        if len(rules)!=3:
            raise InputError("Bad input for rules")
        elif not rules[1]<=rules[0]<=rules[2]:
            raise InputError('Rules are not OK with constraints')
        else:                       #adding rules
            if type=='R':
                self._rules_red=rules 
            elif type=='G':
                self._rules_green=rules
            elif type=='B':
                self._rules_blue=rules
                
    def show_rules(self):
        print("Type : R")
        print("Organism is born if number of neighbors = {0}"\
             .format(self._rules_red[0]))
        print("Organism dies if number of neighbors is {0} <= n <= {1}"\
             .format(self._rules_red[1],self._rules_red[2]))
        print("Type : G")
        print("Organism is born if number of neighbors = {0}"\
             .format(self._rules_green[0]))
        print("Organism dies if number of neighbors is {0} <= n <= {1}"\
             .format(self._rules_green[1],self._rules_green[2]))
        print("Type : B")
        print("Organism is born if number of neighbors = {0}"\
             .format(self._rules_red[0]))
        print("Organism dies if number of neighbors is {0} <= n <= {1}\n"\
             .format(self._rules_blue[1],self._rules_blue[2]))
        
    def evolution(self):
        """We make the grid evolve for one time step"""
        self._old=copy.deepcopy(self._grid)   #we are updating the grid, we deepcopy info in old grid
        for i in range(self._dimensions[0]):  #loop over all cells
            for j in range(self._dimensions[1]):
                neighbors=self._old[i][j].count_neighbors()  
                if not self._old[i][j]._status:
                    #cell is empty, we check if it will be occupied
                    if neighbors==self._rules_red[0]:
                        self.add_element('R',[i,j])         #red is born
                    elif neighbors==self._rules_green[0]:
                        self.add_element('G',[i,j])         #green is born
                    elif neighbors==self._rules_blue[0]:
                        self.add_element('B',[i,j])         #blue is born
                elif self._old[i][j]._status=='R' and \
                         (neighbors<self._rules_red[1] or \
                         neighbors>self._rules_red[2]):     #is red and over/under populated
                    self.add_element(0,[i,j])
                elif self._old[i][j]._status=='G' and \
                        (neighbors<self._rules_green[1] or \
                         neighbors>self._rules_green[2]):   #is green and over/under populated     
                    self.add_element(0,[i,j])
                elif self._old[i][j]._status=='B' and \
                        (neighbors<self._rules_blue[1] or \
                         neighbors>self._rules_blue[2]):    #is blue and over/under populated
                    self.add_element(0,[i,j])
                    
         
class Cell:
    """Each cell of the grid has a status (dead (0) or R, G, B)"""
    def __init__(self,status,pos):
        self._status=status
        self._pos=pos
        
    def count_neighbors(self):
        """Counts the neighbors of a cell"""
        self._nb_neighbors=0              #n
        for i in [-1,0,1]:
            for j in [-1,0,1]:            #loop over all neighbors of the cell
                if i == 0 and j == 0:     #excluding self
                    continue
                elif (self._pos[0] + i) < 0 or (self._pos[1] + j < 0):
                    continue              #avoiding negative index when on a side
                try:
                    value=play._old[self._pos[0] + i][self._pos[1] + j]._status
                    if value in ['R','G','B']:  #it is a neighbor
                        self._nb_neighbors += 1
                except IndexError:        #out of bounds (cell on side)
                    continue
        return self._nb_neighbors

#------------------------fonctions--------------------------
def read_config(file):
    f=open(file)
    initdim=1                               #flag to set grid dimensions
    for line in f:
        line=(line.strip()).split(',')      #get rid of \n and split with delimiter ','  
        if initdim == 1:                    #create a grid with dimensions mentioned in config.txt
            initdim=0
            global play                     #accessible from everywhere
            play=Grid(list(map(int,line)))  #set grid with dimensions
        elif line[0] == 'R' or line[0] == 'G' or line[0] == 'B':
            play.add_element(line[0],list(map(int,line[1:])))  #add element to grid 
        else:
            raise InputError('Bad input in config.txt')
            
def read_rules(file):
    f=open(file)
    for line in f:
        line=(line.strip()).split(':')      #get rid of \n and split with delimiter ':'
        if line[0] == 'R' or line[0] == 'G' or line[0] == 'B':
            rules=list(map(int,line[1].split(',')))     #convert str to list of int
            play.add_rules(line[0],rules)               #adding rules
        else:
            raise InputError("Bad input for type of cell in rules.txt")
                
#-------------------------MAIN()----------------------------  
                
read_config('config.txt')     #read config.txt
read_rules('rules.txt')       #read rules.txt

print('\n\t\tRÈGLEMENTS\n')
play.show_rules()             #we show the rules of the game

print('\nCONFIGURATION INITIALE\n')
play.show_grid()              #initial config of the grid

if '-animation' in sys.argv:
    while True:               #animation stops when ctrl-c by user
        play.evolution()      #the grid evolves
        input()               #press enter to progress
        play.show_grid()      #show the present state of the grid
else:
    try: 
        #search for a number of iterations in command line arguments
        niter=int([s for s in sys.argv if s.isdigit()][0])  
        for i in range(niter):
            play.evolution()  #the grid evolves "niter" times
        play.show_grid()      #we show final state of the grid
    except (TypeError,IndexError):
        raise InputError("You must specify a number of iterations when calling program")
        