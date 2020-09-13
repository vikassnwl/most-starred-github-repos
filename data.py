import requests

# getting response object from requests module by passing url and storing in r
url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
r = requests.get(url)
print('Status: ', r.status_code)

# entire data from above api call
data_dict = r.json()

# extracting items key from data_dict and using it's values
dict_items = data_dict['items']

name_of_repo = []
stargazers_count = []

for item in dict_items:
    print(item['name'])
