from django.db import models
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.validators import RegexValidator


class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=40)
    otp = forms.CharField(max_length=40)
    phone_number = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ('name', 'otp','phone_number', 'password1', 'password2')


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, related_name="profile")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    name = models.CharField(max_length=200, null=False,default="None", blank=False,verbose_name="Full Name")
    phone_number = models.CharField(max_length=17, blank=False, unique=True) # validators should be a list
    created = models.DateTimeField(auto_now_add=True, null=True, blank=False)

    def __str__(self):
        if self.user:
            return "{phone_number}".format(phone_number=self.phone_number)
        else:
            return ""


class OTP(models.Model):
    phone_number = models.CharField(max_length=17, blank=False)
    time_st = models.DateTimeField(auto_now=True)
    otp = models.BigIntegerField()
    verified = models.BooleanField(default=False)


class ShippingAdd(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete= models.SET_NULL, null=True, related_name='ship_profile')
    name = models.CharField(max_length=200, null=False,default=" ", blank=False,verbose_name="Full Name")
    email = models.CharField(max_length=200, null=False,default=" ",  blank=False,verbose_name="Email")
    phone_regex = RegexValidator(regex=r'^\d{10}$', message="Phone number must be entered in the format: '9876543210'. Up to 10 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=False) # validators should be a list
    address1 = models.CharField(max_length=30, blank=False, null=True, verbose_name="Address")
    address2 = models.CharField(max_length=100, null=True, default=" ", verbose_name="Address Line 2")
    city = models.CharField(max_length=30, blank=False)
    states = models.CharField(max_length=30, blank=False,  verbose_name="State Name")
    postal_code = models.CharField(max_length=6, blank=False, null=True , verbose_name="Enter PIN Code")
    country = models.CharField(max_length=30, blank=False,  verbose_name="Country Name", default="India")

    def __str__(self):
        return self.email

class shippingForm(ModelForm):

    class Meta:
        model = ShippingAdd
        fields = ( 'name','email','phone_number','address1','city','states', 'postal_code',  'country'   )

    def __init__(self, *args, **kwargs):
        super(shippingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-alternative form-control-md'
