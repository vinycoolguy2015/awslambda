class Node(object):
    
    def __init__(self,data):
        self.data=data
        self.leftChild=None
        self.rightChild=None

class binarySearchTree(object):
    
    def __init__(self):
        self.root=None
        
    def insert(self,data):
        if self.root is None:
            self.root=Node(data)
        else:
            self.insertNode(self.root,data)
    
    def insertNode(self,node,data):
        if data < node.data:
            if node.leftChild:
                self.insertNode(node.leftChild,data)
            else:
                node.leftChild=Node(data)
        if data > node.data:
            if node.rightChild:
                self.insertNode(node.rightChild,data)
            else:
                node.rightChild=Node(data)
                
                
    def traverse(self):
        if self.root:
            self.traverseInorder(self.root)
            
            
    def traverseInorder(self,node):
        if node.leftChild:
            self.traverseInorder(node.leftChild)
        print node.data
        if node.rightChild:
            self.traverseInorder(node.rightChild)
            
            
    def traverse2(self):
        if self.root:
            self.traversePostorder(self.root)
            
            
    def traversePostorder(self,node):
        if node.leftChild:
            self.traversePostorder(node.leftChild)
        if node.rightChild:
            self.traversePostorder(node.rightChild)
        print node.data
        
            
    def traverse3(self):
        if self.root:
            self.traversePreorder(self.root)
            
            
    def traversePreorder(self,node):
        print node.data
        if node.leftChild:
            self.traversePreorder(node.leftChild)
        if node.rightChild:
            self.traversePreorder(node.rightChild)
            
    def getMaxValue(self):
        if self.root:
            return self.maximum(self.root)
    
    def maximum(self,node):
        if node.rightChild:
            return self.maximum(node.rightChild)
        return node.data
    
    def getMinValue(self):
        if self.root:
            return self.minimum(self.root)
    
    def minimum(self,node):
        if node.leftChild:
            return self.minimum(node.leftChild)
        return node.data
    
    
    
            
        
        
    
if __name__=="__main__":
    bst=binarySearchTree()
    print "Adding some data into this tree"
    bst.insert(32)
    bst.insert(10)
    bst.insert(1)
    bst.insert(55)
    bst.insert(19)
    bst.insert(79)
    bst.insert(16)
    bst.insert(23)
    print("Time to traverse the tree \nInorder traversal")
    bst.traverse()
    print("--------------------------------------")
    print("Post order traversal")
    bst.traverse2()
    print("--------------------------------------")
    print("Pre order traversal")
    bst.traverse3()
    print("--------------------------------------")
    print "Maximum",bst.getMaxValue()
    print "Minimum",bst.getMinValue()

    
        
    