import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import re

ua = UserAgent()
header = {'user-agent':ua.chrome}

genre=raw_input("Please select one of the given genre:action,animation,adventure,biography,comedy,crime,documentary,drama,family,fantasy,history,horror,music,mystery,romance,sci_fi,sport,thriller,war ")
rating=float(raw_input("Please select the minimum rating of the movie "))
year=int(raw_input("Please select the minimum release year of the movie "))

print("Searching Movies for you \n\n")

BASE_URL='http://www.imdb.com/search/title?genres='

for counter in range(1,2501,50):
	end=False
	#URL=BASE_URL+genre+'&title_type=feature&sort=user_rating,desc&page='+str(counter)
	URL=BASE_URL+genre+'&title_type=feature&sort=user_rating,desc&start='+str(counter)
	try:
		data = requests.get(URL,headers=header)
	except requests.exceptions.ConnectionError:
		print("Error establishing connection")
		exit()
	soup=BeautifulSoup(data.content,'lxml')
	results = soup.findAll("div", { "class" : "lister-item mode-advanced" })
	
	for result in results:
		movie=result.findChild("h3", { "class" : "lister-item-header" }).findChild('a').text.replace('(','').replace(')','')
		movie_year=result.findChild("span", { "class" : "lister-item-year text-muted unbold" }).text.replace('(','').replace(')','')
		movie_year=int(re.sub('[^0-9]','', movie_year))
		movie_rating=float(result.findChild("div", { "class" : "inline-block ratings-imdb-rating" })['data-value'])
		if movie_rating >= rating:
			if movie_year>=year:
				print movie.encode("utf-8"),movie_year,movie_rating
		else:
			end=True
			break
	if end==True:
		break
		
		
		
	
	
	
	
	



	
	
		
