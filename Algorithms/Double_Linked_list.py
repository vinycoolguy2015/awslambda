class Node(object):
    
    def __init__(self,data):
        self.data=data
        self.nextNode=None
        self.previousNode=None
        
class DoubleLinkedList(object):
    
    
    def __init__(self):
        self.head=None
        self.size=0;
    
    
    def insertStart(self,data):
        self.size=self.size+1
        newNode=Node(data)
        if not self.head:
            self.head=newNode
        else:
            self.head.previousNode=newNode
            newNode.nextNode=self.head
            self.head=newNode
            
    
    def size(self):
        return self.size
        
    
    def insertEnd(self,data):
        self.size+=1
        newNode=Node(data)
        actualNode=self.head
        while actualNode.nextNode is not None:
            actualNode=actualNode.NextNode
        actualNode.nextNode=newNode
        newNode.previousNode=actualNode
        
    
    def traverse_forward(self):
        actualNode=self.head
        while actualNode is not None:
            print actualNode.data
            actualNode=actualNode.nextNode
    
    
    def traverse_backward(self):
        actualNode=self.head
        while actualNode.nextNode is not None:
            actualNode=actualNode.nextNode
        print actualNode.data
        while actualNode.previousNode is not None:
            print actualNode.previousNode.data
            actualNode=actualNode.previousNode
       
    
    def remove(self,data):
        if self.head is None:
            return
        else:
            currentNode=self.head
            previousNode=None
            while currentNode is not None:
                if currentNode.data==data:
                    self.size-=1
                    if self.head==currentNode:
                        self.head=currentNode.nextNode
                    else:
                        previousNode.nextNode=currentNode.nextNode
                    break
                else:
                    previousNode=currentNode
                    currentNode=currentNode.nextNode
                    

if __name__ == "__main__":
    mylist=DoubleLinkedList()
    mylist.insertStart(10)
    mylist.insertEnd(20)
    mylist.insertStart(15)
    mylist.traverse_forward()
    mylist.traverse_backward()
    
    
    
    
                
        
        
            
        
        
    