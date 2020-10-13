
def quicksort(data,low,high):
    if low >= high:
        return 
    pivot=partition(data,low,high)
    quicksort(data,low,pivot-1)
    quicksort(data,pivot+1,high)
    
def partition(data,low,high):
    pivotIndex=(low+high)/2
    data[pivotIndex],data[high]=data[high],data[pivotIndex]
    i=low
    for j in range(low,high):
        if data[j]<=data[high]:
            data[i],data[j]=data[j],data[i]
            i+=1
    data[i],data[high]=data[high],data[i]
    return i
        
    
data=[10,8,1,2,3,9,7,4,-5,6,0]
quicksort(data,0,len(data)-1)
print data

import random
my_randoms = random.sample(xrange(10000000), 1000000)
import time
start_time = time.time()
quicksort(my_randoms,0,len(my_randoms)-1)
print("--- %s seconds ---" % (time.time() - start_time))


###############################Sort in descending order########################################################

def quicksort(data,low,high):
    if low >= high:
        return 
    pivot=partition(data,low,high)
    quicksort(data,low,pivot-1)
    quicksort(data,pivot+1,high)
    
def partition(data,low,high):
    pivotIndex=(low+high)/2
    data[pivotIndex],data[high]=data[high],data[pivotIndex]
    i=low
    for j in range(low,high):
        if data[j]>data[high]:
            data[i],data[j]=data[j],data[i]
            i+=1
    data[i],data[high]=data[high],data[i]
    return i
data=[10,8,1,2,3,9,7,4,-5,6,0]
quicksort(data,0,len(data)-1)
print data
