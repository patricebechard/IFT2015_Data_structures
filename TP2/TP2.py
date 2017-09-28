#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashtable

#-------------------------------Fonctions--------------------------------------

def read_dictionary(file):
    f = open(file)
    numLines = sum(1 for line in f)
    dictionary = hashtable.HashTable(numLines)
    alphabet = []
    f.seek(0)
    for line in f:
        value = line.strip()
        for char in value:          #every char present in dictionary is memorized
            alphabet.append(char)
        alphabet = list(set(alphabet))          #deleting duplicates
        dictionary[value] = value
    return dictionary, sorted(alphabet)

def read_input(file):
    text = open(file).readline().strip()
    text = text.replace("'","' ")                        #replace ' with spaces
    text = text.split()
    capitalize = [False] * len(text)
    punctuation = [''] * 2 * len(text)
    for i in range(len(text)):
        text[i] = look_for_punctuation(text[i],punctuation,i)
        text[i] = look_for_capital_letters(text[i],capitalize,i)
    return text, capitalize, punctuation

def look_for_punctuation(word,punctuation,i):
    exclude = ''.join('.,!?;:"' + "'")
    #look for punctuation at beginning of word
    for char in word:
        if char in exclude:
            punctuation[2*i] = ''.join(punctuation[2*i] + char)
        else:
            break
    #look for punctuation at end of word
    for char in reversed(word):
        if char in exclude:
            punctuation[2*i+1] = ''.join(char + punctuation[2*i+1])
        else:
            break
    return ''.join(char for char in word if char not in exclude)

def look_for_capital_letters(word,capitalize,i):
    if not word.islower():                       #look for capital letters
        capitalize[i] = True
    return word.lower()

def suggested_words(word,alphabet):
    """Outputs a list of suggested words to try in dictionary"""
    suggested = []

    for i in range(len(word)-1):                        #interversion
        temp = ''.join(word[:i] + word[i+1] + word[i] + word[i+2:])
        if dictionary[temp]:
            suggested.append(temp)
    for i in range(len(word)+1):                        #add letter
        for letter in alphabet:
            temp = ''.join(word[:i] + letter + word[i:])
            if dictionary[temp]:
                suggested.append(temp)
    for i in range(len(word)):                          #remove letter
        temp = ''.join(word[:i] + word[i+1:])
        if dictionary[temp]:
            suggested.append(temp)
    for i in range(len(word)):                          #swap letter
        for letter in alphabet:
            temp = ''.join(word[:i] + letter + word[i+1:])
            if dictionary[temp]:
                suggested.append(temp)
    for i in range(1,len(word)):                        #split in two words
        temp = ''.join(word[:i] + ' ' + word[i:])
        w1, w2 = temp.split(' ')
        if dictionary[w1] and dictionary[w2]:
            suggested.append(temp)
    return list(set(suggested))                         #deleting duplicates

#----------------------------------Main----------------------------------------

dict = 'dict.txt'
dictionary, alphabet = read_dictionary(dict)

input = 'input.txt'
words,capitalize,punctuation = read_input(input)

output = ''
k = 0                                       #keep track of where we are
for word in words:
    if dictionary[word] == word:            #word in dictionary
        if capitalize[k]:
            word = ''.join(word[0].upper() + word[1:])
        output += word + ' '
    else:
        suggestions = suggested_words(word,alphabet)
        if capitalize[k]:                   #re-insert capital letters
            word = ''.join(word[0].upper() + word[1:])
            for j in range(len(suggestions)):
                suggestions[j] = ''.join(suggestions[j][0].upper() + suggestions[j][1:])

        if not suggestions:             #list is empty
            suggestions = ''
        else:
            temp = ''.join([suggestions[i] + ', ' for i in range(len(suggestions)-1)])
            suggestions = temp + suggestions[-1]
        output += punctuation[2*k] + '[' + word + '](' + suggestions + ')' + punctuation[2*k+1] + ' '
    k += 1

print(output)