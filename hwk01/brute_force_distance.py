"""
COMP 182 
homework 1
Zichao Wang
"""

import itertools
import sys
sys.path.append("/Users/zichaowang/Dropbox/RICE/year spring 15/COMP 182")
import provided
import comp182

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
    inf = float("inf") # define infinity
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
                
        
g1 = {
      0: {1,2,3},
      1: {0,4},
      2: {0,5},
      3: {0,6},
      4: {1},
      5: {2},
      6: {3}
      }
      
g2 = {0:{1,2,3,4,5,6,7,8},
      1:{0,2,8},
      2:{0,1,3},
      3:{0,2,4},
      4:{0,3,5},
      5:{0,4,6},
      6:{0,5,7},
      7:{0,6,8},
      8:{0,1,7}
      }
      
g3 = {0: {1,2,3},
      1: {0,4,5},
      2: {0,3,6},
      3: {0,2,7},
      4: {1,3,5,8},
      5: {1,4,9},
      6: {2,7,10},
      7: {3,6,8,10},
      8: {4,7,9,11},
      9: {5,8,11},
      10:{6,7,11},
      11:{8,9,10},
      }

result1 = brute_force_distance(g1,0)
result2 = brute_force_distance(g2,0)
#result3 = brute_force_distance(g3,0)
"""
g1 = provided.upa(4,4)
g2 = provided.upa(8,4)
g3 = provided.upa(16,4)
g4 = provided.upa(32,4)

result1 = comp182.time_func(brute_force_distance,[g1,0])
result2 = comp182.time_func(brute_force_distance,[g2,0])
result3 = comp182.time_func(brute_force_distance,[g3,0])
result4 = comp182.time_func(brute_force_distance,[g4,0])
"""