from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm

from checkout.models import Order 

# Create your views here.


@login_required
def profile(request):

    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form= UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Updated Succesfully')
        else:
            messages.error(request, 'Update failed. Ensure validity.')

    else:    
        form = UserProfileForm(instance=profile)

    template = 'profiles/profile.html'
    orders = profile.orders.all()
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True
    }

    return render(request, template, context)

@login_required
def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}.'
        'A confirmation email will be sent out'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'form_profile': True,
    }

    return render(request, template, context)