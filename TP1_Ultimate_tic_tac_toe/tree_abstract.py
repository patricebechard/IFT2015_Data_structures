# -*- coding: utf-8 -*-
"""
Code Fragments 7.7, 7.8, 8.1 and 8.2 from Goodrich, Tamassia & Goldwasser.
"""

class LinkedQueue:
    """FIFO Queue implementation using a singly linked list for storage"""
    
    class _Node:
        """Lightweight, nonpublic class for storing a singly linked node"""
        __slots__='_element','_next'        #streamline memory usage
        
        def __init__(self,element,next):    #initialize node's field
            self._element=element           #reference to user's element
            self._next=next                 #reference to next node
            
    def __init__(self):
        """Create an empty queue"""
        self._head=None
        self._tail=None
        self._size=0                #number of queue elements
    
    def __len__(self):
        """Return number of elements in queue"""
        return self._size
        
    def is_empty(self):
        """Return True if queue is empty, False otherwise"""
        return self._size==0
    
    def first(self):
        """Return (but do not remove) element at the front of the queue
        Raise Empty exception if queue is empty.
        """
        if self._size==0:
            raise Empty('Queue is empty')
        return self._head._element          #front aligned with head of list
    
    def dequeue(self):
        """Return and remove element at the front of the queue
        Raise Empty exception if queue is empty.
        """
        if self._size==0:
            raise Empty('Queue is empty')
        answer=self._head._element
        self._head=self._head._next
        self._size-=1
        if self.is_empty():             #special case as queue is empty
            self._tail=None                 #removed head had been the tail
        return answer
        
    def enqueue(self,e):
        """Add a note at the end of the queue"""
        newest=self._Node(e,None)               #node will be the new tail
        if self.is_empty():
            self._head=newest           #special case if queue was empty
        else:
            self._tail._next=newest
        self._tail=newest               #update reference to tail node
        self._size+=1


class Tree:
    """Abstract base class representing a tree structure"""
    
    #-----------------Nested Position class-----------------
    class Position:
        """An abstraction representing the location of a single element."""
        
        def element(self):
            """Return the element stored at this Position"""
            raise NotImplementedError('Must be implemented by subclass')
            
        def __eq__(self,other):
            """Return True if other Position represents the same location"""
            raise NotImplementedError('Must be implemented by subclass')
        
        def __ne__(self,other):
            """Return True if other does not represent the same location"""
            return not (self==other)        #opposite of __eq__
    
    #----------------Abstract methods that concrete subclass must support--
    def root(self):
        """Return Position representing the tree's root (None if empty)"""
        raise NotImplementedError('Must be implemented by subclass')
    
    def parent(self,p):
        """Return Position representing p's parent (None if p is root)"""
        raise NotImplementedError('Must be implemented by subclass')

    def num_children(self,p):
        """Return the number of children that Position p has"""
        raise NotImplementedError('Must be implemented by subclass')
    
    def children(self,p):
        """Generate an iterator of Positions representing p's children"""
        raise NotImplementedError('Must be implemented by subclass')

    def __len__(self):
        """Return the total number of elements in the tree"""
        raise NotImplementedError('Must be implemented by subclass')

    #---------------Concrete methods implemented in the class----
    def is_root(self,p):
        """Return True if Position p is the root of the tree"""
        return self.root() == p

    def is_leaf(self,p):
        """Return True if Position p does not have any children"""
        return self.num_children(p) == 0

    def is_empty(self):
        """Return True if the tree is empty"""
        return len(self) == 0

    def depth(self,p):
        """Return the number of levels separating Position p from the root"""
        if self.is_root(p):
            return 0
        else:
            return 1+self.depth(self.parent(p))
            
    def _height1(self,p):        #works, but O(n^2) worst case
        """Return the height of the tree"""
        return max(self.depth(p) for p in self.positions() if self.is_leaf(p))
    
    def _height2(self,p):        #time is linear in size of subtree
        """Return the height of the subtree rooted at Position p"""
        if self.is_leaf(p):
            return 0
        else:
            return 1 + max(self._height2(c)for c in self.children(p))
    
    def height(self,p=None):        #public, calls private method _height2
        """Return the height of the subtree rooted at Position p.
        if p is None, return the height of the entire tree.
        """
        if p is None:
            p = self.root()
        return self._height2(p) #starts _height2 recursion
        
    def __iter__(self):
        """Generates an iteration of the tree's elements"""
        for p in self.position():       #use same order as positions()
            yield p.element()           #but yield each element
    
    def positions(self):
        """Generate an iteration of the tree's positions"""
        return self.preorder()          #return entire preorder iteration
    
    def preorder(self):
        """Generate a preorder iteration of positions in the tree"""
        if not self.is_empty():
            for p in self._subtree_preorder(self.root): #start recursion
                yield p
    
    def _subtree_preorder(self,p):
        """Generate a preorder iteration of positions in subtree rooted at p"""
        yield p             #visit p before its subtree
        for c in self.children(p):      #for each child c
            for other in self._subtree_preorder(c): #do preorder of c's subtrees
                yield other                 #yielding each to our caller
        
    def postorder(self):
        """Generate a postorder iteration of positions in the tree"""
        if not self.is_empty():
            for p in self._subtree_postorder(self.root):    #start recursion
                yield p
    
    def _subtree_postorder(self,p):
        """Generate a postorder iteration of positions in subtree rooted at p"""
        for c in self.children(p):              #for each child in c
            for other in self._subtree_postorder(self,p):   #do postorder of c's subtrees
                yield other                 #yielding each to our caller
        yield p                             #visit p after its subtree
    
    def breadthfirst(self):
        """Generate a breadth-first iteration of positions in the tree"""
        if not self.is_empty():
            fringe=LinkedQueue()            #known positions not yet yielded
            fringe.enqueue(self.root())     #starting with the root
            while not fringe.is_empty():
                p=fringe.dequeue()          #remove front from queue
                yield p                     #report this position
                for c in self.children(p):
                    fringe.enqueue(c)        #add children to back of the queue