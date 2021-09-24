from django.db import models
from django.forms import ModelForm
from home.models import *
from account.models import *

from ckeditor.fields import RichTextField


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from datetime import date
# import django_filters

from django.dispatch import receiver
# from allauth.account.signals import user_signed_up
from django.db.models.signals import m2m_changed
from django.utils.text import slugify
# from .views import *
from django.db.models.signals import pre_save
import datetime
from datetime import datetime, time, timedelta








#
# class contactUsForm(ModelForm):
#     class Meta:
#         model = customersupportmodel
#         fields = [ 'name', 'email', 'phone', 'message']
#
# class aboutsupportmodel(models.Model):
#     name = models.CharField(max_length=200, blank=True, verbose_name='Name', default='None')
#     email = models.CharField(max_length=200, blank=True, verbose_name='Email', default='None')
#     speciality = models.CharField(max_length=200, blank=True, verbose_name='Speciality', default='None')
#
# class aboutUsForm(ModelForm):
#     class Meta:
#         model = aboutsupportmodel
#         fields = [ 'name', 'email',  'speciality']


class Coupon(models.Model):
    code= models.CharField(max_length=120,unique=True)
    profile = models.ManyToManyField(UserProfile,blank=True, related_name='coupon_user')
    image = models.ImageField(upload_to="Coupon/", blank=True, null=True, verbose_name='image')
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(default=0,blank=True, verbose_name='Coupon Discount Price')
    discount_percent = models.IntegerField(default=0,blank=True, verbose_name='Coupon Discount Percent')
    active = models.BooleanField(default=False)
    slug = models.SlugField(max_length=55, blank=True)

    def __str__(self):
        return str(self.code)

    @property
    def active(self):

        return datetime.now().timestamp() < self.valid_to.timestamp() and datetime.now().timestamp() > self.valid_from.timestamp()
    # @property
    # def change_active(self):
    #     print(datetime.now)
    #     if date.today() > self.valid_to:
    #         self.active = False
    #         self.save()
    #     else:
    #         pass
    #     return self.active

    def get_slug(self):
        slug = self.code

        return slugify(slug)

    def save(self, *args, **kwargs):
        self.slug = self.get_slug()
        super(Coupon, self).save(*args, **kwargs)

# class CouponModelForm(ModelForm):
#
#     class Meta:
#         model = Coupon
#         fields = ( 'code',)
#
#     def __init__(self, *args, **kwargs):
#         super(CouponModelForm, self).__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'form-control form-control-alternative form-control-md'

class shipping_charges(models.Model):
    price = models.IntegerField(default=0, null=True, blank=True, verbose_name='Shipping charges')

    def __str__(self):
        return str(self.price)

class Order(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, related_name="order_profile", null= True, blank= True)
    order_num =  models.CharField(max_length=100, null=True)
    date_ordered = models.DateTimeField(auto_now_add= True)
    shippingcharge = models.ForeignKey(shipping_charges,on_delete=models.SET_NULL, related_name="ship_charge",verbose_name="Shipping Charge", null= True, blank= True)
    complete = models.BooleanField(default=False, null= True, blank= False)
    is_initiated = models.BooleanField(default=False, blank=True, null=True)
    # transaction_id =  models.CharField(max_length=100, null=True)
    device = models.CharField(max_length=100, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL,null=True, related_name="order_coupon", blank= True)

    def __str__(self):
        return str(self.order_num)

    # @property
    # def shipping(self):
    #     shipping= False
    #     orderitems = self.OrderItem.all()
    #     for i in orderitems:
    #         if i.product.digital == False:
    #             shipping = True
    #     return shipping
    @property
    def get_cart(self):
        orderitems = self.OrderItem.all()
        amt = sum([item.get_total for item in orderitems])

        return int(amt)

    @property
    def get_cart_total(self):
        orderitems = self.OrderItem.all()
        amt = sum([item.get_total for item in orderitems])
        if self.coupon:
            if self.coupon.discount > 0:
                total = amt - self.coupon.discount
                # print('dis=====',dis)
            else:
                total = amt - amt*(self.coupon.discount_percent/100)
        else:
            total = amt
        # print(total)
        return int(total)

    @property
    def get_cart_items(self):
        orderitems = self.OrderItem.all()
        total = sum([item.quantity for item in orderitems])

        return total

    @property
    def total_items(self):
        orderitems = self.OrderItem.all()
        total = sum([item for item in orderitems])

        return total

    @property
    def get_cart_ship_total(self):
        orderitems = self.OrderItem.all()
        amt = sum([item.get_total for item in orderitems])
        if self.coupon:
            if self.coupon.discount > 0:
                dis = amt - self.coupon.discount
                # print('dis=====',dis)
            else:
                dis = amt - amt*(self.coupon.discount_percent/100)
        else:
            dis = amt
        # print('================',self.coupon.discount)
        qty =sum([item.quantity for item in orderitems])
        print("newwwwwwwwwwwwww========",self.shippingcharge)
        ship_cost = 0
        total = dis + ship_cost
        #     if qty <= 2:
        # elif qty>2 and qty <=4:
        #     ship_cost = 200
        #     total = dis + ship_cost
        # else:
        #     ship_cost = 300
        #     total = dis + ship_cost
        # print(total)
        return int(total)

    @property
    def get_ship_total(self):
        orderitems = self.OrderItem.all()
        qty =sum([item.quantity for item in orderitems])

        ship_cost = 0
        # if qty <= 2:
        #
        # elif qty>2 and qty <=4:
        #     ship_cost = 200
        #
        # else:
        #     ship_cost = 300


        return ship_cost


class OrderItem(models.Model):
    product = models.ForeignKey(product, on_delete= models.SET_NULL,null=True,related_name="prod_order_item")
    variant = models.ForeignKey(Variants, on_delete=models.SET_NULL,blank=True, null=True,related_name="var_order_item")
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,related_name='OrderItem' , null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    tax_amount = models.DecimalField(default=0, null=True, blank=True, max_digits=8, decimal_places=2,
                                     verbose_name='Tax Amount')
    unit_price = models.DecimalField(default=0, null=True, blank=True, max_digits=8, decimal_places=2,
                                     verbose_name='Unit Price(without GST)')
    discount_percentage = models.DecimalField(default=0, null=True, blank=True, max_digits=8, decimal_places=2)
    total_price = models.DecimalField(default=0, null=True, blank=True, max_digits=8, decimal_places=2)

    def __str__(self):
        return self.product.ProductName

    @property
    def get_prod_total(self):
        if self.product.discount_price == 0:
            total = self.product.price * self.quantity
        else :
            total = self.product.discount_price * self.quantity
        return total

    @property
    def get_vari_total(self):
        # print("================",self)
        try:
            if self.variant.discount_price == 0:
                total = self.variant.price * self.quantity
            else :
                total = self.variant.discount_price * self.quantity
        except:
            total= 0
        return total

    @property
    def get_total(self):
        if self.get_vari_total:
            total = self.get_vari_total
        else:
            total = self.get_prod_total
        # print("total==",total)
        return total

# class ShippingAddress(models.Model):
#     profile = models.ForeignKey(UserProfile, on_delete= models.SET_NULL, null=True)
#     name = models.CharField(max_length=200, null=False,default="None", verbose_name="Full Name")
#     email = models.CharField(max_length=200, null=False,default="None", verbose_name="Email")
#     order = models.ForeignKey(Order, on_delete=models.SET_NULL, related_name='ShippingAddress', null=True)
#     address = models.CharField(max_length=500, null=False)
#     city = models.CharField(max_length=200, null=False)
#     state = models.CharField(max_length=200, null=False)
#     zipcode = models.CharField(max_length=200, null=False)
#     country = models.CharField(max_length=200, null=False)
#     date_added = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.name



class Transaction(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=True)
    token = models.CharField(max_length=120)
    order_id = models.CharField(max_length=120,null=True)
    amount = models.DecimalField(max_digits=65, decimal_places=2,null=True)
    success = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    checksum = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=200,default=None,null=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.timestamp and self.id:
            self.order_id = self.timestamp.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super(Transaction, self).save( *args, **kwargs)

    def __str__(self):
        return self.token

    class Meta:
        ordering = ['-timestamp']



class invoiceModel(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    order_id = models.CharField(max_length=300, null=True, verbose_name="Order ID")
    order_item = models.ManyToManyField(OrderItem, default='Other', related_name='order_items')
    transaction_id = models.OneToOneField(Transaction, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    nameDetail = models.CharField(max_length=30, null=True, verbose_name="Name")
    email = models.CharField(max_length=200, null=False,default="None", blank=False,verbose_name="Email")
    phone_regex = RegexValidator(regex=r'^\d{10}$', message="Phone number must be entered in the format: '9876543210'. Up to 10 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=False) # validators should be a list
    full_address = models.CharField(max_length=300,  null=True, verbose_name="Shipping Address")
    address2 = models.CharField(max_length=300, blank=True,  null=True, verbose_name="Address Line 2 ")
    city = models.CharField(max_length=30, null=True, verbose_name="City")
    states = models.CharField(max_length=30, null=True, verbose_name="State")
    pin_code = models.CharField(max_length=30,  null=True, verbose_name="PIN Code")
    billing_address = models.TextField(  null=True, verbose_name="Billing Address")
    gst_number = models.CharField(max_length=30, blank=True, null=True, verbose_name="GST Number")
    success = models.BooleanField(default=False)

    def __str__(self):
        return str(self.order_id)

    @property
    def check_name(self):
        print("hello")

    def orderitem(self):
        return "\n,".join([p.product.ProductName for p in self.order_item.all()])

class invoiceModelForm(ModelForm):

    class Meta:
        model = invoiceModel
        fields = ( 'nameDetail','email','phone_number','full_address',   'city', 'states', 'pin_code', 'billing_address')

    def __init__(self, *args, **kwargs):
        super(invoiceModelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-alternative form-control-md'




class Delivery(models.Model):
    orderid1= models.OneToOneField(Order, on_delete=models.SET_NULL, null=True, verbose_name="Order Number")
    order_item = models.ManyToManyField(OrderItem, default='Other', related_name='del_order_items')
    orderIds= models.ForeignKey(invoiceModel, on_delete= models.SET_NULL, null=True, verbose_name="Transaction Id")
    status = models.CharField(max_length=256, choices=[('Confirmed Order', 'Confirmed Order'),('Processing Order', 'Processing Order'), ('Quality Check', 'Quality Check'),('Product Dispatched', 'Product Dispatched'),('Product Delivered', 'Product Delivered')], default="Confirmed Order")
    shipped_via = models.CharField(max_length=500, null=False, default="DTDC", verbose_name="Shipped Via")
    tracking_no =models.CharField(max_length=500, default="0", verbose_name="Tracking Number")
    expected_date = models.DateField( verbose_name="Expected Date", default=date.today)
    def __str__(self):
        return str(self.status)

    def orderItem(self):
        return "\n,".join([p.product.ProductName for p in self.order_item.all()])

class Wishlist(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)# here CASCADE is the behavior to adopt when the referenced object(because it is a foreign key) is deleted. it is not specific to django,this is an sql standard.
    wished_item = models.ForeignKey(product,on_delete=models.CASCADE,related_name="wished_product")
    added_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=60,null=True,blank=True)

    def __str__(self):
        return self.wished_item.ProductName

    def get_slug(self):

        slug = self.wished_item.ProductName.replace(',','-')
        return slugify(slug)

    def save(self, *args, **kwargs):
        self.slug = self.get_slug()
        super(Wishlist, self).save(*args, **kwargs)
































# class ecommerce_view(models.Model):
#     books_name = models.ManyToManyField(booksMaster, default='Other', related_name='book_originals')
#     books_class = models.ManyToManyField(classesMaster, verbose_name='Class ', related_name='book_classed')
#     books_publisher = models.ManyToManyField(publisherMasters, verbose_name='Publisher ', related_name='book_publisher')
#
# class ecommerceFilter(django_filters.FilterSet):
#     books_publisher = django_filters.ModelMultipleChoiceFilter(queryset=publisherMasters.objects.all(),
#         widget=forms.CheckboxSelectMultiple)
#
#     # publisher1 = django_filters.ModelMultipleChoiceFilter(queryset=publisherMasters.objects.all(),
#     #     widget=forms.CheckboxSelectMultiple)
#     classes1 = django_filters.ModelMultipleChoiceFilter(queryset=classesMaster.objects.all(),
#         widget=forms.CheckboxSelectMultiple)
#     subjectList1 = django_filters.ModelMultipleChoiceFilter(queryset=subjectsMasters.objects.all(),
#         widget=forms.CheckboxSelectMultiple)
#     class Meta:
#         model = ecommerce_view
#         fields = ['books_publisher', 'classes1', 'subjectList1']
#
# class titlemasterfilter(django_filters.FilterSet):
#     publishers = django_filters.ModelMultipleChoiceFilter(
#         field_name = 'ProductName__book_publisher__publisher_name',
#
#         to_field_name='publisher_name',
#         #
#         queryset=publisherMasters.objects.all(),
#     widget = forms.CheckboxSelectMultiple
#     )
#     subjects = django_filters.ModelMultipleChoiceFilter(
#         field_name='ProductName__book_subject__subject_name',
#
#         to_field_name='subject_name',
#         #
#         queryset=subjectsMasters.objects.all(),
#         widget=forms.CheckboxSelectMultiple
#     )
#     classes = django_filters.ModelMultipleChoiceFilter(
#         field_name='title_class__class_name',
#
#         to_field_name='class_name',
#         #
#         queryset= classesMaster.objects.all(),
#         widget=forms.CheckboxSelectMultiple
#     )
#
#
#
#     class Meta:
#         model = titleMaster
#         fields = ['publishers','subjects','classes']
#         # fields = ['books_publisher']
#         # fields = ['ProductName']
#         # fields = ['ProductName__book_publisher__publisher_name']
