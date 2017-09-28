# -*- coding: utf-8 -*-
# @Author: Patrice Béchard 20019173
# @Date:   2017-03-20 15:32:00
# @Last Modified time: 2017-03-20 22:49:34
#
# IFT2015 - Structure de données
# TP1 - Ultimate Tic-Tac-Toe

#-----------------------------Modules-------------------------------------------
import sys
from tree_abstract import Tree, LinkedQueue
import random

#----------------------Setting user's symbol form last move---------------------
initconfig=int(sys.argv[-1])

def define_symbol():
	"""Store symbol used by user (not computer)"""
	temp = initconfig >> 162 & 127
	opp_symbol = initconfig >> ((80-temp)<<1) & 3
	if not opp_symbol in [1,2]: raise InputError('Opponent played unknown symbol')
	SYMBOL = (opp_symbol%2)+1
	return SYMBOL

#-----------------------------Classes-------------------------------------------
class InputError(Exception):
	"""Bad UTTT configuration"""
	pass

class MetaGame:
	"""
	Manages the 'config' int
	calls Game to test subgames
	Manages the display mode
	Manages the modification of the game config
	"""
	SYMBOL=define_symbol()

	class _Game:
		"""Represents a standard tictactoe grid"""
		def __init__(self):
			self._game=[0 for i in range(9)]
			self._status=0

		def __len__(self):
			return len(self._game)

		def winner(self,xo):
			"""status = 0 : unfinished , 1 : won , 2 : lost , 3 : tie"""
			for i in [xo,(xo%2)+1]:
				"""try all tictactoe winning combinations"""
				if (self._game[0] == i and self._game[1] == i and self._game[2] == i) or \
				   (self._game[3] == i and self._game[4] == i and self._game[5] == i) or \
				   (self._game[6] == i and self._game[7] == i and self._game[8] == i) or \
				   (self._game[0] == i and self._game[3] == i and self._game[6] == i) or \
				   (self._game[1] == i and self._game[4] == i and self._game[7] == i) or \
				   (self._game[2] == i and self._game[5] == i and self._game[8] == i) or \
				   (self._game[0] == i and self._game[4] == i and self._game[8] == i) or \
				   (self._game[2] == i and self._game[4] == i and self._game[6] == i) :
				   	if i == xo:
				   		self._status = 1
				   		return
				   	else:
				   		self._status = 2
				   		return
			if 0 not in self._game:
				self._status = 3
				return
			self._status = 0
			return

	def __init__(self,config):
		"""Initialize last move info, full game grid and game status"""
		self._config = config
		lastpos = config >> 162 & 127
		if not 0 <= lastpos < 81 : raise InputError('Bad configuration : last element not in grid')
		lastsymb = config >> ((80-lastpos)<<1) & 3
		if not lastsymb in [1,2] : raise InputError('Bad configuration : unknown symbol for last move played')
		self._last = [lastpos, lastsymb]
		self._fullgame = self._Game()
		self._status = 0
		self.set_config()		

	def set_config(self):
		"""Initialize status for every sub game and full game"""
		for i in range(9):
			temp=self._Game()
			for j in range(len(temp)):
				trycell = 9*i + j
				temp._game[j] = self._config >> ((80-trycell)<<1) & 3
			temp.winner(self.SYMBOL)				#status of the grid
			self._fullgame._game[i]=temp._status
		self._fullgame.winner(1)					#status of the full game
		
	def update_config(self):
		"""Returns all possible configurations"""
		whichgame = [self._last[0] % 9]				#next game to play in
		self._possible=[]
		if self._fullgame._game[whichgame[0]] != 0: #game is over, we can play anywhere
			whichgame=[]
			for i in range(9):
				if self._fullgame._game[i] == 0:	#games not over yet
					whichgame.append(i)
		for i in whichgame:
			for j in range(9):
				trycell = i*9 + j
				if not self._config >> ((80-trycell)<<1) & 3 :	#cell is empty
					self.newconfig = self._update_cell(trycell)
					self._possible.append(self.newconfig)
		return self._possible
				
	def _update_cell(self,cell):
		"""Changing bits from configuration for position and last played"""
		temp = self._config ^ (1<<(161-(2*cell+(self._last[1]+1)%2)))	#update cell
		temp = temp ^ (self._last[0]<<162) | (cell<<162)				#set as last cell updated
		return temp

	def is_winner(self):
		return True if self._fullgame._status == 1 else False

	def is_loser(self):
		return True if self._fullgame._status == 2 else False
	
	def display(self,config=None):
		"""Displays the complete UTTT grid configuration"""
		status = [46,120,111]							# '.' , 'x' , 'o'
		if config == None:
			config = self._config
		last = config >> 162 & 127 
		for i in range(9):	
			s = ''
			if i and not i%3 : print(29*'-')					#horizontal separation when i=3,6
			for j in range(9):
				if j and not j%3 : s += chr(124)				#vertical separation when j=3,6
				cell = (i//3)*27 + (i%3)*3 + (j//3)*9 + j%3		#generates cell number
				value = status[config >> ((80-cell)<<1) & 3]
				if cell == last and value in [120,111] : value -= 32	#convert to capital letter
				s += (chr(32) + chr(value) + chr(32))
			print(s)

class GameTree(Tree):
	"""Defines the game tree for a given configuration"""
	class _Node:
		"""Lightweight, nonpublic class for storing node"""
		__slots__='_element','_parent','_children'        #streamline memory usage

		def __init__(self,element,parent=None):
			self._element=element
			self._parent=parent
			self._children=[]

	class Position(Tree):
		"""An abstraction representing the location of a single element"""
		def __init__(self,container,node):
			"""Constructor should not be invoked by user"""
			self._container=container
			self._node=node
        
		def element(self):
			"""Return the element stored at this position"""
			return self._node._element
        
		def __eq__(self,other):
			"""Return True if other is a Position representing the same location"""
			return type(other) is type(self) and other._node is self._node

	def __init__(self):
		self._root=None
		self._size=0

	def __len__(self):
		"""Return the total number of elements in the tree"""
		return self._size

	def _make_position(self,node):
		"""Return Position instance for given node (or None if no node)"""
		return self.Position(self,node)

	def _validate(self,p):
		"""Return associated node, if position is valid"""
		if not isinstance(p,self.Position):
			raise TypeError("p must be proper Position type")
		if p._container is not self:
			raise ValueError("p does not belong to this container")
		if p._node._parent is p._node:      #convention for deprecated nodes
			raise ValueError("p is no longer valid")
		return p._node

	def root(self):
		"""Return the root Position of the tree (or None if the tree is empty)"""
		return self._make_position(self._root)
    
	def parent(self,p):
		"""Return the Position of p's parent (or None if p is root)"""
		node=self._validate(p)
		return self._make_position(node._parent)

	def children(self,p):
		"""Return the position of p's children (or None if p has no children)"""
		node=self._validate(p)
		children_pos=[]
		for i in range(len(node._children)):
			children_pos.append(self._make_position(node._children[i]))
		return children_pos

	def num_children(self,p):
		"""Return the number of children of Position p"""
		node=self._validate(p)
		return len(node._children) if node._children != None else 0
	
	def add_root(self,e):
		"""Place element e at the root of an empty tree and return new Position    
		Raise ValueError if tree is not empty
		"""
		if self._root is not None: raise ValueError('Root exists')
		self._size=1
		self._root=self._Node(e)
		return self._make_position(self._root)

	def add_children(self,e,p):
		"""Place elements in e as children of node at position p. Return new position
		Raise ValueError if tree is empty
		"""
		parent=self._validate(p)
		if self._root is None : raise ValueError("Root doesn't exist")
		children_pos=[]
		for i in e:
			self._size += 1
			parent._children.append(self._Node(i,parent))
			children_pos.append(self._make_position(parent._children[-1]))
		return children_pos

	def show_tree(self):
		BFS=self.breadthfirst()
		i=0
		d=0
		while i<self._size:
			current = next(BFS)
			if d < self.depth(current):
				print('')
				d += 1
			print(current._node._element , end=' ')
			i += 1
		print('')

#-----------------------------Functions-----------------------------------------
def build_tree(game,depth=1):
	tree = GameTree()
	root = tree.add_root(game._config)
	children = tree.add_children(game.update_config(),root)
	j=1
	while j < depth :
		newchild = []
		for i in children :
			temp = MetaGame(i._node._element)
			newchild += (tree.add_children(temp.update_config(),i))
		children = newchild
		j += 1
	return tree

def prob_winning(possible):
	"""Computes best possible move with Monte Carlo search"""
	prob = [0 for i in possible]
	total = [0 for i in possible]
	for i in range(500):
		choice = random.randrange(len(possible))
		total[choice] += 1
		temp=MetaGame(possible[choice])
		while temp._fullgame._status == 0:
			poss = temp.update_config()
			for i in poss:
				found=False
				temp=MetaGame(i)
				if temp.is_winner():
					prob[choice] += 1
					found=True
					break
				elif temp.is_loser():
					found=True
					break
			if not found:
				temp=MetaGame(poss[random.randrange(len(poss))])
	for i in range(len(possible)):
		prob[i] = prob[i] / total[i]
	choice = possible[prob.index(max(prob))]
	print(choice)

def default_mode(param):
	config = int(param[-1])
	game=MetaGame(config)
	possible=game.update_config()
	for i in possible:
		temp=MetaGame(i)
		if temp.is_winner():
			print(i)
			return
	prob_winning(possible)
	return

def tree_mode(param):
	config = int(param[-1])
	initconfig = int(param[-1])
	depth = int(param[-2])	
	game=MetaGame(config)
	tree=build_tree(game,depth)
	tree.show_tree()

def show_mode(param):
	config = int(param[-1])
	game = MetaGame(config)
	game.display()

#--------------------------------MAIN-------------------------------------------
if len(sys.argv) == 2 :
	"""mode par défaut"""
	default_mode(sys.argv)
elif len(sys.argv) == 4 and sys.argv[1] == 'a':
	"""mode arbre"""
	tree_mode(sys.argv)
elif len(sys.argv) == 3 and sys.argv[1] == 'p':
	"""mode affichage"""
	show_mode(sys.argv)
else:
	raise InputError("Mauvaise entrée pour un mode choisi, réessayer")
