def insertion_sort(data):
    for i in range(1,len(data)):
        for j in range(i,0,-1):
            if data[j]<data[j-1]:
                data[j-1],data[j]=data[j],data[j-1]
        print data
    print data
                
            
            
a=[10,9,8,1,3,4,5,7,6,0,2]
#a=[100,99,1,2,3,67,78,67,34,190,1,2]
print ("Initial data is: ",a)
insertion_sort(a)

