from flask import Flask, abort, render_template, url_for, request


from PaymentProcessor import PaymentProcessor   #Payment Processor Service
from errors import InvalidDataError

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