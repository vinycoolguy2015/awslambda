class Node(object):
    
    def __init__(self,data):
        self.data=data
        self.nextNode=None
        
class LinkedList(object):
    
    def __init__(self):
        self.head=None
        self.size=0;
    
    def insertStart(self,data):
        self.size=self.size+1
        newNode=Node(data)
        if not self.head:
            self.head=newNode
        else:
            newNode.nextNode=self.head
            self.head=newNode
            
    #0(1) complexity
    def size(self):
        return self.size
        
    #If we don't store self.size then we can use this method but it'll have 0(n) complexity
    def size2(self):
        actualNode=self.head
        size=0
        while actualNode is not None:
            size+=1
            actualNode=actualNode.nextNode
        return size
    
    #O(n) complexity
    def insertEnd(self,data):
        self.size+=1
        newNode=Node(data)
        actualNode=self.head
        while actualNode.nextNode is not None:
            actualNode=actualNode.NextNode
        actualNode.nextNode=newNode
        
    #O(n) complexity
    def traverse(self):
        actualNode=self.head
        while actualNode is not None:
            print actualNode.data
            actualNode=actualNode.nextNode
            
            
    #O(n) complexity
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
    mylist=LinkedList()
    print mylist.size
    mylist.insertStart(10)
    print mylist.size
    mylist.insertEnd(20)
    print mylist.size
    mylist.traverse()
    mylist.remove(30)
    mylist.insertStart(15)
    print mylist.size
    mylist.traverse()
    mylist.remove(10)
    mylist.remove(20)
    mylist.traverse()
    mylist.remove(15)
    print mylist.size
    
    
    
    
                
        
        
            
        
        
    