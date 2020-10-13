def counter_sort(data):
    maximum=max(data)
    minimum=min(data)
    counter_array=[0] * ((maximum-minimum)+1)
    for item in data:
        counter_array[item-minimum]+=1
    z=0
    length=len(counter_array)
    for i in range(length):
        while counter_array[i]>0:
            data[z]=minimum+i
            counter_array[i]-=1
            z+=1
    return data
print counter_sort([10,9,8,7,6,5,4,3,2,1,0,10,9,8,7,6,5,4,3,2,1,0,10,9,8,7,6,5,4,3,2,1,0,10,9,8,7,6,5,4,3,2,1,0])

import random
my_randoms = random.sample(xrange(10000000), 1000000)
import time
start_time = time.time()
counter_sort(my_randoms)
print("--- %s seconds ---" % (time.time() - start_time))
