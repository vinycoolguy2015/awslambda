class Heap(object):
    
    HEAP_SIZE=20
    
    def __init__(self):
        self.size=10
        self.heap=[None]*Heap.HEAP_SIZE
        self.currentIndex=-1
        
    def insert(self,item):
        self.currentIndex+=1
        if self.isFull():
            print ("Heap is full..")
            return
        self.heap[self.currentIndex]=item
        self.fixUp(self.currentIndex)
        
        
    def isFull(self):
        if self.currentIndex==Heap.HEAP_SIZE:
            return True
        
    def fixUp(self,index):
        parentIndex=int((index-1)/2)
        while parentIndex >=0 and self.heap[parentIndex]<self.heap[index]:
            self.heap[index],self.heap[parentIndex]=self.heap[parentIndex],self.heap[index]
            index=parentIndex
            parentIndex=int((index-1)/2)
            
           
    
    def returnHeap(self):
        for item in self.heap:
            if item is not None:
                print item
            
if __name__=="__main__":
    heap=Heap()
    heap.insert(10)
    heap.insert(20)
    heap.insert(30)
    heap.insert(340)
    heap.insert(50)
    heap.insert(1)
    heap.insert(2)
    heap.insert(3)
    heap.insert(4)
    heap.insert(500)
    heap.insert(5000)
    heap.insert(60)
    heap.returnHeap()
    
        