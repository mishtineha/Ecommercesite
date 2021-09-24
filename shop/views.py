from django.shortcuts import render, redirect
from .models import *
from account.models import *
from home.models import *

from django.contrib.auth.decorators import login_required, user_passes_test

import os



import json
# Create your views here.
from django.db.models import F
from django.db.models import Q

from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import  get_object_or_404
from django.urls import reverse
#Paging
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.decorators.csrf import csrf_exempt
import requests
import hashlib
import hmac
import base64
# import reportlab
import string
from hashlib import sha256
from django.db.models import Count

from rest_framework import pagination


from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib import messages


from django.urls import reverse_lazy
from django.views import generic

import math
import random

from django.core.mail import send_mail
from django.contrib.auth.models import User, Group
import razorpay
from django.core.exceptions import ObjectDoesNotExist

keyID = 'rzp_test_tUKqhcADEgW9fB'
secretKey = 'VuhjcEHGQUuo1xJOSMHgTLqa'

client = razorpay.Client(auth=(keyID,secretKey))

def generate_order_id():
    date_str = "SAY"+date.today().strftime('%Y%m%d')[2:] + str(datetime.datetime.now().second)
    # print(date_str)
    rand_str = "".join([random.choice(string.digits) for count in range(3)])
    # print(rand_str)
    return date_str + rand_str


@login_required
def cart(request):
    try:
        order = Order.objects.get(profile=request.user.profile, complete=False)
    except ObjectDoesNotExist:
        order = None
    category = Category.objects.all()
    context = {
        'Category': category,
        'order': order,
        'profile': request.user.profile
    }
    return render(request, 'cart.html', context)


@login_required
def checkout(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except:
        profile= None
    try:
        order = Order.objects.get(profile=profile, complete=False)
        if not order.order_num:
            order.order_num = generate_order_id()
        order.save()
    except:
        order = None
    category = Category.objects.all()
    form = invoiceModelForm()

    if request.method == "POST":

        print("===================================================================================")
        form = invoiceModelForm(request.POST or None)
        form.full_clean()
        print("invoiceform=====--======-----",form.errors)

    # check if form data is valid
        if form.is_valid():
        # save the form data to model
            invoiceForm = form.save()
            invoiceForm.order_id = order.order_num
            invoiceForm.owner = profile
            invoiceForm.save()
            # abc = invoiceModel.objects.get(id=invoiceForm.pk)
            #
            # print(abc)
            return redirect(reverse('shop:checkoutDetails'))
        else:
            messages.warning(request,'Please fill the form correctly')

    context = {
        'Category':category,
        'order':order,
        'profile':profile,
        'form':form,

    }
    return render(request,'checkout.html',context)

@login_required
def checkoutDetails(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except:
        profile= None
    try:
        try:
            device = request.COOKIES['device']
            order = Order.objects.get(device=device,complete=False)
            if not order.device:
                order.device = device
            order.save()
        except:
            order = Order.objects.get(profile=profile,complete=False)

        if not order.order_num:
            order.order_num = generate_order_id()
        order.save()
    except:
        order = None
    category = Category.objects.all()
    subcate = subcategory.objects.all()
    # print(client)
    newOrder = Order.objects.get(profile = profile, complete=False)
    print(newOrder,profile)
    invoice = invoiceModel.objects.filter(owner = profile,order_id=newOrder,success=False).last()

    newOrder.is_initiated = True
    newOrder.save()


    order_amount = int(newOrder.get_cart_total*100),
    order_currency = 'INR'
    order_receipt = newOrder.order_num
    # notes = {'Shipping address': 'Bommanahalli, Bangalore'}   # OPTIONAL
    # print(order_amount)

    response = client.order.create(dict(amount=order_amount[0], currency=order_currency,receipt=order_receipt))
    order_id = response['id']
    order_status = response['status']

    if order_status=='created':
        context ={'price':order_amount,
                  'name': invoice.nameDetail,
                  'phone': str(invoice.phone_number),
                  'email' : invoice.email,
                  'invoice_id' : order_id,
                  'invoice':invoice,
                  # 'order_num' : newOrder
                  }
        return render(request, 'checkoutload.html', context)

    return HttpResponse('<h1>Error! Please Try again later</h1>')


from django.templatetags.static import static
#from django.contrib.staticfiles.templatetags.staticfiles import static
from fpdf import FPDF, HTMLMixin
class HTML2PDF(FPDF, HTMLMixin):
    pass

from datetime import timedelta
import datetime
from datetime import date
@login_required
@csrf_exempt
def check_response(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except:
        profile= None
    try:
        try:
            device = request.COOKIES['device']
            order = Order.objects.get(device=device,complete=False)
            if not order.device:
                order.device = device
            order.save()
        except:
            order = Order.objects.get(profile=profile,complete=False)

        if not order.order_num:
            order.order_num = generate_order_id()
        order.save()
    except:
        order = None
    print(order)
    Category = category.objects.all()
    subcate = subcategory.objects.all()

    response = request.POST

    params_dict = {
        'razorpay_payment_id' : response.get('razorpay_payment_id'),
        'razorpay_order_id' : response.get('razorpay_order_id'),
        'razorpay_signature' : response.get('razorpay_signature')
    }
    # print("response.get('razorpay_payment_id')=====",response.get('razorpay_payment_id'))
    # print("response.get('razorpay_order_id')=====",response.get('razorpay_order_id'))
    # print("response.get('razorpay_signature')=====",response.get('razorpay_signature'))
    #
    #
    # # VERIFYING SIGNATURE
    # print(response.get('order_amount'))
    # print(response.get('order_receipt'))

    # try:
    status = client.utility.verify_payment_signature(params_dict)
    print("status======",status)
    # order = Order.objects.get(order_num=order,complete=False)

    order_items =  OrderItem.objects.filter(order=order)

    # order_items.update( date_ordered=datetime.datetime.now())
    transaction = Transaction.objects.create(profile=order.profile,
                    token=params_dict['razorpay_payment_id'],
                    order_id=order.order_num,
                    amount= order.get_cart_total  ,
                    success=True)
    # transaction.save()
    invoice = invoiceModel.objects.get(order_id=order.order_num)
    invoice.transaction_id = Transaction.objects.get(id=transaction.pk)

#             invoice.order_item = postData['referenceId']
    invoice.success = True

    for item in order_items:
        invoice.order_item.add(item)
        invoice.save()
    invoice.save()
    # try:
    #     ownerbook = ownerShipTable.objects.get(owner= order.profile)
    #     for item in order_items:
    #         ownerbook.books.add(item.product)
    #         ownerbook.save()
    # except:
    #     ownerbook = ownerShipTable.objects.create(owner= order.profile)
    #     for item in order_items:
    #         ownerbook.books.add(item.product)
    #         ownerbook.save()
    order.complete=True
    order.save()

    # html = '''<h1 align="center">PyFPDF HTML Demo</h1>
    #   <p>This is regular text</p>
    #      <p>You can also <b>bold</b>, <i>italicize</i> or <u>underline</u>
    #      '''
    #
    # newTh = str(datetime.datetime.now())
    # newTech = str(params_dict['razorpay_payment_id'])
    # data = [['Transaction Reference Code', newTech],
    # ['Order Date', str(invoice.created)],
    #
    # ['Order Number', str(invoice.order_item)],
    # ['Amount',str(order.get_cart_total)],
    # ['Invoice Date', newTh],
    # ]
    #
    # spacing=3
    # pdf = FPDF()
    # pdf.set_font("Arial", size=12)
    # pdf.add_page()
    # pdf.image('https://sli-sp.s3.amazonaws.com/SLI/static/assets1/images/logo1/logo3.png', x=70, y=8, w=80)
    #
    # pdf.ln(75)
    # pdf.cell(20, 10, txt="This is to verify that you have placed an order with us. Please visit your profile for a full receipt.", ln=1, align="L")
    #
    # pdf.ln(10)
    # col_width = pdf.w / 2.2
    # row_height = pdf.font_size
    # for row in data:
    #     for item in row:
    #         pdf.cell(col_width, row_height*spacing,
    #                  txt=item, border=1)
    #     pdf.ln(row_height*spacing)
    # pdf.ln(6)
    #
    # pdf.cell(20, 10, txt="Regards,", ln=1, align="L")
    #
    # pdf.cell(40, 10, txt="Souvenir Publishers Pvt Ltd", ln=1, align="L")
    # abcd = ('invoice/{0}.pdf'.format(newTech))
    # print(abcd)
    # #abcd = 'static/{0}.pdf'.format(newTech)
    # pdf.output(abcd)
    # sg = sendgrid.SendGridClient('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')
    # print("INVOICE ID")
    # print(invoice.id)
    email_to = invoice.email
    print(email_to)
    items2= '<p>'+'User details and order details are given below:-'+'<br>'+'Name: '+ invoice.owner.user.first_name + ' ' + invoice.owner.user.last_name + '<br>' + 'Email: '+email_to + '<br>' +'Phone Number: '+request.user.profile.phone_number +'</p>'
    items2 +='<ul>'

    for i in order_items:
        items2 += '<li>' + str(i) +' - ' + str(i.quantity)+'                                    Amount- ' +str(i.get_total) + '</li>'

    items2 += '</ul>'

    print(items2)
    message = sendgrid.Mail()
    message.add_to([email_to])

    message.set_subject('Order Confirmed -' + str(invoice.order_item))
    message.set_html('Thank you for choosing Sayra. We sincerely appreciate getting to work with you. Help us serve you better with your valuable feedback. ')
    message.set_text(' ')
    message.set_from('info.digisahay@gmail.com')
    # message.add_attachment(file_= abcd, name="Invoice.pdf")
    status, msg = sg.send(message)
    #
    # print(status)
    # print(msg)
    #
    #
    # message_2 = sendgrid.Mail()
    # message_2.add_to(['vasu@dreambox.cloud'])
    #
    # message_2.set_subject('Order Confirmed-'+str(invoice.order_item))
    # message_2.set_html(items2)
    # message_2.set_text(' ')
    # message_2.set_from('info@souvenirpublisher.in')
    # message_2.add_attachment(file_= abcd, name="Invoice.pdf")
    # status, msg = sg.send(message_2)
    return render(request, 'Thankyou.html', {'status': 'Payment Successful','order':order,'amount':order.get_cart_total,'referenceId':newTech})






def wishlists(request,id):
    profile = UserProfile.objects.get(user=request.user)
    prod = product.objects.get(id=id)

    if Wishlist.objects.filter(wished_item=prod,user=profile).exists() :
        print("hello")
        wish = Wishlist.objects.filter(wished_item=prod,user=profile).delete()
    else:
        wish = Wishlist.objects.create(wished_item=prod,user=profile)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def addtocart(request):
    if request.method == 'POST':
        product_id = request.POST.get('productval')
        quantity = request.POST.get('quant')
        prod = product.objects.get(id=product_id)
        order, created = Order.objects.get_or_create(profile=request.user.profile, complete=False)
        if not order.order_num:
            order.order_num = generate_order_id()
        order.save()
        if OrderItem.objects.filter(order=order, product=prod).exists():
            return HttpResponse(status=404)
        OrderItem.objects.create(order=order, product=prod, quantity=quantity, tax_amount=prod.tax_amount,
                                 unit_price=prod.unit_price, discount_percentage=prod.discount_percent)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def removefromcart(request):
    if request.method == 'POST':

        device = request.COOKIES['device']
        productId = request.POST.get('productval')
        varientId = request.POST.get('varientval')
        quantity = request.POST.get('quant')

        try:
            Variant = Variants.objects.get(id=varientId)
            Product = product.objects.get(id=productId)
        except:
            Product = product.objects.get(id=productId)

        if request.user.is_authenticated:
            profile = UserProfile.objects.get(user=request.user)
            order = Order.objects.get(profile=profile,complete=False)
        else:
            order = Order.objects.get(device=device,complete=False)
        if varientId is None:
            orderItem = OrderItem.objects.get(order=order,product=Product,variant=None)
        else:
            orderItem = OrderItem.objects.get(order=order,product=Product,variant=Variant)

        orderItem.quantity-=int(quantity)
        orderItem.save()
        #     try:
        #         orderItem = OrderItem.objects.get()
        #     print("hello Add to cart")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def deletefromcart(request,id):
    orderItem = OrderItem.objects.get(id=id)

    orderItem.delete()
        # orderItem.save()
        #     try:
        #         orderItem = OrderItem.objects.get()
        #     print("hello Add to cart")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

@login_required
def orderlist(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except:
        profile= None
    try:
        device = request.COOKIES['device']
        try:
            order = Order.objects.get(device=device,complete=False)
        except:
            order = Order.objects.get(profile=profile,complete=False)
        if not order.device:
            order.device = device
        if not order.order_num:
            order.order_num = generate_order_id()
        order.save()
    except:
        order = None
    # print(order.order_num,order)
    Category = category.objects.all()
    subcate = subcategory.objects.all()


    user_order_list = Order.objects.filter(profile=profile, complete=True)

    deliver = Delivery.objects.all()
    context = {
    'Category':Category,
    'sub':subcate,
    'new_profile':profile,

    'user_order_list': user_order_list,
    'deliver':deliver
    }
    return render(request, 'userorder.html',context)

