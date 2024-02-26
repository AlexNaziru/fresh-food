import json
import stripe
from django.conf import settings
from django.http import JsonResponse
from .models import Order, OrderItem
from cart.cart import Cart


def start_order(request):
    cart = Cart(request)
    # Getting info from the front end
    data = json.loads(request.body)
    # Sending price to stripe initially
    total_price = 0

    items = []
    for item in cart:
        product = item['product']
        total_price += product.price * int(item['quantity'])

        # Setting up a dictionary to append to items list
        obj = {  # Info that stripe needs from us to work
            'price_data': {
                'currency': 'ron',
                'product_data': {
                    'name': product.name
                },
                'unit_amount': product.price,
            },
            'quantity': item['quantity']
        }
        items.append(obj)

    # When we loop, we create a session
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=items,
        mode='payment',
        success_url='http://127.0.0.1:8000/cart/success',
        cancel_url='http://127.0.0.1:8000/cart'
    )
    payment_intent = session.payment_intent  # This is an id we get from stripe when everything is ok

    order = Order.objects.create(
        user=request.user,
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        address=data['address'],
        zipcode=data['zipcode'],
        place=data['place'],
        phone=data['phone'],
        payment_intent=payment_intent,
        paid=True,
        paid_amount=total_price)

    for item in cart:
        product = item['product']
        quantity = int(item['quantity'])
        price = product.price * quantity

        item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)

    cart.clear()

    return JsonResponse({'session': session, 'order': payment_intent})

