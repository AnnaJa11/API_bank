from flask import Flask, render_template, request, redirect, url_for
import requests
import csv

app = Flask(__name__)


response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data_API = response.json()
my_dict = dict(zip(range(len(data_API)), data_API))


dict_data = (my_dict[0]['rates'])

csv_columns = []
for i in dict_data[0]:
    csv_columns.append(i)

with open("bank_rates.csv", 'w', encoding='utf8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter=';')
        writer.writeheader()
        for data in dict_data:
            writer.writerow(data)

     
@app.route('/')
def base_templ():
    return render_template('base.html')

@app.route("/base/calc", methods=['GET', 'POST'])
def test():
    if request.method == 'GET':
       print("We received GET from CALC")
       return render_template("calculator.html", data=dict_data)
    elif request.method == "POST":
        form_data = request.form
        print(form_data)
        select = form_data.get('user_select')
        user_value = form_data.get('user_amount')
        return select, user_value    # just to see what is there
    return redirect("/")
   
dict_data_length = len(dict_data)
currency_codes = []
for i in range (0, dict_data_length):
    code = dict_data[i]['code']
    currency_codes.append(code)      
print(currency_codes)
   
currency_ask_values = []
for i in range (0, dict_data_length):
    ask_value = dict_data[i]['ask']
    currency_ask_values.append(ask_value)
print(currency_ask_values)

user_code_choice = input('Choose index  of currency: ')
user_value = float(input('Enter your value: '))
code_index = currency_codes.index(user_code_choice)
code_ask_value = currency_ask_values[code_index]
print(code_ask_value)
result = round(user_value * code_ask_value, 2)
print(f'{result} PLN')

if __name__ == "__main__":
    app.run(debug=True)
  