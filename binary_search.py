# implementation of binary search algo

# naive search : scan entire list  and ask if it equals to the target
# if yes then return the index
# if no then return -1

import random
import time

def naive_search (list, target):
    for i in range(len(list)):
        if list[i] == target:
            return i
    return -1

# binary search uses divide and conquer
# The list must be SORTED before using binary search
def binary_search(list, target, low = None, high = None):
    if low == None:
        low = 0
    if high == None:
        high = len(list) - 1
    if high < low: # target not found
        return -1
    
    midpoint = ( low + high ) // 2
    
    if list[midpoint] == target:
        return midpoint
    elif list[midpoint] >  target:
        return binary_search(list,target,low, midpoint-1)
    else:
        return binary_search(list, target, midpoint+1, high)

if __name__ == '__main__':
#    l = [0,1,2,3,4,5,6,7,8,9,10,11,12]
#    target = 10
#    print(naive_search(l,target))
#    print(binary_search(l,target))

#    time analysis

    length = 10000
    # build a sorted list of length 10000
    sorted_list = set()
    while len(sorted_list) < length:
        sorted_list.add(random.randint(-3*length, 3*length))

    sorted_list = sorted(list(sorted_list))

    start = time.time()
    for target in sorted_list:
        naive_search(sorted_list, target)
    end = time.time()
    print("Naive Search time: ", (end-start)/length, "seconds")


    start = time.time()
    for target in sorted_list:
        binary_search(sorted_list, target)
    end = time.time()
    print("Binary Search time: ", (end-start)/length, "seconds")
