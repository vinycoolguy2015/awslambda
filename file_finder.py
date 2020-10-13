import os
from os.path import join
import re
import time
import tkMessageBox 


lookfor = "python"
result=[]
start_time=time.clock()
for root, dirs, files in os.walk('C:\\'):
    print "searching", root
    if re.search(lookfor, ''.join(files), flags=0):
        print "found: %s" % join(root, lookfor)
        result.append(join(root, lookfor))
end_time=time.clock()
print (str(len(result))+" files found")
tkMessageBox.showinfo("Execution completed","Time taken "+ str(end_time-start_time)+" seconds")
