def longest_run(L):
    """
    Assumes L is a list of integers containing at least 2 elements.
    Finds the longest run of numbers in L, where the longest run can
    either be monotonically increasing or monotonically decreasing. 
    In case of a tie for the longest run, choose the longest run 
    that occurs first.
    Does not modify the list.
    Returns the sum of the longest run. 
    """
    # Your code here
    max_count=0
    min_count=0
    max_index=0
    min_index=0
    max_sum=0
    min_sum=0
   
    for i in range (len(L)-1):
        count_max=0
        count_min=0
        sum_max=L[i]
        sum_min=L[i]
        
        for j in range(i,len(L)-1):
            if L[j+1]<L[j]:
                break
            else:
                count_max+=1
                sum_max+=L[j+1]
        if count_max > max_count:
            max_count=count_max
            max_index=i
            max_sum=sum_max
        for k in range(i,len(L)-1):
            if L[k+1]>L[k]:
                break
            else:
                count_min+=1
                sum_min+=L[k+1]
        if count_min > min_count:
            min_count=count_min
            min_index=i
            min_sum=sum_min
    if max_count > min_count:
        return max_sum
    elif max_count < min_count:
        return min_sum
    elif max_count==min_count:
        if max_index < min_index:
            return max_sum
        else :
            return min_sum
