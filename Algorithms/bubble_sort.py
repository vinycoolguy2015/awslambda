def bubble_sort(data):
    for i in range(len(data)-1):
        for j in range(len(data)-i-1):
            if data[j]>data[j+1]:
                data[j],data[j+1]=data[j+1],data[j]
            print data
        print("----------------------------")
    
            

a=[10,9,8,1,3,4,5,7,6,0,2]
print ("Initial data is: ",a)
bubble_sort(a)


