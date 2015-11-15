#!/usr/bin/python

#import project3
#import alg_cluster
import csv
import random
import math

class Cluster:
    """
    Class for creating and merging clusters of counties
    """
    
    def __init__(self, fips_codes, horiz_pos, vert_pos, population, risk):
        """
        Create a cluster based the models a set of counties' data
        """
        self._fips_codes = fips_codes
        self._horiz_center = horiz_pos
        self._vert_center = vert_pos
        self._total_population = population
        self._averaged_risk = risk
        
        
    def __repr__(self):
        """
        String representation assuming the module is "alg_cluster".
        """
        rep = "alg_cluster.Cluster("
        rep += str(self._fips_codes) + ", "
        rep += str(self._horiz_center) + ", "
        rep += str(self._vert_center) + ", "
        rep += str(self._total_population) + ", "
        rep += str(self._averaged_risk) + ")"
        return rep


    def fips_codes(self):
        """
        Get the cluster's set of FIPS codes
        """
        return self._fips_codes
    
    def horiz_center(self):
        """
        Get the averged horizontal center of cluster
        """
        return self._horiz_center
    
    def vert_center(self):
        """
        Get the averaged vertical center of the cluster
        """
        return self._vert_center
    
    def total_population(self):
        """
        Get the total population for the cluster
        """
        return self._total_population
    
    def averaged_risk(self):
        """
        Get the averaged risk for the cluster
        """
        return self._averaged_risk
   
        
    def copy(self):
        """
        Return a copy of a cluster
        """
        copy_cluster = Cluster(set(self._fips_codes), self._horiz_center, self._vert_center,
                               self._total_population, self._averaged_risk)
        return copy_cluster


    def distance(self, other_cluster):
        """
        Compute the Euclidean distance between two clusters
        """
        vert_dist = self._vert_center - other_cluster.vert_center()
        horiz_dist = self._horiz_center - other_cluster.horiz_center()
        return math.sqrt(vert_dist ** 2 + horiz_dist ** 2)
        
    def merge_clusters(self, other_cluster):
        """
        Merge one cluster into another
        The merge uses the relatively populations of each
        cluster in computing a new center and risk
        
        Note that this method mutates self
        """
        if len(other_cluster.fips_codes()) == 0:
            return self
        else:
            self._fips_codes.update(set(other_cluster.fips_codes()))
 
            # compute weights for averaging
            self_weight = float(self._total_population)                        
            other_weight = float(other_cluster.total_population())
            self._total_population = self._total_population + other_cluster.total_population()
            self_weight /= self._total_population
            other_weight /= self._total_population
                    
            # update center and risk using weights
            self._vert_center = self_weight * self._vert_center + other_weight * other_cluster.vert_center()
            self._horiz_center = self_weight * self._horiz_center + other_weight * other_cluster.horiz_center()
            self._averaged_risk = self_weight * self._averaged_risk + other_weight * other_cluster.averaged_risk()
            return self

    def cluster_error(self, data_table):
        """
        Input: data_table is the original table of cancer data used in creating the cluster.
        
        Output: The error as the sum of the square of the distance from each county
        in the cluster to the cluster center (weighted by its population)
        """
        # Build hash table to accelerate error computation
        fips_to_line = {}
        for line_idx in range(len(data_table)):
            line = data_table[line_idx]
            fips_to_line[line[0]] = line_idx
        
        # compute error as weighted squared distance from counties to cluster center
        total_error = 0
        counties = self.fips_codes()
        for county in counties:
            line = data_table[fips_to_line[county]]
            singleton_cluster = Cluster(set([line[0]]), line[1], line[2], line[3], line[4])
            singleton_distance = self.distance(singleton_cluster)
            total_error += (singleton_distance ** 2) * singleton_cluster.total_population()
        return total_error

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function to compute Euclidean distance between two clusters
    in cluster_list with indices idx1 and idx2
    
    Returns tuple (dist, idx1, idx2) with idx1 < idx2 where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))

def slow_closest_pairs(cluster_list):
    """
    Compute the set of closest pairs of cluster in list of clusters
    using O(n^2) all pairs algorithm
    
    Returns the set of all tuples of the form (dist, idx1, idx2) 
    where the cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.   
    
    """
    (best_dist,p_u,p_v) = (float("inf"), -1, -1)
    output = set([])
    for p_u in range(len(cluster_list)):
        for p_v in range(len(cluster_list)):
            if p_v == p_u:
                continue
            pair_dist = pair_distance(cluster_list, p_v, p_u)
            if pair_dist[0] < best_dist:
                best_dist = pair_dist[0]
                output = set([pair_dist])
            elif pair_dist[0] == best_dist:
                best_dist = pair_dist[0]
                output.add(pair_dist)
    
    #print "output", output
    return output    


def fast_closest_pair(cluster_list):
    """
    Compute a closest pair of clusters in cluster_list
    using O(n log(n)) divide and conquer algorithm
    
    Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
    cluster_list[idx1] and cluster_list[idx2]
    have the smallest distance dist of any pair of clusters
    """
        
    def fast_helper(cluster_list, horiz_order, vert_order):
        """
        Divide and conquer method for computing distance between closest pair of points
        Running time is O(n * log(n))
        
        horiz_order and vert_order are lists of indices for clusters
        ordered horizontally and vertically
        
        Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
        cluster_list[idx1] and cluster_list[idx2]
        have the smallest distance dist of any pair of clusters
    
        """
        
        # base case
        n_h = len(horiz_order)
        if n_h <= 3:
            #Q_var = []
            #for idx in range(0,n):
            #    Q_var.append(cluster_list[horiz_order[idx]])
                
            q_var = [cluster_list[horiz_order[idx]] for idx in range(0,n_h)]
            #print "Q", Q_var
            #print slow_closest_pairs(Q_var)
            #print "pd base", tuple(slow_closest_pairs(Q_var))[0]
            pair_tuple = tuple(slow_closest_pairs(q_var))[0]
            #dist = pair_tuple[0]
            #idx1 = horiz_order[pair_tuple[1]]
            #idx2 = horiz_order[pair_tuple[2]]
            #ret = (dist, idx1, idx2)
            #print "ret", ret
            #return ret
            return (pair_tuple[0], horiz_order[pair_tuple[1]], horiz_order[pair_tuple[2]])
            #base_
            
            #return tuple(slow_closest_pairs(Q_var))[0]
        
        # divide
        half = int(math.ceil(n_h/2.0))
        #print m
        mid = 0.5 * (cluster_list[horiz_order[half-1]].horiz_center() + cluster_list[horiz_order[half]].horiz_center())
        horiz_order_l = horiz_order[0:half]
        horiz_order_r = horiz_order[half:]
        set_h_l = set(horiz_order_l)
        set_h_r = set(horiz_order_r)
        vert_order_l = []
        vert_order_r = []
        for idx in vert_order:
            if idx in set_h_l:
                vert_order_l.append(idx)
            if idx in set_h_r:
                vert_order_r.append(idx)
                
        (d_l, i_l, j_l) = fast_helper(cluster_list, horiz_order_l, vert_order_l)
        (d_r, i_r, j_r) = fast_helper(cluster_list, horiz_order_r, vert_order_r)
        (d_min,i_var,j_var) = min((d_l, i_l, j_l), (d_r, i_r, j_r))
                
        # conquer
        s_var = []
        for v_idx in vert_order:
            if abs(cluster_list[v_idx].horiz_center() - mid) < d_min:
                s_var.append(v_idx)
                
        #print "S_var", S_var
            
        k_var = len(s_var)
        for u_idx in range(k_var - 1):
            v_var = u_idx + 1
            end = min(u_idx + 3, k_var - 1)
            for idx in range(v_var, end+1):
                #pair_dist = pair_distance(S_var, u_idx, v_var)
                pair_dist = pair_distance(cluster_list, s_var[u_idx], s_var[v_var])
                #print "pairpair_dist                
                #(d_min, i_var, j_var) = min((d_min, i_var, j_var), (pair_dist, S_var[u_idx], S_var[v_var]))
                #print "pd", pair_dist
                (d_min, i_var, j_var) = min((d_min, i_var, j_var), pair_dist)
             
        return (d_min, i_var, j_var)
            
    # compute list of indices for the clusters ordered in the horizontal direction
    hcoord_and_index = [(cluster_list[idx].horiz_center(), idx) 
                        for idx in range(len(cluster_list))]    
    hcoord_and_index.sort()
    horiz_order = [hcoord_and_index[idx][1] for idx in range(len(hcoord_and_index))]
     
    # compute list of indices for the clusters ordered in vertical direction
    vcoord_and_index = [(cluster_list[idx].vert_center(), idx) 
                        for idx in range(len(cluster_list))]    
    vcoord_and_index.sort()
    vert_order = [vcoord_and_index[idx][1] for idx in range(len(vcoord_and_index))]

    # compute answer recursively
    answer = fast_helper(cluster_list, horiz_order, vert_order)
    return (answer[0], min(answer[1:]), max(answer[1:]))


# Assets
#DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
#MAP_URL = DIRECTORY + "data_clustering/USA_Counties.png"
#DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"

for run_counter in range(5000):
    random.seed(run_counter)
    probability = random.randrange(10,100) / 100.0
    print "Run: ", run_counter, "p:", probability
    csv_file = open('unifiedCancerData_111.csv', 'r')
    reader = csv.reader(csv_file)
    cluster_list = []
    for row in reader:
        if random.random() > probability:
            continue
        new_cluster = Cluster(
                int(row[0]),
                float(row[1]), float(row[2]),
                int(row[3]), float(row[4]))
        cluster_list.append(new_cluster)

    slow_res = slow_closest_pairs(cluster_list)
    fast_res = fast_closest_pair(cluster_list)

    print cluster_list
    print "slow_res", slow_res
    print "fast_res", fast_res

    assert fast_res in slow_res