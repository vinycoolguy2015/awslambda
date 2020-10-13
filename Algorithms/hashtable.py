class HashTable(object):
    
    def __init__(self):
        self.size=10;
        self.keys=[None]*self.size
        self.values=[None]*self.size
        
        
    def hashFunction(self,key):
        sum=0
        for pos in range(len(key)):
            sum+=ord(key[pos])
        return sum%self.size
    
    def put(self,key,data):
        index=self.hashFunction(key)
        while self.keys[index] is not None:
            if self.keys[index]==key:
                self.values[index]=data
                return
            index=(index+1)%self.size
        self.keys[index]=key
        self.values[index]=data
        
    def get(self,key):
        index=self.hashFunction(key)
        while self.keys[index] is not None:
            if self.keys[index]==key:
                return self.values[index]
            index=(index+1)%self.size
        return None
        
if __name__=="__main__":
    table=HashTable()
    table.put('10',"Vinayak")
    table.put('11',"Viny")
    table.put('12',"Pandey")
    table.put('13',"Ashish")
    table.put('14',"Ashish")
    table.put('14',"Ashish Pandey")
    print table.get('10')
    print table.get('11')
    print table.get('12')
    print table.get('13')
    print table.get('14')
    
            
        