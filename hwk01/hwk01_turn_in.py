"""
COMP 182 
homework 1
Zichao Wang
"""
import sys
# TODO: change the following path to where you put provided.py and comp182.py
sys.path.append("/Users/zichaowang/Dropbox/RICE/year spring 15/COMP 182")
import provided
import comp182
import itertools
from collections import deque

inf = float("inf") # define infinity

def brute_force_distance(g, startnode):
    """
    Brute force algorithm to calculate distance 
    from startnode to all nodes in g.
    
    Arguments:
    g         -- a graph
    startnode -- the start node
            
    Returns:
    a dictionary where the keys are nodes in g and
    the values are the distance from startnode to 
    that node.
    
    """
    result = {}
    
    # assign infinite length to every node
    for node in g:
        result[node] = inf
    
    # assign startnode length = 0
    result[startnode] = 0
    
    # create list of remaining nodes
    nodes = []
    for node in g:
        nodes.append(node)
    max_diameter = len(nodes) - 1 # assign biggest possible length in g
    nodes.remove(startnode)
    
    c = 1 # initial condition for while loop
    nodes_in_between = []
    nodes_in_between.append(startnode)
    while c <= max_diameter and len(nodes) != 0:
        c_permutation = list(itertools.permutations(nodes,c))
        for each_permutation in c_permutation:
            nodes_in_between[1:] = []
            connected = True
            for node in each_permutation:
                nodes_in_between.append(node)
            for i in range(0,c):
                if len({nodes_in_between[i+1]} & g[nodes_in_between[i]]) == 0:
                    connected = False
                    break
            if connected == True and result[nodes_in_between[c]] == inf:
                result[nodes_in_between[c]] = c
                #nodes.remove(nodes_in_between[c])
        c += 1
        
    return result


def bfs(g,startnode):
    """
    BFS algorithm to calculate distance 
    from startnode to all nodes in g.
    
    Arguments:
    g         -- a graph
    startnode -- the start node
            
    Returns:
    a dictionary where the keys are nodes in g and
    the values are the distance from startnode to 
    that node.
    
    """
    Q = deque('') # initialize Q to be empty queue

    result = {}
    # assign infinite length to every node
    for node in g:
        result[node] = inf
    result[startnode] = 0 # assign start node length = 0
    Q.append(startnode) # attach the start node to the queue
    
    while len(Q) > 0:
        j = Q.popleft()
        for neighbor in g[j]:
            if result[neighbor] == inf:
                result[neighbor] = result[j] + 1
                Q.append(neighbor)
    
    return result


def connected_components(graph):
    """
    computes the set of connected components of a graph 

    Arguments: 
    graph -- input graph

    Return: 
    a list of sets, where each set contains 
    the nodes belonging to that connected component
    """
    import random
    import sys
    # TODO: change this path to where you put the bfs.py file
    sys.path.append("/Users/zichaowang/Dropbox/RICE/year spring 15/COMP 182")
    import bfs

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