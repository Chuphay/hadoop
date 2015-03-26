# simple api example 
# to be used with python 3
import urllib.request
import json

api_key = 'cf2a8bdb6289efa4a18fa091216fc9b8e0b0eda4'
def locu_search(search):
	# first we want to define the url we are going to search the api in
	base_url = 'https://api.locu.com/v1_0/venue/search/?&api_key=cf2a8bdb6289efa4a18fa091216fc9b8e0b0eda4'
	locality = search.replace(' ','%20')
	final_url = base_url + '&locality=' + locality + '&category=restaurant' 
	json_obj = urllib.request.urlopen(final_url)
	decoded_json_obj = json_obj.readall().decode('utf-8')
	data = json.loads(decoded_json_obj)
	for item in data['objects']:
		print(item['name'])
		print((item['phone']))


def locu_search_more(loc, cat):
    # first we want to define the url we are going to search the api in
    base_url = 'https://api.locu.com/v1_0/venue/search/?&api_key=cf2a8bdb6289efa4a18fa091216fc9b8e0b0eda4'
    locality = loc.replace(' ','%20')
    category = cat.replace(' ','%20')
    final_url = base_url + '&locality=' + locality + '&category=' +category 
    json_obj = urllib.request.urlopen(final_url)
    decoded_json_obj = json_obj.readall().decode('utf-8')
    data = json.loads(decoded_json_obj)
    for item in data['objects']:
        print(item['name'])
        print((item['phone']))

# lets make this a little more interacticve
answer = 'yes'
while(answer == 'yes' or answer == 'y'):
    print('Hello please enter the city you wish to search: ')
    location_city = input()
    print('What type of location are you searching for: (restaurant, spa, gym etc)')
    category = input()
    locu_search_more(location_city,category)
    print('Would you like to make another search? (yes or no)')
    answer = input()

