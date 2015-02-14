'''
COMP 182 S15
Homework 2 turn in
'''
from collections import deque
import sys
sys.path.append("/Users/zichaowang/Dropbox/RICE/year spring 15/COMP 182")
import comp182
import provided
import random
import bfs
import modified_bfs
import compute_flow
import numpy

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
			if d[u] != float('inf'):
				W.add(u)
		CC.append(W)
		for node in W:
			remainingNodes.remove(node)
	return CC

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
		flow = compute_flow(g,dist,npaths)
		betweenness = {x: betweenness.get(x, 0) + flow.get(x, 0) for x in set(betweenness).union(flow)}
	return betweenness

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

# provided function
def remove_edges(g, edgelist):
    """
    Remove the edges in edgelist from the graph g.

    Arguments:
    g -- undirected graph
    edgelist - list of edges in g to remove

    Returns:
    None
    """
    for edge in edgelist:
        (u, v) = tuple(edge)
        g[u].remove(v)
        g[v].remove(u)   

def gn_graph_partition(g):
    """
    Partition the graph g using the Girvan-Newman method.

    Requires connected_components, shortest_path_edge_betweenness, and
    compute_q to be defined.  This function assumes/requires these
    functions to return the values specified in the homework handout.

    Arguments:
    g -- undirected graph

    Returns:
    A list of tuples where each tuple contains a Q value and a list of
    connected components.
    """
    ### Start with initial graph
    c = connected_components(g)
    q = compute_q(g, c)
    partitions = [(q, c)]

    ### Copy graph so we can partition it without destroying original
    newg = comp182.copy_graph(g)
    ### Iterate until there are no remaining edges in the graph
    while True:
        ### Compute betweenness on the current graph
        btwn = shortest_path_edge_betweenness(newg)
        #print 'shortest path edge betweenness function working'
        if not btwn:
            ### No information was computed, we're done
            break

        ### Find all the edges with maximum betweenness and remove them
        maxbtwn = max(btwn.values())
        maxedges = [edge for edge, b in btwn.iteritems() if b == maxbtwn]
        remove_edges(newg, maxedges)

        ### Compute the new list of connected components
        c = connected_components(newg)
        #print 'connected componets function working'
        if len(c) > len(partitions[-1][1]):
            ### This is a new partitioning, compute Q and add it to
            ### the list of partitions.
            q = compute_q(g, c)
            #print 'compute Q function working'
            partitions.append((q, c))

    return partitions

'''
# test
fig3_14g = {1: set([2,3]),
            2: set([1,3]),
            3: set([1,2,7]),
            4: set([5,6]),
            5: set([4,6]),
            6: set([4,5,7]),
            7: set([3,6,8]),
            8: set([7,9,12]),
            9: set([8,10,11]),
            10: set([9,11]),
            11: set([9,10]),
            12: set([8,13,14]),
            13: set([12,14]),
            14: set([12,13])}
fig3_15g = {1: set([2,3]),
            2: set([1,3,4,5]),
            3: set([1,2,4,5]),
            4: set([2,3,5]),
            5: set([2,3,4,6,7]),
            6: set([5,7]),
            7: set([5,6,8,9,10]),
            8: set([7,9,10]),
            9: set([7,8,10,11]),
            10: set([7,8,9,11]),
            11: set([9,10])}
g1 = {
	0: {1,2},
	1: {0,3},
	2: {0,3,4},
	3: {1,2,5},
	4: {2,5,6},
	5: {3,4},
	6: {4}
	} 
g1_partition = gn_graph_partition(g1)
fig3_14g_partition = gn_graph_partition(fig3_14g)
fig3_15g_partition = gn_graph_partition(fig3_15g)
print g1_partition, '\n'
print fig3_14g_partition, '\n'
print fig3_15g_partition
'''
'''
# part 3 A
fig3_13g = {1: set([32, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 18, 20, 22]), 
            2: set([1, 3, 4, 8, 14, 18, 20, 22, 31]), 
            3: set([1, 2, 4, 33, 8, 9, 10, 14, 28, 29]), 
            4: set([1, 2, 3, 8, 13, 14]), 
            5: set([1, 11, 7]), 
            6: set([1, 11, 17, 7]), 
            7: set([1, 5, 6, 17]), 
            8: set([1, 2, 3, 4]), 
            9: set([1, 34, 3, 33, 31]), 
            10: set([34, 3]), 
            11: set([1, 5, 6]), 
            12: set([1]), 
            13: set([1, 4]), 
            14: set([1, 2, 3, 4, 34]), 
            15: set([33, 34]), 
            16: set([33, 34]), 
            17: set([6, 7]), 
            18: set([1, 2]), 
            19: set([33, 34]), 
            20: set([1, 2, 34]), 
            21: set([33, 34]), 
            22: set([1, 2]), 
            23: set([33, 34]), 
            24: set([33, 26, 28, 34, 30]), 
            25: set([32, 26, 28]), 
            26: set([24, 25, 32]), 
            27: set([34, 30]), 
            28: set([24, 25, 34, 3]), 
            29: set([32, 34, 3]), 
            30: set([24, 33, 34, 27]), 
            31: set([9, 2, 34, 33]), 
            32: set([1, 34, 33, 25, 26, 29]), 
            33: set([32, 34, 3, 9, 15, 16, 19, 21, 23, 24, 30, 31]), 
            34: set([32, 33, 9, 10, 14, 15, 16, 19, 20, 21, 23, 24, 27, 28, 29, 30, 31])}
fig3_13g_partition = gn_graph_partition(fig3_13g)
# construct result disctionary for plotting
result = {}
idx = 0
while idx < len(fig3_13g_partition):
	result[idx] = fig3_13g_partition[idx][0]
	idx += 1
comp182._plot_dict_bar(result, xmin=None, label=None)
print fig3_13g_partition[1]
'''

# part 3 B

rice_fb = comp182.read_graph('rice-facebook.repr')
rice_fb_partition = gn_graph_partition(rice_fb)
result = {}
idx = 0
while idx < len(rice_fb_partition):
	result[idx] = rice_fb_partition[idx][0]
	idx += 1
comp182._plot_dict_bar(result, xmin=None, label=None)
comp182.show()