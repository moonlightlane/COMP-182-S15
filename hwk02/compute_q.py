'''
COMP 182 S15
Homework 2 Part 4
Author: Zichao Wang
'''
import numpy
def compute_q(g,c):
	'''
	compute Q value, the modularity measure of a graph

	arguments:
	g -- input graph
	c -- a list of sets of nodes taht form a partition
	     of the nodes of graph g

	return:
	a single floating point number , the Q value
	'''
	# find the total number of edges of a graph
	edge_total = 0
	for node in g:
		edge_total += len(g[node])
	edge_total = edge_total/2

	# find trace of each partition and D matrix values
	D = numpy.zeros((len(c),len(c))) # initialize D matrix
	row = 0 # from the first row
	while row < len(c): # loop through each partition (row = the row_th item in c)
		trace_each = 0
		d_each = 0
		for node in c[row]: # for each node in partition
			for neighbor in g[node]:
				if {neighbor} & c[row]: # trace + 1 when neighbor of this node is also in partition
					trace_each += 1
				else: # d matrix item + 1 when neighbor of this node is not in partition
					idx = 0
					# while loop to find which partition this neighbor is in
					while idx < len(c):
						if {neighbor}&c[idx]!=set(): # if neighbor in this partition with index = idx in c
							col = idx 
							D[row,col] += float(1)/float(edge_total)
						idx += 1
		D[row,row] = (float(trace_each)/2/float(edge_total))
		row += 1
	# calculate Q value
	trace = 0
	pointer = 0
	while pointer < len(c):
		trace += D[pointer,pointer]
		pointer += 1
	Q = trace - numpy.sum(numpy.dot(D,D))

	return Q
'''
g = {
	0: {1,2},
	1: {0,3},
	2: {0,3,4},
	3: {1,2,5},
	4: {2,5,6},
	5: {3,4},
	6: {4}
	} 
c = [{0,1,2,3},{4,5,6}]
Q = compute_q(g,c)
print Q
'''



