import requests
import json
import csv

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data_API = response.json()
my_dict = dict(zip(range(len(data_API)), data_API))

dict_data = (my_dict[0]['rates'])

csv_columns = []
for i in dict_data[0]:
    csv_columns.append(i)
print(csv_columns)

with open("bank_rates.csv", 'w', encoding='utf8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter=';')
        writer.writeheader()
        for data in dict_data:
            writer.writerow(data)
