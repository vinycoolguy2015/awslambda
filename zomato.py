import requests
import json
import sys

def city_details():
	city_name=raw_input("Enter city name ")
	city_details = "https://developers.zomato.com/api/v2.1/cities?q="+city_name
	header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": "<your key>"}
	response = requests.get(city_details, headers=header)
	city_id=response.json()['location_suggestions'][0]['id']
	return city_id

def restaurant_search(city_id):
	for count in range(1,50,20):
		url_endpoint="https://developers.zomato.com/api/v2.1/search?entity_id="+str(city_id)+"&entity_type=city&start="+str(count)+"&count=20&sort=rating"
		header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": "<your_key>"}
		response = json.loads(requests.get(url_endpoint, headers=header).text)
		for key,value in response.iteritems():
			if key =='restaurants':
				for item in value:
					print item['restaurant']['name'],item['restaurant']['user_rating']['aggregate_rating'],item['restaurant']['average_cost_for_two'],item['restaurant']['location']['address']
			

if __name__=="__main__":
	try:
		city_id=city_details()
	except:
		print("Data not available")
		sys.exit()
	restaurant_search(city_id)
	
	
