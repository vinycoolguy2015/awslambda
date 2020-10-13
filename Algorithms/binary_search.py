def binary_search(data,item):
    start=0
    end=len(data)-1
    found=False
    while start <= end and not found:
        mid=(start+end)/2
        pivot=data[mid]
        if item==pivot:
            found=True
            break
        elif item>pivot:
            start=mid+1
        elif item < pivot:
            end=mid-1
    return found
    
            
            
list=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
item=20
if binary_search(list,item):
    print "Item found"
else:
    print "Item not found"
    
import random
my_randoms = random.sample(xrange(10000000), 1000000)
import time
start_time = time.time()
my_randoms.sort()
if binary_search(my_randoms,my_randoms[100]):
    print "Item found"
else:
    print "Item not found"
print("--- %s seconds ---" % (time.time() - start_time))

    

