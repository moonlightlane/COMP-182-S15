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

# test 1#
""" 
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

result1 = bfs(g1,0)
result2 = bfs(g2,0)
result3 = bfs(g3,0)
"""

# test 2 #
g4 = provided.upa(500,5)
g5 = provided.upa(500,20)
g6 = provided.upa(500,80)
g7 = provided.upa(500,320)

result4 = comp182.time_func(bfs,[g4,0])
result5 = comp182.time_func(bfs,[g5,0])
result6 = comp182.time_func(bfs,[g6,0])
result7 = comp182.time_func(bfs,[g7,0])
