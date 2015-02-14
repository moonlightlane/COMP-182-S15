'''
COMP 182 S15
Homework 2 TEST FILE
Author: Zichao Wang
'''
from collections import deque
import sys
sys.path.append("/Users/zichaowang/Dropbox/RICE/year spring 15/COMP 182")
import provided
import comp182


# test of compute_flow
import modified_bfs
import compute_flow
import bookgraphs
rice_fb = comp182.read_graph('rice-facebook.repr')
dist, npaths = modified_bfs.bfs(rice_fb,1077)
flow = compute_flow.compute_flow(rice_fb,dist,npaths)
print len(flow)

# test of partition algorithm