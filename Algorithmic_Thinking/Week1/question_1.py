# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

"""
Provided code for Application portion of Module 1

Imports physics citation graph 
"""

# general imports
import urllib2
from matplotlib import pyplot
import random
# Set timeout for CodeSkulptor if necessary
#import codeskulptor
#codeskulptor.set_timeout(20)


###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

class DPATrial:
    """
    Simple class to encapsulate optimized trials for DPA algorithm
    
    Maintains a list of node numbers with multiple instances of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a DPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_node trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors 

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
    
def make_random_digraph(num_nodes, p):
    """
    Creates a complete undirected graph
    """
    if num_nodes < 1:
        return {}
    
    complete_graph = {}
    for idx in range(num_nodes):
        complete_graph[idx] = set([])
        for each_idx in range(num_nodes):
            rand_num = random.random()
            if idx != each_idx and rand_num < p:
                complete_graph[idx].add(each_idx)
                
    return complete_graph

def dfa(total_nodes, initial_nodes):
    vertices = set(range(initial_nodes))
    graph = make_complete_graph(initial_nodes)
    for idx in range(initial_nodes, total_nodes):
        in_degrees = compute_in_degrees(graph)
        in_degree_sum = sum(in_degrees.values())
        vertices_prime = set([])
        for node in vertices:
            p = float(in_degrees[node] + 1)/(in_degree_sum + len(vertices))
            rand_num = random.random()
            if rand_num < p:
                vertices_prime.add(node)
        vertices.add(idx)
        graph[idx] = vertices_prime
    return graph  

def dfa2(total_nodes, initial_nodes):
    vertices = set(range(initial_nodes))
    graph = make_complete_graph(initial_nodes)
    dpa_trial = DPATrial(initial_nodes)
    for idx in range(initial_nodes, total_nodes):
        #in_degrees = compute_in_degrees(graph)
        #in_degree_sum = sum(in_degrees.values())
        #vertices_prime = set([])
        #num_vertices = len(vertices)
        #dpa_trial = DPATrial(idx + 1)
        #dpa_trial = DPATrial(initial_nodes)
        #vertices_prime = dpa_trial.run_trial(idx + 1)
        vertices_prime = dpa_trial.run_trial(initial_nodes)
        #for node in vertices:
        #    p = float(in_degrees[node] + 1)/(in_degree_sum + len(vertices))
        #    rand_num = random.random()
        #    if rand_num < p:
        #        vertices_prime.add(node)
        vertices.add(idx)
        graph[idx] = vertices_prime
    return graph     
    
citation_graph = load_graph(CITATION_URL)

dist = in_degree_distribution(citation_graph)
#print dist

"""
x = dist.keys()
y = dist.values()
sum_y = sum(y)
y_normal = [float(val)/sum_y for val in y]

for i in range(len(x)):
    print str(x[i]) + ", " + str(y[i]) 

pyplot.figure(1)
pyplot.subplot(211)
#pyplot.plot(x[0:100], y[0:100])
pyplot.plot(x, y_normal)
pyplot.xscale('log')
pyplot.yscale('log')
pyplot.xlabel('log of in degrees')
pyplot.ylabel('log of frequency')
pyplot.title('In degree distribution')
pyplot.show()

EX_GRAPH0 = {0: set([1,2]), 1: set([]), 2: set([])}
EX_GRAPH1 = {0: set([1,4,5]), 1: set([2,6]), 2: set([3]), 3: set([0]), 4: set([1]), 5: set([2]), 6: set([])}
EX_GRAPH2 = {0: set([1,4,5]), 1: set([2,6]), 2: set([3, 7]), 3: set([7]), 4: set([1]), 5: set([2]), 6: set([]), 7: set([3]), 8: set([1,2]), 9: set([0,3,4,5,6,7])}
"""

"""
#problem 2
random_digraph = make_random_digraph(500, 0.2)
dist = in_degree_distribution(random_digraph)

x = dist.keys()
y = dist.values()
pyplot.figure(1)
pyplot.subplot(211)
pyplot.plot(x, y)
pyplot.xlabel('in degrees')
pyplot.ylabel('frequency')
pyplot.title('In degree distribution')
pyplot.show()
"""

#problem 3
#cg = make_complete_graph(30)
#print compute_in_degrees(cg)

#print "abc"


n = len(citation_graph)
#n = 27770
print "n =", n
product = 0
for key, value in dist.iteritems():
    product += key * value 
#print "product = ", product
m = product / n
print "m = ", m
#dfa_graph = dfa(n, m)
#print dfa_graph

# problem 4
#n = len(citation_graph)
#n = 27770
#print "n =", n
#product = 0
#for key, value in dist.iteritems():
#    product += key * value 
#print "product = ", product
#m = product / n
#print "m = ", m
#m=24
dfa_graph = dfa2(n, m)
print dfa_graph

dpa_dist = in_degree_distribution(dfa_graph)
print dpa_dist

x = dpa_dist.keys()
y = dpa_dist.values()
sum_y = sum(y)
y_normal = [float(val)/sum_y for val in y]

#for i in range(len(x)):
#    print str(x[i]) + ", " + str(y[i]) 

pyplot.figure(1)
pyplot.subplot(211)
#pyplot.plot(x[0:100], y[0:100])
pyplot.plot(x, y_normal, 'ro')
pyplot.axis([0,20,0,0.6])
#pyplot.xscale('log')
#pyplot.yscale('log')
pyplot.xlabel('log of in degrees')
pyplot.ylabel('log of frequency')
pyplot.title('In degree distribution')
pyplot.show()
