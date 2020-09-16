from geopy import geocoders
from geopy import distance
g = geocoders.GoogleV3(api_key='apikeygoeshere')
inputAddress = '175 5th Ave, New York,  NY' 
location = g.geocode(inputAddress, timeout=10)
print(location.latitude, location.longitude)
print(location.raw)
print(location.address)

_, start = g.geocode(u"Kanpur".encode('utf-8'))
_, finish = g.geocode(u"Lucknow".encode('utf-8'))
print distance.distance(start, finish)







