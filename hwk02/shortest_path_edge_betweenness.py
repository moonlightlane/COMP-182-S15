'''
COMP 182 S15
Homework 2 Part 3
Author: Zichao Wang
'''
import sys
sys.path.append("/Users/zichaowang/Dropbox/RICE/year spring 15/COMP 182")
import modified_bfs
import compute_flow

def shortest_path_edge_betweenness(g):
	'''
	computes the betweenness of each edge of a graph

	argument:
	g -- input graph

	return:
	a dictionary in which the keys are frozensets with 
	two elements that represent an edge in the graph 
	and the values are the betweenness value for the 
	corresponding edge
	'''
	# variable definition
	betweenness = {}

	# run compute flow and bfs for each node in the graph
	for startnode in g:
		dist, npaths = modified_bfs.bfs(g, startnode)
		flow = compute_flow.compute_flow(g,dist,npaths)
		betweenness = {x: betweenness.get(x, 0) + flow.get(x, 0) for x in set(betweenness).union(flow)}
	return betweenness

# test
'''
g0 = {1: set([2, 3]), 2: set([1, 3]), 3: set([1, 2, 7]), 4: set([5, 6]), 
5: set([4, 6]), 6: set([4, 5, 7]), 7: set([3, 6]), 8: set([9, 12]), 
9: set([8, 10, 11]), 10: set([9, 11]), 11: set([9, 10]), 12: set([8, 13, 14]), 
13: set([12, 14]), 14: set([12, 13])} 
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
betweenness = shortest_path_edge_betweenness(g1)
print betweenness
