import random
import sys
# TODO: change this path to where you put the bfs.py file
sys.path.append("/Users/zichaowang/Dropbox/RICE/year spring 15/COMP 182")
import comp182
import provided
import bfs

inf = float("inf") # define infinity

def connected_components(graph):
	"""
	computes the set of connected components of a graph 

	Arguments: 
	graph -- input graph

	Return: 
	a list of sets, where each set contains 
	the nodes belonging to that connected component
	"""
	# initialize remaining nodes set
	remainingNodes = set()
	for node in graph:
		remainingNodes.add(node)

	# initialize 
	CC = []

	while len(remainingNodes) != 0:
		i = random.sample(remainingNodes,1)[0]
		d = bfs.bfs(graph,i)
		W = set()
		for u in remainingNodes:
			if d[u] != inf:
				W.add(u)
		CC.append(W)
		for node in W:
			remainingNodes.remove(node)
	return CC
	
