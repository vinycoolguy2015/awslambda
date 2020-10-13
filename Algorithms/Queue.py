class Queue(object):
    
    def __init__(self):
        self.queue=[]
        
    def isEmpty(self):
        return self.queue==[]
    
    def enQueue(self,data):
        self.queue.append(data)
        
    def deQueue(self):
        data=self.queue[0]
        del self.queue[0]
        return data
    
    def peek(self):
        return self.queue[0]
    
    def size(self):
        return len(self.queue)
    
    def data(self):
        for item in self.queue:
            yield item
        
        
    
queue=Queue()
queue.enQueue(10)
queue.enQueue(20)
queue.enQueue(30)
queue.enQueue(40)
queue.enQueue(50)
print queue.deQueue()
print queue.peek()
print queue.size()
if not queue.isEmpty():
    data=queue.data()
    for item in data:
        print item
else:
    print "Queue is empty"

        
    
        
        