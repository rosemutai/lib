from django.shortcuts import render,get_object_or_404, redirect
from django.contrib import  messages
from web.models import ExerciseBook
from cart.models import Cart, Order
from django.contrib.auth.decorators import login_required

# Create your views here.



def remove_from_cart(request, id):
    item = get_object_or_404(ExerciseBook, id=id)
    cart_qs = Cart.objects.filter(user=request.user, item=item)
    if cart_qs.exists():
        cart = cart_qs[0]
        if cart.quantity > 1:
            cart.quantity -= 1
            cart.save()
        else:
            cart_qs.delete()
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item__id=item.id).exists():
            order_item = Cart.objects.filter(item=item, user=request.user)[0]
            order.orderitems.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect("books.html")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("books.html")
    else:
        messages.info(request, "You do not have an active order")
        return  redirect("books.html")





