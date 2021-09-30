from django.shortcuts import render, redirect
from .models import *
from account.models import *
from shop.models import *
from . utils import cookieCart, cartData, guestOrder

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


from django.urls import reverse_lazy
from django.views import generic

import math
from django.core.mail import send_mail
from django.contrib.auth.models import User, Group


# import souvenir.settings as sett,BASE_DIR
# from .paytm import generate_checksum, verify_checksum

import json

from datetime import date
import random


import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
# from django.db.models.signals import m2m_changed



from django.utils.text import slugify
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.contrib.auth import authenticate, user_logged_in
from django.core.mail import send_mail as sm
from django.conf import settings

#html email required
from django.core.mail  import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.exceptions import ObjectDoesNotExist

from django.db.models.signals import m2m_changed
def toppings_changed(sender, instance,action,**kwargs):
    # print(action)
    if action == 'post_add':
        print("-------- in generate meta")
        instance.meta = instance.ProductName.replace(',',' ')
        for items in instance.SubcatName.all():
            instance.meta += ' ' + items.name+' '
            instance.save()

        for items in instance.CategoryName.all():
            instance.meta += ' ' +items.CategoryName
            instance.save()

        print('slug==================',instance.meta)
        # instance.title_name.first().book_name + " " + instance.title_name.first().book_publisher.first().publisher_name + " " + instance.title_class.first().class_name

        instance.slug = instance.ProductName.replace(' ','-').lower().replace("'",'').replace('.','').replace('(','-').replace(')','-').replace('/','-').replace(',','-')
        # for items in instance.SubcatName.all():
        #     instance.slug += '-' + items.name.replace(' ','-').lower().replace("'",'').replace('.','').replace('(','-').replace(')','-').replace('/','-').replace(',','-')
        #     # print('instance.slug==',instance.slug)
        # for items in instance.CategoryName.all():
        #     instance.slug += '-' +items.CategoryName.replace(' ','-').lower().replace("'",'').replace('.','').replace('(','-').replace(')','-').replace('/','-').replace(',','-')
            # print('instance.slug==================',instance.slug)
        instance.slug = instance.slug.replace('--','-')
         # instance.title_name.first().book_publisher.first().publisher_name.replace(' ','-').lower() + "-" + instance.title_class.first().class_name.replace(' ','-').lower()
        instance.save()
    elif action == 'post_remove':
        print("-------- in generate meta")
        instance.meta = instance.ProductName.replace(',',' ')
        for items in instance.SubcatName.all():
            instance.meta += ' ' + items.name+' '
            instance.save()

        for items in instance.CategoryName.all():
            instance.meta += ' ' +items.CategoryName
            instance.save()

        print('slug==================',instance.meta)
        # instance.title_name.first().book_name + " " + instance.title_name.first().book_publisher.first().publisher_name + " " + instance.title_class.first().class_name

        instance.slug = instance.ProductName.replace(' ','-').lower().replace("'",'').replace('.','').replace('(','-').replace(')','-').replace('/','-').replace(',','-')
        # for items in instance.SubcatName.all():
        #     instance.slug += '-' + items.name.replace(' ','-').lower().replace("'",'').replace('.','').replace('(','-').replace(')','-').replace('/','-').replace(',','-')
        #     # print('instance.slug==',instance.slug)
        # for items in instance.CategoryName.all():
        #     instance.slug += '-' +items.CategoryName.replace(' ','-').lower().replace("'",'').replace('.','').replace('(','-').replace(')','-').replace('/','-').replace(',','-')
            # print('instance.slug==================',instance.slug)
        instance.slug = instance.slug.replace('--','-')
         # instance.title_name.first().book_publisher.first().publisher_name.replace(' ','-').lower() + "-" + instance.title_class.first().class_name.replace(' ','-').lower()
        instance.save()
        # print("nooooooooooo")
    else:
        pass
# m2m_changed.connect(toppings_changed, sender=titleMaster.title_class.through)
m2m_changed.connect(toppings_changed, sender=product.SubcatName.through)




def generate_order_id():
    date_str = "SAY"+date.today().strftime('%Y%m%d')[2:] + str(datetime.datetime.now().second)
    # print(date_str)
    rand_str = "".join([random.choice(string.digits) for count in range(3)])
    # print(rand_str)
    return date_str + rand_str


def getList(dict):
    return dict.keys()


# def hello(request):
#     print("yes")
#
#     return response

@receiver(user_logged_in)
def adding_cart(sender, user, request, **kwargs):
    try:
        device = request.COOKIES['device']
        try:
            order = Order.objects.get(device=device,complete=False)
        except:
            order = Order.objects.get(profile=request.user.profile.first(),complete=False)
        if not order.device:
            order.device = device
        if not order.order_num:
            order.order_num = generate_order_id()
        order.save()
    except:
        try:
            device = request.COOKIES['device']

            if request.user.is_authenticated:
                order = Order.objects.create(profile=request.user.profile.first(),device=device,complete=False)
                if not order.order_num:
                    order.order_num = generate_order_id()
            else:
                order = Order.objects.create(device=device,complete=False)
                if not order.order_num:
                    order.order_num = generate_order_id()
            order.save()
        except :
            pass


    try:
        anonyOrder = Order.objects.get(device = device, complete=False)
        logedOrder = Order.objects.get(profile = request.user.profile.first(), complete=False)
        anony = OrderItem.objects.filter(order = anonyOrder)
        loged = OrderItem.objects.filter(order = logedOrder)

        for i in anony:
            for j in loged:
                if i.product == j.product:
                    if i.variant == j.variant:
                        j.quantity += i.quantity
                        logedOrder.device = device
                        j.save()
                        logedOrder.save()
                        i.delete()
                        anonyOrder.delete()
                else:
                    j.quantity += i.quantity
                    logedOrder.device = device
                    i.delete()
                    anonyOrder.delete()
                    j.save()
                    logedOrder.save()
    except:
        pass


def index(request):
    profile = None
    order = None
    wish = []
    if request.user.is_authenticated:
        profile = request.user.profile
        wishing = Wishlist.objects.filter(user=profile)
        for item in wishing:
            wish.append(item.wished_item.id)
        try:
            order = Order.objects.get(profile=profile, complete=False)
        except ObjectDoesNotExist:
            order = None
    first_banners = Widgets.objects.get(priority=1).banner_set.all().order_by('priority')
    second_banners = Widgets.objects.get(priority=2).banner_set.all().order_by('priority')
    category = Category.objects.all()
    feature = FeaturedItem.objects.all().order_by('-id')
    best_seller = bestseller.objects.all().order_by('-id')
    context = {'first_banners': first_banners,
               'second_banners': second_banners,
               'Category': category,
               'order': order,
               'feature': feature,
               'best_seller': best_seller,
               'wish': wish,
               'profile': profile
               }
    return render(request,'index.html',context)


def category_page(request, slug):
    profile = None
    order = None
    wish = []
    wishing = []
    if request.user.is_authenticated:
        profile = request.user.profile
        wishing = Wishlist.objects.filter(user=profile)
        for item in wishing:
            wish.append(item.wished_item.id)
        try:
            order = Order.objects.get(profile=profile, complete=False)
        except ObjectDoesNotExist:
            order = None
    category = Category.objects.all()
    Prod = product.objects.filter(CategoryName__slug=slug)

    context = {
        'Category':category,
        'wishing':wishing,
        'wish':wish,
        'Product':Prod,
        'order': order,
        'sluging':slug,
        'profile':profile
    }
    return render(request,'category.html',context)

def visitor_ip_address(request):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def product_page(request, slug):
    category = Category.objects.all()
    profile = None
    order = None
    in_bag = False
    is_fav = False
    try:
        prod = product.objects.get(slug=slug)
    except ObjectDoesNotExist:
        return HttpResponse(status=404)
    if request.user.is_authenticated:
        profile = request.user.profile
        is_fav = Wishlist.objects.filter(user=profile, wished_item=prod).exists()
        try:
            order = Order.objects.get(profile=profile, complete=False)
            in_bag = OrderItem.objects.filter(order=order, product=prod).exists()
        except ObjectDoesNotExist:
            pass

    context = {
               'product': prod,
               'Category': category,
               'order': order,
               'in_bag':in_bag,
               'profile': profile,
               'wish': is_fav, 'similar_product': SimilarProduct.objects.filter(prod=prod)
               }
    if request.method == 'POST': #if we select color
        Product = request.POST.get('productId')
        # print(Product)
        size_id = request.POST.get('size')
        color_id = request.POST.get('color')
        variantId = request.POST.get('variantId')
        wish=[]

        wishing = Wishlist.objects.filter(user=profile)
        for item in wishing:
            wish.append(item.wished_item.id)
        try:
            variant = Variants.objects.get(id=variantId,product__id=Product,color__id=color_id ,size__id=size_id) #selected product by click color radio
        except:
            try:
                variant = Variants.objects.get(id=variantId,product__id=Product ) #selected product by click color radio
            except:
                pass
        return redirect('home:product', slug=variant.slug )
        # colors = Variants.objects.filter(product_id=id,size_id=variant.size_id )
        # sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',[id])
        # query += variant.title+' Size:' +str(variant.size) +' Color:' +str(variant.color)
        # else:
        #     pass
            # variant = Variants.objects.filter(product=Product).first()
            # print('variants[0]==',variant)
            # colors = Variants.objects.filter(product_id=id,size_id=variants[0].size_id )
            # sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',[id])
    #         variant =Variants.objects.get(id=variants[0].id)
    # context = {
    # 'Category':Category,
    # 'sub':subcate
    # }

        context.update({
        # 'sizes': sizes,
        # 'colors': colors,
        'variant': variant,
        'order': order,
        'profile':profile,
        'wish':wish
        })
    return render(request,'product.html',context)

def ajaxsize(request):
    data = {}
    if request.POST.get('action') == 'post':
        size = request.POST.get('size')
        # print("10===",color_id)
        productid = request.POST.get('product')
        print("20===",productid)
        variant =  Variants.objects.get(product__id=productid, size__id=size)
        variantscol = Variants.objects.filter(product=variant.product, size__id=size)
        context = {
            'size': size,
            'productid': productid,
            'variant':variant,
            'variantscol': variantscol,
        }
        data = {'rendered_table': render_to_string('color.html', context=context)}
        # print("1---------------------")
        # print(data)
        return JsonResponse(data)

    # print("0---------------------")
    # print(data)
    return JsonResponse(data)


def contactus(request):
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
    if request.method == 'POST':
        name= request.POST.get('name')
        email= request.POST.get('email')
        subject= request.POST.get('subject')
        message= request.POST.get('message')

        contact = Contactus.object.create(name=name,email=email,subject=subject,message=message)

        message_1 = f'User details are given below:-'+'\n'+'Name: '+ name + '\n' + 'Email: '+email + '\n' +  '\n' +'Subject: '+subject+'\n' +'Message: '+message
        # form.save()
        # print(name,email,phone,message_1)

        html_content_receive = render_to_string("contact_template_receive.html",{'name':name,'email':email,'subject':subject,'message':message})

        mailing= EmailMultiAlternatives(
        subject,
        message_1,
        settings.EMAIL_HOST_USER,
        ['info.digisahay@gmail.com'],
        )
        mailing.attach_alternative(html_content_receive,"text/html")
        mailing.send()
        # print(mailing)
        html_content_send = render_to_string("contact_template_send.html",{'name':name})

        mailing1= EmailMultiAlternatives(
        subject,
        message_1,
        settings.EMAIL_HOST_USER,
        [email],
        )
        mailing1.attach_alternative(html_content_send,"text/html")
        mailing1.send()
        return redirect('home:index')
    category = Category.objects.all()
    subcate = subcategory.objects.all()
    context = {
    'Category':category,
    'sub':subcate,
    'order':order,
    'profile':profile
    }
    return render(request,'contactus.html',context)

@login_required
def wishlistPage(request):
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
    wish = Wishlist.objects.filter(user=profile)
    category = Category.objects.all()
    subcate = subcategory.objects.all()
    context = {
    'Category':category,
    'sub':subcate,
    'order':order,
    'profile':profile,
    'wish':wish
    }
    return render(request,'wishlist.html',context)
