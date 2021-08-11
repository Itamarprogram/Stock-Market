from flask import Flask, request, render_template, redirect
import requests

# file deepcode ignore HardcodedNonCryptoSecret: <declaring the key>
API_KEY = 'K5C1AVWTEC7NXPYQ'

def create_app():
    app = Flask(__name__)

    def get_company(company):
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={company}&apikey={API_KEY}'

        r1 = requests.get(url)

        try:
            latest_price = r1.json()['Global Quote']['05. price']
            print(latest_price)
            change_percent  = r1.json()['Global Quote']['10. change percent']
            print(change_percent)
            change = r1.json()['Global Quote']['09. change']
            print(change)
            open = r1.json()['Global Quote']['02. open']
            print(open)
            high = r1.json()['Global Quote']['03. high']
            print(high)
            low = r1.json()['Global Quote']['04. low']
            print(low+"\n")
        except KeyError:
            print("There is no such company")
            return None

        return latest_price, change_percent , change, open, high, low


    @app.route('/', methods=['GET', 'POST'])
    def home():

        try:
            if request.method == "POST":
                company = request.form['company']
                company = company.upper()

                latest_price, change_percent, change, open, high, low = get_company(company)

                return render_template("result_search.html",company=company, latest_price=latest_price, change_percent=change_percent,
                    change=change, open=open,high=high, low=low)
        except Exception:
            print("There is some error I suppose")

        return render_template("index.html")
     
    @app.route('/compare', methods=['GET','POST'])
    def redirect_compare():
        return render_template('compare.html')


    @app.route('/comparison', methods=['POST'])
    def comparison():
        try:
            if request.method == 'POST':
                company_1 = request.form['company1']
                company_1 = company_1.upper()
                company_2 = request.form['company2']
                company_2 = company_2.upper()

                if company_1 == company_2:
                    print("The same company")
                    return render_template('compare.html')

                latest_price_1, change_percent_1, change_1, open_1, high_1, low_1 = get_company(company_1)
                latest_price_2, change_percent_2, change_2, open_2, high_2, low_2 = get_company(company_2)

                return render_template("result_compare.html",company_1=company_1, company_2=company_2, latest_price_1=latest_price_1,
                latest_price_2=latest_price_2, change_precent_1=change_percent_1, change_precent_2=change_percent_2, change_1=change_1,
                change_2=change_2, open_1=open_1, open_2=open_2, high_1=high_1, high_2=high_2, low_1=low_1, low_2=low_2,)
        except Exception:
            return redirect('/compare')

    return app