"""
COMP 182 
homework 1
Zichao Wang
"""

from collections import deque
import sys
sys.path.append("/Users/zichaowang/Dropbox/RICE/year spring 15/COMP 182")
import provided
import comp182

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
    
    inf = float("inf") # define infinity
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

