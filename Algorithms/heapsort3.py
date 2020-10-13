def createHeap(data,index):
    parentIndex=int((index-1)/2)
    while parentIndex >=0 and data[parentIndex]<data[index]:
        data[index],data[parentIndex]=data[parentIndex],data[index]
        index=parentIndex
        parentIndex=int((index-1)/2)

def sort(data):
    for i in range(len(data)-1):
        counter=len(data)-1-i
        data[0],data[counter]=data[counter],data[0]
        index=0
        leftIndex=(2*index)+1 
        rightIndex=(2*index)+2
        leftIndex=leftIndex if leftIndex <counter else index
        rightIndex=rightIndex if rightIndex <counter else index
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
            leftIndex=(2*index)+1 
            rightIndex=(2*index)+2
            leftIndex=leftIndex if leftIndex <counter else index
            rightIndex=rightIndex if rightIndex <counter else index
    return data


def heapSort(data):
    for i in range(len(data)):
        createHeap(data,i)
    sort(data)
    return data
    
        
import random
import time
my_randoms = random.sample(xrange(100000), 100000)
sort_time = time.time()
data=heapSort(my_randoms)
print("--- %s seconds ---" % (time.time() - sort_time))
        

    
    