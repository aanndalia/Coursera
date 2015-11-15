# -*- coding: utf-8 -*-
"""
Created on Sun Sep 14 17:01:28 2014

@author: stree_001
"""
from collections import deque


def bfs_visited(ugraph, start_node):
    """
    Performs breath first search to obtain all nodes that can be visited
    from start_node
    """
    queue = deque()
    queue.clear()
    visited = set([start_node])
    queue.append(start_node)
    while len(queue) > 0:
        j_item = queue.popleft()
        for neighbor in ugraph[j_item]:
            if neighbor not in visited:
                visited = visited.union(set([neighbor]))
                queue.append(neighbor)
    return visited
    
def cc_visited(ugraph):
    """
    Returns all connected components of ugraph
    """
    remaining_nodes = ugraph.keys()
    connected_components = []
    while len(remaining_nodes) > 0:
        i_node = remaining_nodes[0]
        visited = bfs_visited(ugraph, i_node)
        connected_components.append(set(visited))
        remaining_nodes = list(set(remaining_nodes).difference(visited))
    return connected_components
    
def largest_cc_size(ugraph):
    """
    Returns size of largest connected component
    in ugraph
    """
    connected_components = cc_visited(ugraph)
    return max(len(comp) for comp in connected_components)

def compute_resilience(ugraph, attack_order):
    """
    Computes the resiliecies of the graph when removes nodes in
    the specificied attack_order for ugraph.
    """
    resiliency = [largest_cc_size(ugraph)]
    for node in attack_order:
        ugraph.pop(node)
        for g_vals in ugraph.values():
            if node in g_vals:
                g_vals.remove(node)
        if len(ugraph) > 0:
            resiliency.append(largest_cc_size(ugraph))
        else:
            resiliency.append(0)
    return resiliency
    

    
#def main():
#    g = {'a': set(['b','c','e']), 'b': set(['a']), 'c': set(['a','d','e']), 'd': set(['c','e']), 'e': set(['a','c','d']),'f': set([])}
#    print cc_visited('b', 'd')
#    print compute_resilience(g, ['b','d'])

#main()