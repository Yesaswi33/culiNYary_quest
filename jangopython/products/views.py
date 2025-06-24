from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.contrib import messages

from .models import Product, Cart, Order
from vege.models import Recepie


def product_list(request):
    products = Product.objects.all()
    receipes = Recepie.objects.all()
    return render(request, 'products/product_list.html', {
        'products': products,
        'receipes': receipes,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, product_slug=slug)
    return render(request, 'products/product_detail.html', {'product': product})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, uid=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')


@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'products/cart.html', {'cart_items': cart_items, 'total': total})


@csrf_exempt
@login_required
def add_custom_dish_to_cart(request, dish_id):
    if request.method == 'POST':
        dish = get_object_or_404(Recepie, id=dish_id)
        
        # Ensure slug is safe
        slug_base = dish.receipe_name.lower().replace(' ', '-') if dish.receipe_name else f'dish-{dish_id}'
        
        # Create or get corresponding Product
        product, _ = Product.objects.get_or_create(
            product_name=dish.receipe_name,
            defaults={
                'product_slug': slug_base,
                'product_description': dish.receipe_description or 'Tasty dish',
                'product_price': dish.receipe_price or 99,
            }
        )

        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()

        messages.success(request, f"{product.product_name} added to your cart!")

    return redirect('cart')


@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, uid=product_id)
    cart_item = get_object_or_404(Cart, user=request.user, product=product)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
        
    return redirect('cart')


@login_required
@csrf_exempt
def update_cart_quantity(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
    return redirect('cart')
