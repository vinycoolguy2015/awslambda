def flatten(aList):
    result=[]
    for items in aList:
        if type(items) ==list:
            for item in items:
                result.append(item)
        else:
            result.append(items)
    return result
    
def radix_sort(random_list):
    div=1
    modulo=10
    counter=len(str(max(random_list)))
    for i in range(counter):
        new_list = [[], [], [], [], [], [], [], [], [], []]
        for item in random_list:
            value= item%modulo
            digit=value/div
            new_list[digit].append(item)
        div=div*10
        modulo=modulo*10
        random_list=flatten(new_list)
    return random_list

import random
my_randoms = random.sample(xrange(10000000), 1000000)
import time
start_time = time.time()
radix_sort(my_randoms)
print("--- %s seconds ---" % (time.time() - start_time))


