from flask import Flask, request, render_template, redirect
import requests

# file deepcode ignore HardcodedNonCryptoSecret: <declaring the key>
API_KEY = 'K5C1AVWTEC7NXPYQ'

def create_app():
    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def home():

        try:
            if request.method == "POST":
                company = request.form['company'].upper()
                company = company.upper()

                url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={company}&apikey={API_KEY}'
                url_2 = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={company}&apikey={API_KEY}'

                r1 = requests.get(url)
                r2 = requests.get(url_2)

                data = r1.json()['Global Quote']
                latest_price = r1.json()['Global Quote']['05. price']
                change_precent = r1.json()['Global Quote']['10. change percent']
                change = r1.json()['Global Quote']['09. change']
                open = r1.json()['Global Quote']['02. open']
                high = r1.json()['Global Quote']['03. high']
                low = r1.json()['Global Quote']['04. low']
                fifty_two_weeks_high = r2.json()['52WeekHigh']
                fifty_two_weeks_low = r2.json()['52WeekLow']


                return render_template("result_search.html",company=company, latest_price=latest_price, change_precent=change_precent,
                 change=change, open=open,high=high, low=low, fifty_two_weeks_high=fifty_two_weeks_high, fifty_two_weeks_low=fifty_two_weeks_low)
        except Exception:
            pass

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
                    print("Can't compare company")
                    return render_template('compare.html')

                #Getting company 1 urls
                url_company1_1 = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={company_1}&apikey={API_KEY}'
                url_company1_2 = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={company_1}&apikey={API_KEY}'
                url_company2_1 = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={company_2}&apikey={API_KEY}'
                url_company2_2 = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={company_2}&apikey={API_KEY}'

                #Requesting company 1
                r1_company_1 = requests.get(url_company1_1)
                r2_company_1 = requests.get(url_company1_2)
                r1_company_2 = requests.get(url_company2_1)
                r2_company_2 = requests.get(url_company2_2)

                #Getting all the details of company 1
                latest_price_1 = r1_company_1.json()['Global Quote']['05. price']
                change_precent_1 = r1_company_1.json()['Global Quote']['10. change percent']
                change_1 = r1_company_1.json()['Global Quote']['09. change']
                open_1 = r1_company_1.json()['Global Quote']['02. open']
                high_1 = r1_company_1.json()['Global Quote']['03. high']
                low_1 = r1_company_1.json()['Global Quote']['04. low']
                fifty_two_weeks_high_1 = r2_company_1.json()['52WeekHigh']
                fifty_two_weeks_low_1 = r2_company_1.json()['52WeekLow']

                #Getting all the details of company 2
                latest_price_2 = r1_company_2.json()['Global Quote']['05. price']
                change_precent_2 = r1_company_2.json()['Global Quote']['10. change percent']
                change_2 = r1_company_2.json()['Global Quote']['09. change']
                open_2 = r1_company_2.json()['Global Quote']['02. open']
                high_2 = r1_company_2.json()['Global Quote']['03. high']
                low_2 = r1_company_2.json()['Global Quote']['04. low']
                fifty_two_weeks_high_2 = r2_company_2.json()['52WeekHigh']
                fifty_two_weeks_low_2 = r2_company_2.json()['52WeekLow']


                return render_template("result_compare.html",company_1=company_1, company_2=company_2, latest_price_1=latest_price_1,
                latest_price_2=latest_price_2, change_precent_1=change_precent_1, change_precent_2=change_precent_2, change_1=change_1,
                change_2=change_2, open_1=open_1, open_2=open_2, high_1=high_1, high_2=high_2, low_1=low_1, low_2=low_2,
                fifty_two_weeks_low_1=fifty_two_weeks_low_1, fifty_two_weeks_low_2=fifty_two_weeks_low_2,
                fifty_two_weeks_high_1=fifty_two_weeks_high_1, fifty_two_weeks_high_2=fifty_two_weeks_high_2)
        except Exception:
            return redirect('/compare')



    return app