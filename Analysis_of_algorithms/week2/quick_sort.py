# -*- coding: utf-8 -*-
"""
Created on Sun Nov 09 23:00:10 2014

@author: stree_001
"""
import fileinput
counter = 0

def get_pivot1(arr):
    return arr[0]
    
def get_pivot2(arr):
    return arr[-1]
    
def get_pivot3(arr):
    return sorted([arr[0], arr[len(arr)/2], arr[-1]])[1]

def quick_sort(arr, fp):
    global counter
    comparisons = (len(arr) - 1)
    counter += (len(arr) - 1)
    if len(arr) < 2:
        return arr, 0
    
    pivot = fp(arr)    
    less = []
    equal = []
    greater = []
    for i in range(len(arr)):
        if arr[i] < pivot:
            less.append(arr[i])
        elif arr[i] == pivot:
            equal.append(arr[i])
        else:
            greater.append(arr[i])
    
    sorted_less, less_comparisons = quick_sort(less, fp)
    sorted_greater, greater_comparisons = quick_sort(greater, fp)         
    #return quick_sort(less)[0] + equal + quick_sort(greater)[0], comparisons + quick_sort
    return sorted_less + equal + sorted_greater, comparisons + less_comparisons + greater_comparisons
    
        
def main():
    global counter
    arr = [8, 2, 4, 5, 7, 1]
    output = quick_sort(arr, get_pivot1)
    print output
    
    #arr = []
    with open('QuickSort.txt') as f:
        arr = [int(line.rstrip()) for line in f.readlines()]
        
    counter = 0
    output = quick_sort(arr, get_pivot1)
    #print arr
    print output[1], counter
    counter = 0
    output = quick_sort(arr, get_pivot2)
    print output[1], counter
    counter = 0
    output = quick_sort(arr, get_pivot3)
    print output[1], counter
    
main()