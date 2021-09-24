import json

from . models import *
from shop.models import *
# from account.models import *

from . views import *
import datetime
from datetime import date
import random
import math
import string
from hashlib import sha256
from django.db.models import Count

def generate_order_id():
    date_str = date.today().strftime('%Y%m%d')[2:] + str(datetime.datetime.now().second)
    # print(date_str)
    rand_str = "".join([random.choice(string.digits) for count in range(3)])
    # print(rand_str)
    return date_str + rand_str



def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
        # print("cart:",cart)
    items = []
    order = {'get_total':0,'get_cart_total':0, 'get_cart_items':0, 'shipping': False,'get_cart_ship_total':0,'get_ship_total':0}
    cartItems = order['get_cart_items']

    for i in cart:
        # print(cart[i])
        try:
            cartItems += cart[i]["quantity"]
            if cart[i]["quantity"] >=1 :
                quant =cart[i]["quantity"]
            else:
                quant = 0
            # print("adfsgdhj=====================",quant)
            Product = product.objects.get(id=i)
            if Product.discount_price == '0':
                total = (Product.price * cart[i]["quantity"])
                price = Product.price
                discount_price= 0
                # print("Price",price)
            else:
                total = (Product.discount_price * cart[i]["quantity"])
                price = Product.price

                discount_price = Product.discount_price
                # print("Price",price)

            # print("price-------------",price)
            order['get_cart_total'] += total
            # print(order['get_cart_total'])
            order['get_cart_items'] = cartItems
            abc=0
            abc=order['get_cart_total']
            # print("acbjhacbcbjdab----------",order['get_cart_total'])

            # print(order['get_cart_ship_total'])
            item = {
                'product':{
                    'id':Product.id,
                    # 'name':Product.title_name.objects.first().book_name,
                    'ProductName': Product.ProductName,
                    'price':price,
                    'discount_price':discount_price,
                    'image':Product.image,
                    'slug': Product.slug
                },
                'quantity': quant,
                'get_total':total,
                }
            items.append(item)
            # print("1256354825=====",items)
            # if Product.digital == False:
            #     order['shipping'] = True
        except:

            pass
    if cartItems <= 2:
        ship_cost = 100

    elif cartItems>2 and cartItems <=4:
        ship_cost = 200

    else :
        ship_cost = 300


    order['get_ship_total'] = ship_cost


    order['get_cart_ship_total'] = order['get_ship_total']+order['get_cart_total']
    return{'cartItems':cartItems, 'order':order, 'items': items}

def cartData(request):
    print("hellloooo")
    if request.user.is_authenticated:
        profile = request.user.profile.first()
        # print(request.user.profile.first())
        try:
            order = Order.objects.get(profile=profile, complete=False)
        # order = Order.objects.filter(profile=profile, complete=False).first()
        except:
            order=Order.objects.create(profile=profile, complete=False)
            if not order.order_num:
                order.order_num = generate_order_id()
        order.save()
        items = order.OrderItem.all()

        cartItems = order.get_cart_items

    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return{'cartItems':cartItems, 'order':order, 'items': items}

def guestOrder(request, data):
    # print('user is not logged in..')

    # print('Cookies:', request.COOKIES)
    name = data['form']['name']

    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    profile, created = UserProfile.objects.get_or_create(
        email= email,
    )
    profile.name = name
    profile.save()

    order, created = Order.objects.get_or_create(
        profile = profile,
        complete =False,
    )


    for item in items:
        product = product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            product = product,
            order = order,
            quantity = item['quantity']
            )
    return profile,order
