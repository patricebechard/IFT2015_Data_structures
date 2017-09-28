# -*- coding: utf-8 -*-
# @Author: Patrice Béchard 20019173
# @Date:   2017-03-20 21:23:48
# @Last Modified time: 2017-03-20 21:53:45
#
# 
# test generating a tree configuration

import random

config=0


x=random.randrange(81)

print(x)

config = config ^ (0<<162) | (x<<162)				#set as last cell updated
already=[x]
for i in range(50):
	cell = random.randrange(81)
	while cell in already:
		cell=random.randrange(81)
	already.append(cell)
	config = config ^ (1<<(161-(2*cell+(i+1)%2)))	#update cell



config = config ^ (1<<(161-(2*x+(i+1)%2)))

print(config)
print(bin(config))