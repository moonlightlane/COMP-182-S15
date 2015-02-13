'''
COMP 182 S15
Homework 2 Part 2
Author: Zichao Wang
'''
from collections import deque
import operator
import sys
sys.path.append("/Users/zichaowang/Dropbox/RICE/year spring 15/COMP 182")
import provided
import comp182

def compute_flow(g,dist,paths):
	'''
	computes the flow of every edge of a graph

	arguments:
	g 	  -- input graph
	dist  -- distance from every node to the start node defined in bfs
	paths -- number of shortest paths flowing through nodes

	return:
	a dictionary in which the keys are frozensets with two elements that 
	represent an edge in the graph and the values are the flow value for 
	the corresponding edge
	'''
	# delete node with infinite length (not within reach of the startnode)
	inf_node = []
	for node in dist:
		if dist[node] == float('inf'):
			inf_node.append(node)
	dist = {key: dist[key] for key in dist if key not in inf_node}

	d_max = dist[max(dist, key=lambda i:dist[i])] # get the maximum distance of a node from the start node
	d = d_max # counter. first start with nodes with greatest distance. so initialized as d_max
	f_node = {} # flow of a node
	for node in g: # initialize every node flow to be 1
		f_node[node] = 1
	f_edge = {} # flow of an edge. keys are frozensets

	while d >= 0: # before the start node is reached
		node_d = []
		for n, distance in dist.iteritems(): # get all nodes at distance d, store the nodes in list node_d
			if distance == d:
				node_d.append(n)
		for node in node_d: # calculate flow of a node and its incoming edges
			if d >= d_max:
				pass			
			else:
				for neighbor in g[node]: # neighbor in a lower layer
					if dist[neighbor] == d + 1: # the neighbor needs to be in the next layer (outgoing flows of the node)
						f_node[node] += float(f_edge[frozenset([node, neighbor])]) # add up all the outgoing flows from this node
			for neighbor in g[node]: # neighbor in a upper layer
				if dist[neighbor] == d - 1: # calculate flow for each of the incoming edge to the node
					f_edge[frozenset([node, neighbor])] = float(f_node[node]) * float(paths[neighbor]) / float(paths[node])

		d -= 1
	return f_edge



