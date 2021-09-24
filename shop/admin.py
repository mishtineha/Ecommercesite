from django.contrib import admin
from django.forms import CheckboxSelectMultiple

# Register your models here.

from django.db import models
# from django.contrib import admin

from .models import *

# Register your models here.




@admin.register(OrderItem)
class OrderItem(admin.ModelAdmin):
    search_fields = ('product__ProductName','variant__title' 'order__order_num','quantity','date_added')
    # fields = ['product', 'order','quantity','date_added']
    list_display = ['product', 'order','variant','quantity','date_added']
    list_filter = ['product', 'order','variant','quantity','date_added']

@admin.register(Order)
class Order(admin.ModelAdmin):
    list_display = ['profile', 'order_num','complete','is_initiated']
    # list_filter = ['profile', 'order_num','complete','is_initiated']
    # fields = ['profile', 'order_num']
    search_fields = ['profile__email', 'order_num']


@admin.register(Transaction)
class Transaction(admin.ModelAdmin):
    list_display = ['profile','token', 'order_id','amount','success','timestamp','checksum']
    # list_filter = ['profile','token', 'order_id','amount','success']
    search_fields = ('profile__email','token', 'order_id','amount','success','timestamp','checksum')


@admin.register(Delivery)
class Delivery(admin.ModelAdmin):
    list_display = ['orderid1','orderIds','orderItem','status','shipped_via','tracking_no','expected_date']
    search_fields = ('orderid1__order_num','order_item__product__ProductName','status','shipped_via','tracking_no','expected_date')


@admin.register(invoiceModel)
class invoiceModel(admin.ModelAdmin):
    list_display = ['owner','order_id','orderitem', 'email','phone_number','transaction_id','gst_number','nameDetail','full_address','address2','city','states','pin_code','billing_address','success','created']
    # list_display = ['owner','order_id', 'sub_category','email','phone_number','transaction_id','nameDetail',,)
    fields = ['owner','order_id', 'order_item','email','phone_number','transaction_id','gst_number','nameDetail','full_address','address2','city','states','pin_code','billing_address','success','created']
    # formfield_overrides = {
    #     models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    # }
    search_fields = ('owner__email','order_id','email','order_item__product__ProductName','phone_number','transaction_id__token','nameDetail','full_address','address2','city','states','pin_code','gst_number','billing_address','success','created')
    readonly_fields = ['created']

@admin.register(Coupon)
class Coupon(admin.ModelAdmin):
    list_display = ['code','valid_from', 'valid_to','discount','discount_percent','active']
    # list_filter = ['profile','token', 'order_id','amount','success']
    search_fields = ('code','profile__email','valid_from', 'valid_to','discount','discount_percent')

@admin.register(Wishlist)
class Wishlist(admin.ModelAdmin):
    list_display = ['user','wished_item', 'added_date','slug']
    # list_filter = ['profile','token', 'order_id','amount','success']
    search_fields = ('user__email','wished_item', 'added_date','slug')
