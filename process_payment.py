from flask import Flask, abort, render_template, url_for, request


from PaymentProcessor import PaymentProcessor   #Payment Processor Service
from errors import InvalidDataError
from PriceEstimator import PriceEstimator
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def process_payment():
    if request.method =='POST': 

        try:
            paymentProcessor = PaymentProcessor(request)
            paymentProcessor.validate_data()
            return ('Hello, ' + paymentProcessor.payment.get('card_holder')), 200
        except InvalidDataError:
            return ('Bad Request 400'), 400

        except:
            return '500 Internal Server Error', 500
        

    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/estimate-price', methods=['POST', 'GET'])
def estimate_price():
    if request.method =='POST':

        try:
            p = PriceEstimator(request)
            p.make_prediction()
            return 'Hello, World!', 200
        except:
            return '500 Internal Server Error', 500