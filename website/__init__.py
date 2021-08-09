from flask import Flask, request, render_template, flash
import requests



def create_app():
    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def home():

        latest_price = ''
        change_precent = ''
        change = ''
        open = ''
        high = ''
        low = ''
        fifty_two_weeks_high = ''
        fifty_two_weeks_low = ''
        company = ''

        try:
            if request.method == "POST":
                company = request.form['company']


                api_key = 'K5C1AVWTEC7NXPYQ'
                url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={company}&apikey={api_key}'
                url_2 = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={company}&apikey={api_key}'

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

                print(latest_price)

                return render_template("result.html",company=company, latest_price=latest_price, change_precent=change_precent, change=change, open=open,
                high=high, low=low, fifty_two_weeks_high=fifty_two_weeks_high, fifty_two_weeks_low=fifty_two_weeks_low)
        except KeyError:
            print("Couldn't get the stock")

        return render_template('index.html')

    return app