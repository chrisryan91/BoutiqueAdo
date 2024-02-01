from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm
from bag.contexts import bag_contents
import stripe
from dotenv import load_dotenv
import os



def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))
    
    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_total = round(total * 100)

    order_form = OrderForm()

    load_dotenv()
    # Now you can access environment variables using the os module
    stripe_public_key = os.getenv('STRIPE_PUBLIC_KEY')
    stripe_secret_key = os.getenv('STRIPE_SECRET_KEY')
    print("Stripe Public Key:", stripe_public_key)
    print("Stripe Secret Key:", stripe_secret_key)

    if not stripe_public_key or not stripe_secret_key:
        messages.error(request, "Stripe API keys are not set.")
        return redirect(reverse('products'))

    stripe.api_key = stripe_secret_key

    template = 'checkout/checkout.html'

    try:
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,  # Amount in cents
            currency='usd',
            # Verify your integration in this guide by including this parameter
            metadata={'integration_check': 'accept_a_payment'},
        )
    except stripe.error.StripeError as e:
        # Handle Stripe errors, if any
        messages.error(request, str(e))
        return redirect(reverse('products'))

    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)
