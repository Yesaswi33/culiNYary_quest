from django.shortcuts import render
from .models import *
from django.shortcuts import redirect
from .models import Cart


# Create your views here.
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})


def product_detail(request, slug):
    product = Product.objects.get(product_slug=slug)
    return render(request, 'products/product_detail.html', {'product': product})

def add_to_cart(request, product_id):
    product = Product.objects.get(uid=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')


def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'products/cart.html', {'cart_items': cart_items, 'total': total})
