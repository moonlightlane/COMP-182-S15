'''
COMP 182 S15
Homework 2
Author: Zichao Wang
'''
from collections import deque
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
	d_n = {} # initialize distance and number of incoming edges for every node
	result = {} # initialize the dictionary of tuple. 
    			# The key correspond to the node. 
    			# e.g. result[0] stores corresponding data for node 0.

	# assign infinite length and incoming edge to every node
	for node in g:
		d_n[node] = [inf, inf]

	result[startnode] = (0,1) # assign start node d = 0, n = 1
	Q.append(startnode) # attach the start node to the queue

	while len(Q) > 0:
		j = Q.popleft() # get a node from the queue
    	for neighbor in g[j]: # examine all neighbor nodes of the above node
    		if d_n[neighbor][0] == inf: # if this neighbor is not discovered
    			d_n[neighbor][0] = d_n[j][0] + 1 # assign length to this neighbor
    			d_n[neighbor][1] = d_n[j][1] # assign number of incoming edges to this neighbor
    			Q.append(neighbor) # attach this neighbor to the queue
    		elif d_n[neighbor][0] == d_n[j][0] + 1: # if this neighbor has been discovered
    			d_n[neighbor][1] += d_n[j][1] # add the incoming edges of node j to its neighbor
    		result[neighbor] = (d_n[neighbor][0],d_n[neighbor][1]) # assign the corresponding tuple to result
	return result

# test
g1 = {
	0: {1,2},
	1: {0,3},
	2: {0,3,4},
	3: {1,2,5},
	4: {2,5,6},
	5: {3,4},
	6: {4}
	}    
g1_result = bfs(g1, 0)
print g1_result