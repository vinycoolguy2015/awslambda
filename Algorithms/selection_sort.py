def selection_sort(data):
    for i in range(len(data)-1):
        minimum=data[i]
        index=i
        for j in range(i+1,len(data)):
            if data[j]<minimum:
                index=j
                minimum=data[j]
        data[i],data[index]=data[index],data[i]
    return data
       
    
            

a=[10,9,8,1,3,4,5,7,6,0,2]
#a=[100,99,1,2,3,67,78,67,34,190,1,2]
print ("Initial data is: ",a)
print selection_sort(a)












