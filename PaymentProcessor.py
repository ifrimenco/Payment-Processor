import datetime
import calendar

from errors import InvalidDataError

class PaymentProcessor:
    def __init__(self, request):
        exp_date = compute_expiration_date(int(request.form.get("expiration_month")),
                                           int(request.form.get("expiration_year")))
        self.payment = {
            'card_number': request.form.get("card_number"),
            'card_holder': request.form.get("card_holder"),
            'expiration_date': exp_date,
            'security_code': request.form.get("security_code"),
            'amount': int(request.form.get("amount"))
        }
        
        expGateway = True # checks if ExpensivePaymentGateway is available


    def validate_data(self):
        if (self.payment['card_number'] == None or self.payment['card_holder'] == None or
           validate_date(self.payment['expiration_date']) == 0 or
           validate_card(self.payment['card_number']) == False or self.payment['amount'] <= 0):
            raise InvalidDataError

    def process_payment(self):
        amount = self.payment['amount']


        if amount < 0:
            raise InvalidDataError

        if amount <= 500:
            if (amount <= 20 or expGateway == False):
                CheapPaymentGateway(amount)
            else:
                ExpensivePaymentGateway(amount)

        else:
            for i in range(3):
                if (PremiumPaymentGateway(amount) == True):
                    return None
                
        


# Payment Gateway Methods - they return true in case of succes
def CheapPaymentGateway(amount):
    # to be implemented
    return True


def ExpensivePaymentGateway(amount):
    # to be implemented
    return True

def PremiumPaymentGateway(amount):
    # to be implemented
    return True


def compute_expiration_date(month, year):
    expiration_date = datetime.datetime(year=year, 
                                        month=month, 
                                        day=calendar.monthrange(year, month)[1])
    return expiration_date



def validate_card(card_number):
    
    digits = str(card_number)

    if len(digits) != 16:
        return 0

    double = 0
    total = 0

    for i in range(len(digits) - 1, -1, -1):
        for c in str((double + 1) * int(digits[i])):
            total += int(c)
        double = (double + 1) % 2

    return (total % 10) == 0


def validate_date(expiration_date):
    return expiration_date != None and datetime.datetime.now() < expiration_date