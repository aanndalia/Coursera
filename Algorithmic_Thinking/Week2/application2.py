# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 07:43:20 2014

@author: stree_001
"""

"""
Provided code for Application portion of Module 2
"""

# general imports
import urllib2
import random
import time
import math

# CodeSkulptor import
#import simpleplot
#import codeskulptor
#codeskulptor.set_timeout(60)

# Desktop imports
import matplotlib.pyplot as pyplot
from collections import deque

M = 3112 # network edges
N = 1347 # network nodes

"""
Provided code for application portion of module 2

Helper class for implementing efficient version
of UPA algorithm
"""

#import random

class UPATrial:
    """
    Simple class to encapsulate optimizated trials for the UPA algorithm
    
    Maintains a list of node numbers with multiple instance of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a UPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_nodes trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that each node number
        appears in correct ratio
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for _ in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        for dummy_idx in range(len(new_node_neighbors)):
            self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors

###########################
# From first assignment

def compute_in_degrees(digraph):
    """ 
    Computes the in degree of every node in the digraph
    """
    in_degrees = {}
    for key in digraph.keys():
        in_degrees[key] = 0
    for value in digraph.values():
        for item in value:
            if item in in_degrees:
                in_degrees[item] += 1
                
    return in_degrees

def in_degree_distribution(digraph):
    """
    Computes the in degree distribution 
    """
    in_degrees = compute_in_degrees(digraph)
    dist = {}
    for value in in_degrees.values():
        if value in dist:
            dist[value] += 1
        else:
            dist[value] = 1
    
    return dist
    
def make_complete_graph(num_nodes):
    """
    Creates a complete undirected graph
    """
    if num_nodes < 1:
        return {}
    
    complete_graph = {}
    for idx in range(num_nodes):
        complete_graph[idx] = set([])
        for each_idx in range(num_nodes):
            if idx != each_idx:
                complete_graph[idx].add(each_idx)
                
    return complete_graph
    
############################################
# Provided code

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)
    
def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    #N(N+M)
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order
    


##########################################################
# Code for loading computer network graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"


def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph
    
def make_ER_graph(num_nodes):
    """
    Creates a complete undirected graph
    """
    if num_nodes < 1:
        return {}
    
    p = float(M) / (N * (N-1) / 2)
    print "ER p=", p
    complete_graph = {}
    for idx in range(num_nodes):
        complete_graph[idx] = set([])
        for each_idx in range(num_nodes):
            if idx != each_idx and random.random() < p:
                complete_graph[idx].add(each_idx)
                #complete_graph[each_idx].add(idx)
                
    return complete_graph
    
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
    #remaining_nodes = ugraph.keys()
    remaining_nodes = set(ugraph.keys())
    connected_components = []
    while len(remaining_nodes) > 0:
        #i_node = remaining_nodes[0]
        i_node = remaining_nodes.pop()
        remaining_nodes.add(i_node)
        visited = bfs_visited(ugraph, i_node)
        connected_components.append(set(visited))
        #remaining_nodes = list(set(remaining_nodes).difference(visited))
        remaining_nodes = remaining_nodes.difference(visited)
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
        #for key, g_vals in ugraph.items():
        #    if node in g_vals:
        #        ugraph[key].remove(node)
        if len(ugraph) > 0:
            resiliency.append(largest_cc_size(ugraph))
        else:
            resiliency.append(0)
    return resiliency
    
def random_order(graph):
    graph_keys = graph.keys()
    random.shuffle(graph_keys)
    return graph_keys
    
def upa(total_nodes, initial_nodes):
    vertices = set(range(initial_nodes))
    graph = make_complete_graph(initial_nodes)
    upa_trial = UPATrial(initial_nodes)
    #print "upa_trial", upa_trial
    for idx in range(initial_nodes, total_nodes):
        vertices_prime = upa_trial.run_trial(initial_nodes)
        #print "vertices_prime", vertices_prime
        vertices.add(idx)
        graph[idx] = vertices_prime
        for v in vertices_prime:
            graph[v].add(idx)
    return graph  
    
def question1():
    network_graph = load_graph(NETWORK_URL)
    er_graph = make_ER_graph(N)
    #print "m=", math.floor(math.sqrt(N))
    p = float(M) / (N * (N-1) / 2)
    print "p=", p
    m=2
    upa_graph = upa(N, m)
    
    print "ng edges=", sum(len(edge) for edge in network_graph.values()) / 2
    print "er edges=", sum(len(edge) for edge in er_graph.values()) / 2
    print "upa edges=", sum(len(edge) for edge in upa_graph.values()) / 2
    
    network_random_nodes = random_order(network_graph)
    er_random_nodes = random_order(er_graph)
    upa_random_nodes = random_order(upa_graph)
    
    #print network_graph
    #print network_random_nodes
    start1 = time.time()
    network_resilience = compute_resilience(network_graph, network_random_nodes)
    print "network time:", time.time() - start1
    #print network_resilience
    print "len net:", len(network_resilience)
    start2 = time.time()
    er_resilience = compute_resilience(er_graph, er_random_nodes)
    print "er time:", time.time() - start2
    print "len er:", len(er_resilience)
    start3 = time.time()
    upa_resilience = compute_resilience(upa_graph, upa_random_nodes)
    print "upa time:", time.time() - start3
    print "len upa: ", len(upa_resilience)
    
    pyplot.figure(1)
    #pyplot.figure(1)
    pyplot.subplot(211)
    #pyplot.plot(x[0:100], y[0:100])
    pyplot.plot(range(N+1), network_resilience, '-r', label="network")
    pyplot.plot(range(N+1), er_resilience, '-b', label="ER p=" + str(p))
    pyplot.plot(range(N+1), upa_resilience, '-g', label="UPA m=" + str(m))
    
    pyplot.legend(loc='upper right')
    pyplot.axis([0,N+1,0,N+1])
    #pyplot.xscale('log')
    #pyplot.yscale('log')
    pyplot.xlabel('Number of nodes removed')
    pyplot.ylabel('Largest connected component')
    pyplot.title('Connection resiliency for different graph algorithms')
    #annotation = "m=",m,"p=",p
    #pyplot.annotate(s=annotation)
    pyplot.show()
    
def question4():
    #network_graph = load_graph(NETWORK_URL)
    er_graph = make_ER_graph(N)
    #print "m=", math.floor(math.sqrt(N))
    #p = float(M) / (N * (N-1) / 2)
    #print "p=", p
    m=2
    upa_graph = upa(N, m)
    
    #print "ng edges=", sum(len(edge) for edge in network_graph.values()) / 2
    #print "er edges=", sum(len(edge) for edge in er_graph.values()) / 2
    #print "upa edges=", sum(len(edge) for edge in upa_graph.values()) / 2
    
    #network_random_nodes = targeted_order(network_graph)
    er_random_nodes = targeted_order(er_graph)
    upa_random_nodes = targeted_order(upa_graph)
    
    #print network_graph
    #print network_random_nodes
    #network_resilience = compute_resilience(network_graph, network_random_nodes)
    #print network_resilience
    #print "len net:", len(network_resilience)
    er_resilience = compute_resilience(er_graph, er_random_nodes)
    #print "len er:", len(er_resilience)
    upa_resilience = compute_resilience(upa_graph, upa_random_nodes)
    #print "len upa: ", len(upa_resilience)
    
    pyplot.figure(1)
    #pyplot.figure(1)
    pyplot.subplot(211)
    #pyplot.plot(x[0:100], y[0:100])
    #pyplot.plot(range(N+1), network_resilience, '-r', label="network")
    pyplot.plot(range(N+1), er_resilience, '-b', label="ER p=" + str(p))
    pyplot.plot(range(N+1), upa_resilience, '-g', label="UPA m=" + str(m))
    
    pyplot.legend(loc='upper right')
    pyplot.axis([0,N+1,0,N+1])
    #pyplot.xscale('log')
    #pyplot.yscale('log')
    pyplot.xlabel('Number of nodes removed')
    pyplot.ylabel('Largest connected component')
    pyplot.title('Connection resiliency for different graph algorithms')
    #annotation = "m=",m,"p=",p
    #pyplot.annotate(s=annotation)
    pyplot.show()
    
def fast_targeted_order(ugraph):
    # N+N+NNM
    # 2N + MN^2 
    ugraph_keys = ugraph.keys()
    num_nodes = len(ugraph_keys)
#    degree_sets = {}
#    for key in ugraph:
#        degree = len(ugraph[key])
#        if degree in degree_sets:
#            degree_sets[degree].add(key)
#        else:
#            degree_sets[degree] = set([key])
    #print "ugraph", ugraph
    degree_sets = [set([]) for k_init in range(num_nodes)]
    #for k_init in range(num_nodes):
    #    degree_sets[k_init] = set([])
    
        
    for key in ugraph_keys:
        degree = len(ugraph[key])
        degree_sets[degree].add(key)
    
    #print "initial degree sets", degree_sets
    #max_degree = max(degree_sets.keys())        
    L= []
    #i = 0
    
    for k in range(num_nodes - 1, -1, -1):
        while len(degree_sets[k]) > 0:
            u = degree_sets[k].pop()
            #degree_sets[k].add(u)
            #degree_sets[k] = degree_sets[k].difference(set([u]))
            #degree_sets[k] = degree_sets[k].difference(u)
            for v in ugraph[u]:
                #print "v=",v,"u=",u,"ugraph_u=",ugraph[u]
                #print "ugraph", ugraph
                if v in ugraph:
                    d = len(ugraph[v])
                    #print "d=",d
                    #print "degree_sets_d", degree_sets[d]
                    #print "degree_sets_d-1", degree_sets[d-1]
                    degree_sets[d] = degree_sets[d].difference(set([v]))
                    degree_sets[d-1] = degree_sets[d-1].union(set([v]))
            
            #L[i] = u
            #i += 1
            L.append(u)
            ugraph.pop(u)
    return L

def targeted_order_test():
    num_nodes = range(10, 1000, 10)
    m = 5
    slow_time = []
    fast_time = []
    #print "num_nodes", num_nodes
    for n in num_nodes:
        print "n", n
        upa_graph = upa(n, m)
        #print "g", upa_graph
        start_slow = time.time()
        targeted_order(upa_graph)
        slow_time.append(time.time() - start_slow)
        
        start_fast = time.time()
        fast_targeted_order(upa_graph)
        fast_time.append(time.time() - start_fast)
        
    pyplot.figure(1)
    pyplot.subplot(211)
    pyplot.plot(num_nodes, slow_time, '-r', label="targeted_order")
    pyplot.plot(num_nodes, fast_time, '-b', label="fast_targeted_order")
    pyplot.legend(loc='upper right')
    pyplot.axis([0,1000,0,max(slow_time)])
    pyplot.xlabel('Number of Nodes')
    pyplot.ylabel('Time Elapsed')
    pyplot.title('Time for targeted order algorithms to run on UPA graph on Desktop')
    pyplot.show()
    
#targeted_order_test()
    
#question1()
    
question4()

    
    
    





