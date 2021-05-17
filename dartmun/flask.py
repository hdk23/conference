import os
import stripe

from flask import Flask, jsonify

app = Flask(__name__)

stripe.api_key = 'sk_test_51InZXBFBCMNMdnJVuuNVFjDyQlLw6uCWCtrpBaDzFS6ezCtaoJtGr2qdLGSZPO900czOuoM5phPwxAqcybZPGbLN00ouIQKOxc'


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session(request):
  session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
      'price_data': {
        'currency': 'usd',
        'product_data': {
          'name': 'Support Developer',
        },
        'unit_amount': 100,
      },
      'quantity': 1,
    }],
    mode='payment',
    success_url='127.0.0.1:8000/dartmun/bio/',
    cancel_url='127.0.0.1:8000/dartmun/checkout/',
  )

  return jsonify(id=session.id)

if __name__== '__main__':
    app.run(port=8000)
