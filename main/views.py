from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import Products, Category, Cart, CartItem

def index(request):
    products = Products.objects.all()
    categories = Category.objects.all()
    
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    context = {
        'products': products,
        'categories': categories,
        'cart_count': get_cart_count(request),
    }
    return render(request, 'index.html', context)

def get_cart_count(request):
    if request.user.is_authenticated:
        try:
            cart = request.user.cart
            return cart.get_total_items()
        except Cart.DoesNotExist:
            return 0
    return 0

@login_required(login_url='auth:login')
@require_http_methods(["POST"])
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    
    product = get_object_or_404(Products, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    messages.success(request, f"{product.product_name} added to cart!")
    return redirect('main:index')

@login_required(login_url='auth:login')
def cart_view(request):
    try:
        cart = request.user.cart
    except Cart.DoesNotExist:
        cart = None
    
    context = {
        'cart': cart,
        'cart_count': get_cart_count(request),
    }
    return render(request, 'cart_page.html', context)

@login_required(login_url='auth:login')
@require_http_methods(["POST"])
def update_cart_item(request):
    item_id = request.POST.get('item_id')
    quantity = int(request.POST.get('quantity', 1))
    action = request.POST.get('action', 'update_quantity')
    
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    
    if action == 'remove':
        cart_item.delete()
        messages.success(request, "Item removed!")
    else:
        if quantity <= 0:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "Quantity updated!")
    
    return redirect('main:cart')

@login_required(login_url='auth:login')
@require_http_methods(["POST"])
def remove_from_cart(request):
    item_id = request.POST.get('item_id')
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Removed from cart!")
    return redirect('main:cart')