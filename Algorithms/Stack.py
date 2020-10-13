class Stack(object):
    
    def __init__(self):
        self.stack=[]
        
    def isEmpty(self):
        return self.stack==[]
    
    def push(self,data):
        self.stack.append(data)
        
    def pop(self):
        data=self.stack[-1]
        del self.stack[-1]
        return data
    
    def peek(self):
        return self.stack[-1]
    
    def size(self):
        return len(self.stack)
    
    def data(self):
        for i in range(self.size()-1,-1,-1):
            yield self.stack[i]
        
        
    
stack=Stack()
stack.push(10)
stack.push(20)
stack.push(30)
stack.push(40)
stack.push(50)
print stack.pop()
print stack.peek()
print stack.size()
if not stack.isEmpty():
    data=stack.data()
    for item in data:
        print item
else:
    print "Stack is empty"

        
    
        
        