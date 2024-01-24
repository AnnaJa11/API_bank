from flask import Flask, render_template, request, redirect, url_for
import requests
import csv

app = Flask(__name__)


response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data_API = response.json()
my_dict = dict(zip(range(len(data_API)), data_API))
dict_data = (my_dict[0]['rates'])

# dict_data = [{'currency': 'dolar amerykański', 'code': 'USD', 'bid': 4.0042, 'ask': 4.085}, {'currency': 'dolar australijski', 'code': 'AUD', 'bid': 2.6332, 'ask': 2.6864}, {'currency': 'dolar kanadyjski', 'code': 'CAD', 'bid': 2.9703, 'ask': 3.0303}, {'currency': 'euro', 'code': 'EUR', 'bid': 4.3457, 'ask': 4.4335}, {'currency': 'forint (Węgry)', 'code': 'HUF', 'bid': 0.011261, 'ask': 0.011489}, {'currency': 'frank szwajcarski', 'code': 'CHF', 'bid': 4.5965, 'ask': 4.6893}, {'currency': 'funt szterling', 'code': 'GBP', 'bid': 5.0773, 'ask': 5.1799}, {'currency': 'jen (Japonia)', 'code': 'JPY', 'bid': 0.026992, 'ask': 0.027538}, {'currency': 'korona czeska', 'code': 'CZK', 'bid': 0.1748, 'ask': 0.1784}, {'currency': 'korona duńska', 'code': 'DKK', 'bid': 0.5827, 'ask': 0.5945}, {'currency': 'korona norweska', 'code': 'NOK', 'bid': 0.3806, 'ask': 0.3882}, {'currency': 'korona szwedzka', 'code': 'SEK', 'bid': 0.3821, 'ask': 0.3899}, {'currency': 'SDR (MFW)', 'code': 'XDR', 'bid': 5.3134, 'ask': 5.4208}]

csv_columns = []
for i in dict_data[0]:
    csv_columns.append(i)

with open("bank_rates.csv", 'w', encoding='utf8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter=';')
        writer.writeheader()
        for data in dict_data:
            writer.writerow(data)

codes = []
for i in dict_data:
    code = (i['code'])
    codes.append(code)
# codes = ['USD', 'AUD', 'CAD', 'EUR', 'HUF', 'CHF', 'GBP', 'JPY', 'CZK', 'DKK', 'NOK', 'SEK', 'XDR']
asks = []
for i in dict_data:
    ask = (i['ask'])
    asks.append(ask)
# asks = [4.085, 2.6864, 3.0303, 4.4335, 0.011489, 4.6893, 5.1799, 0.027538, 0.1784, 0.5945, 0.3882, 0.3899, 5.4208]
     
@app.route('/')
def home():
    return render_template('base.html')

@app.route("/base/calc", methods=['GET', 'POST'])
def calc():
    payment = ''
    if request.method == ['POST']:
       amount = request.form.get("amount")
       user_select = request.form.get("code")
       for item in dict_data:
          if item['code'] == user_select:
            payment = round((float(item['ask']) * float(amount)), 2)
    return render_template("calculator.html", codes=codes, payment=payment)
 

if __name__ == "__main__":
    app.run(debug=True)
  