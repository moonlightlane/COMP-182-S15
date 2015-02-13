'''
COMP 182 S15
Homework 2 Part 1
Author: Zichao Wang
'''
from collections import deque
import operator
import sys
sys.path.append("/Users/zichaowang/Dropbox/RICE/year spring 15/COMP 182")
import provided
import comp182

def bfs(g, startnode):
	'''
	modified version of bfs algorithm useful for
	computing edge betweenness

	Arguments: 
	g		  -- input graph
	stargnode -- the node to start with

	Return:
	a tuple that contains d, the distance from 
	a node to the startnode, and n, the incoming
	edges to a node.
	'''
	Q = deque('') # initialize Q to be empty queue
	inf = float("inf") # define infinity
	distance = {} # initialize the dictionary of tuple. 
	paths = {}

	# assign infinite length and incoming edge to every node
	for node in g:
		distance[node] = inf
		paths[node] = 0

	distance[startnode] = 0 # assign start node d = 0, n = 1
	paths[startnode] = 1

	Q.append(startnode) # attach the start node to the queue
	while len(Q) > 0:
		j = Q.popleft() # get a node of the queue
		for neighbor in g[j]: # for each neighbor of this node
			if distance[neighbor] == inf: # if this neighbor is not discovered
				distance[neighbor] = distance[j] + 1 # distance + 1
				paths[neighbor] = paths[j] # path = path of previous node
				Q.append(neighbor) # put this neighbor into queue
			elif distance[neighbor] == distance[j]+1: # if this neighbor has been discovered
				paths[neighbor] = paths[j] + paths[neighbor] # path = path of node + path of neighbor
	return (distance,paths) # return distance from starting node and path through node
# test
'''
g1 = {
	0: {1,2},
	1: {0,3},
	2: {0,3,4},
	3: {1,2,5},
	4: {2,5,6},
	5: {3,4},
	6: {4}
	}    
g1_result = bfs(g1, 6)
print g1_result
'''