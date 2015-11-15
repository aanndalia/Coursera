# -*- coding: utf-8 -*-
"""
Created on Wed Oct 22 22:56:40 2014

@author: stree_001
"""

def merge_count_inversions(arr1, arr2):
    i1 = 0
    i2 = 0
    m_arr = []
    count = 0
    while i1 < len(arr1) and i2 < len(arr2):
        if arr1[i1] < arr2[i2]:
            m_arr.append(arr1[i1])
            i1 += 1
        elif arr1[i1] > arr2[i2]:
            m_arr.append(arr2[i2])
            i2 += 1
            # count remaining numbers in left array as inversions
            count += (len(arr1) - i1)
        else:
            m_arr.append(arr1[i1])
            m_arr.append(arr2[i2])
            i1 += 1
            i2 += 1
    
    while i1 < len(arr1):
        m_arr.append(arr1[i1])
        i1 += 1
        
    while i2 < len(arr2):
        m_arr.append(arr2[i2])
        i2 += 1
        #count += 1
    
    return m_arr, count

def count_inversion3(in_arr):
    if len(in_arr) < 2:
        return in_arr, 0
    
    arr = in_arr

    m_left, count_left = count_inversion3(arr[0:(len(arr)/2)])
    m_right, count_right = count_inversion3(arr[(len(arr)/2):])
    merged, count_merged = merge_count_inversions(m_left, m_right)
    return merged, count_left + count_right + count_merged
    
def main():
    file_arr = []
    with open("IntegerArray.txt") as f:
        for line in f:
            file_arr.append(int(line))
    
    print count_inversion3(file_arr)
    
main()