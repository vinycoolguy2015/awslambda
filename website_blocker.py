from datetime import datetime as dt
import time
host_file="C:\Windows\System32\drivers\etc\hosts"
websites=["www.facebook.com","www.youtube.com"]
redirect="127.0.0.1"

while True:
    if (dt.now().hour >=10 and dt.now().hour<=18):
        print("Working Hours")
        with open(host_file,'r+') as f:
            content = f.read()
            for website in websites:
                if website in content:
                    pass
                else:
                    f.seek(0, 2)
                    f.write("\n"+redirect+ " "+website)
                
    else: 
        print("Let's have some fun")
        with open(host_file,'r+') as f:
            content = f.readlines()
            f.seek(0)
            for line in content:
                if not any(website in line for website in websites):
                    f.write(line)
                f.truncate()
    time.sleep(5)
            
            
            
            
    
    
    
