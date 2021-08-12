from flask import Flask, request, render_template, redirect
import requests

API_KEY = 'K5C1AVWTEC7NXPYQ'

def create_app():
    app = Flask(__name__)

    def get_company(company):
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={company}&apikey={API_KEY}'

        response = requests.get(url)

        try:
            price = response.json()['Global Quote']['05. price']
            change_percent  = response.json()['Global Quote']['10. change percent']
            change = response.json()['Global Quote']['09. change']
            open = response.json()['Global Quote']['02. open']
            high = response.json()['Global Quote']['03. high']
            low = response.json()['Global Quote']['04. low']

            details = {
                'company': company,
                'price': price,
                'changePercent': change_percent,
                'change': change,
                'open': open,
                'high': high,
                'low': low
            }
        except KeyError:
            return None

        return details

    @app.route('/', methods=['GET', 'POST'])
    def home():

        try:
            if request.method == "POST":
                company = request.form['company'].upper()

                details = get_company(company)

                return render_template("result_search.html", details=details)
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
                company_1 = request.form['company1'].upper()
                company_2 = request.form['company2'].upper()

                if company_1 == company_2:
                    print("You have entered the same company")
                    return render_template('compare.html')

                details_1 = get_company(company_1)
                details_2 = get_company(company_2)

                return render_template("result_compare.html", details_1=details_1, details_2=details_2)
        except Exception:
            return redirect('/compare')

    return app