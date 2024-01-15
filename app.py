import requests
import json


response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()

my_dict = dict(zip(range(len(data)), data))
print(type(my_dict))

rates = (my_dict[0]['rates'])
print(rates)
