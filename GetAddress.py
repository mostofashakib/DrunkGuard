import requests
from geopy.geocoders import Nominatim

def GetAddress_Run():

	ip_request = requests.get('https://get.geojs.io/v1/ip.json')
	my_ip = ip_request.json()['ip']

	geo_request_url = 'https://get.geojs.io/v1/ip/geo/' + my_ip + '.json'
	geo_request = requests.get(geo_request_url)
	geo_data = geo_request.json()

	address = geo_data['latitude'] + ", " + geo_data['longitude']

	geolocator = Nominatim(user_agent="GetAddress")
	location = geolocator.reverse(str(address))

	def display_ip():
	    ip_request = requests.get('https://get.geojs.io/v1/ip.json')
	    my_ip = ip_request.json()['ip']
	    geo_request = requests.get('https://get.geojs.io/v1/ip/geo/' +my_ip + '.json')
	    geo_data = geo_request.json()

	return location.address