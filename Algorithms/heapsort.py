def createHeap(data,index):
    parentIndex=int((index-1)/2)
    while parentIndex >=0 and data[parentIndex]<data[index]:
        data[index],data[parentIndex]=data[parentIndex],data[index]
        index=parentIndex
        parentIndex=int((index-1)/2)
   
    
        
def sort(data):
    while len(data)>1:
        data[0],data[-1]=data[-1],data[0]
        print data[-1]
        del data[-1]
        items=len(data)
        index=0
        leftIndex=(index*2)+1
        rightIndex=(index*2)+2
        if leftIndex >= len(data):
            leftIndex=index
        if rightIndex >= len(data):
            rightIndex=index
        while data[index]<data[leftIndex] or data[index]<data[rightIndex]:
            if data[index]<data[leftIndex]:
                if data[leftIndex]< data[rightIndex]:
                    data[index],data[rightIndex]=data[rightIndex],data[index]
                    index=rightIndex
                else:
                    data[index],data[leftIndex]=data[leftIndex],data[index]
                    index=leftIndex
            elif data[index]<data[rightIndex]:
                data[index],data[rightIndex]=data[rightIndex],data[index]
                index=rightIndex
            leftIndex=(index*2)+1
            rightIndex=(index*2)+2
            items=len(data)
            if leftIndex >= len(data):
                leftIndex=index
            if rightIndex >= len(data):
                rightIndex=index
       
    
   
    
def heapSort(data):
    import time
    heap_time = time.time()
    for i in range(len(data)):
        createHeap(data,i)
    print("--- %s seconds ---" % (time.time() - heap_time))
    
    sort_time = time.time()
    sort(data)
    print("--- %s seconds ---" % (time.time() - sort_time))
    
        

import random
my_randoms = random.sample(xrange(100000), 100000)
heapSort(my_randoms)





                              




                          
        
                                


        

        