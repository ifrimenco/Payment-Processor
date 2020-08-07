import pytest

from flask import Flask, request
import process_payment

def test_payment_succes():
    app = process_payment.app
    with app.test_client() as client:
        response = client.post('/', 
                    data = {
                        'card_number': '4111111111111111',
                        'card_holder': 'Andrew Smith',
                        'expiration_month': 5,
                        'expiration_year': 2083,
                        'security_code': 252,
                        'amount': 252
                    })
        assert response.status_code == 200
    

def test_bad_request_wrong_card():
    app = process_payment.app
    with app.test_client() as client:
        response = client.post('/',
                    data = {
                        'card_number': '3716009271998',
                        'card_holder': 'John Smith',
                        'expiration_month': 5,
                        'expiration_year': 2023,
                        'security_code': 252,
                        'amount': 252
                    })
        assert response.status_code == 400


def test_bad_request_empty_name():
    app = process_payment.app
    with app.test_client() as client:
        response = client.post('/',
                    data = {
                        'card_number': '4111111111111111',
                        'card_holder': None,
                        'expiration_month': 5,
                        'expiration_year': 2023,
                        'security_code': 252,
                        'amount': 252
                    })
        assert response.status_code == 400

def test_bad_request_wrong_date():
    app = process_payment.app
    with app.test_client() as client:
        response = client.post('/',
                    data = {
                        'card_number': '4111111111111111',
                        'card_holder': None,
                        'expiration_month': 5,
                        'expiration_year': 203,
                        'security_code': 252,
                        'amount': 252
                    })
        assert response.status_code == 400



def test_bad_request_negative_amount():
    app = process_payment.app
    with app.test_client() as client:
        response = client.post('/',
                    data = {
                        'card_number': '4111111111111111',
                        'card_holder': None,
                        'expiration_month': 5,
                        'expiration_year': 2023,
                        'security_code': 252,
                        'amount': -5
                        })
        assert response.status_code == 400


def test_prediction_succes():
    app = process_payment.app
    with app.test_client() as client:
        response = client.post('/estimate-price',
                    data = {
                        'year': '2011',
                        'month': '4',
                        'day': '8',
                        'stock': 'AA'
                    })
        assert response.status_code == 200