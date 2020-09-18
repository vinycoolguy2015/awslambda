def match_status():
    from bs4 import BeautifulSoup
    import requests
    import datetime
    import sys
    

    baseurl='https://www.espncricinfo.com/'

    result = requests.get(baseurl)
    soup=BeautifulSoup(result.text,'lxml')
    match_today=False
    
    for link in soup.findAll('a', href=True):
		if 'indian-premier-league' in str(link['href']):
            matchurl=link['href']
			match_today=True
            break
    if match_today==False:
        return "No match today"
        sys.exit(0)
	
    result = requests.get(baseurl+matchurl)
    soup=BeautifulSoup(result.text,'lxml')
	
    team1=soup.findAll("div", { "class" : "team-col" })[0].text.strip()
    team2=soup.findAll("div", { "class" : "team-col" })[2].text.strip()
	
    
    try:
        match_start_time=soup.find("div", { "class" : "status-label" }).text.strip()
        match_start_time=datetime.datetime.strptime(match_start_time.replace(',',''), '%d-%b-%Y %I:%M %p')
        time_remaining=match_start_time-datetime.datetime.utcnow()
        return "Match between "+team1+" and "+team2+" will start in "+str(time_remaining)+" hours"
    except:
        return "Match between "+team1+" and "+team2+" is in progress"
	
def notify(title, text):
    import os
    os.system("""osascript -e 'display notification "{}" with title "{}"'""".format(text, title))

	
def main():
	status=match_status()
	notify("IPL match notification", status)	
	
if __name__ == '__main__':
	main()
	
    
