#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

class HashTable:
    """Custom dictionary class"""

    def __init__(self,size):
        """Constructor of the class"""
        self.define_size(size)
        self._table = [None] * self._size
        self._hash_coeff = 33
        self._hash_MAD = [random.randint(0,self._prime-1),random.randint(0,self._prime-1)]

    def __getitem__(self,key):
        """Returns value associated with key"""
        value = key
        key = self.hash_function(key,value)
        if self._table[key] is not None:            #match found
            return self._table[key]
        return False

    def __setitem__(self,key,value):
        """Insert value associated with key in hash table"""
        key = self.hash_function(key)
        self._table[key] = value

    def define_size(self,size):
        """
        Assigns the size of the dict and primes for hashing.
        Primes taken from planetmath.org/goodhashtableprimes
        """
        listprimes = [7,53,97,193,389,769,1543,3079,6151,12289,24593,49157,98317,
                                        196613,393241,786433,1572869,3145739]
        for i in range(1,len(listprimes)-1):
            if size < 2**(i+4):
                self._size = listprimes[i]
                self._prime = listprimes[i+1]
                self._double_hash_prime = listprimes[i-1]
                break

    def hash_function(self,key,value=None):
        """Re-maps the key to an int"""
        key = self.horner([ord(i) for i in key])     #hash code
        key = self.hash_MAD(key)                     #compression fct
        key = self.double_hashing(key,value)         #double hashing
        return key

    def horner(self,key):
        """Polynomial accumulation as hash code with horner's rule"""
        if len(key) == 1:
            return key[0]
        else:
            return key[0] + self._hash_coeff  * self.horner(key[1:])

    def hash_MAD(self,key):
        """MAD Compression function"""
        return ((self._hash_MAD[0]*key + self._hash_MAD[1]) % self._prime) % self._size

    def double_hashing(self,key,value):
        """Double hashing function"""
        steps = self._double_hash_prime - (key % self._double_hash_prime)
        while (self._table[key] is not None and self._table[key] != value):
            key = (key + steps) % self._size
        return key

if __name__ == "__main__":
    """Perform tests here"""
    pass
