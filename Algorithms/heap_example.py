import heapq
 
li = [5, 7, 9, 1, 3]
heapq.heapify(li)
 
print ("The created heap is : ")
print (list(li))
 
heapq.heappush(li,4)
 
print ("The modified heap after push is : ")
print (list(li))
 
print ("The popped and smallest element is : ")
print (heapq.heappop(li))


#Finding n largest and smallest in a list

import heapq
li1 = [6, 7, 9, 4, 3, 5, 8, 10, 1]
heapq.heapify(li1)
 
print("The 3 largest numbers in list are : ")
print(heapq.nlargest(3, li1))
 
print("The 3 smallest numbers in list are : ")
print(heapq.nsmallest(3, li1))