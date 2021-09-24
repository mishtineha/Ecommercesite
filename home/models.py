from django.db import models
from django.forms import ModelForm

# Create your models here.
# from ckeditor_uploader.widgets import CKEditorWidget, CKEditorUploadingWidget
from ckeditor_uploader.fields import RichTextUploadingField


from ckeditor.fields import RichTextField


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from datetime import date
import django_filters

from django.dispatch import receiver
# from allauth.account.signals import user_signed_up
from django.db.models.signals import m2m_changed
from django.utils.text import slugify
# from .views import *
from django.db.models.signals import pre_save
from django.core.validators import MinValueValidator,MaxValueValidator

from account.models import *
from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField



class subcategory(models.Model):
    # avatar = models.ImageField(upload_to='avatars/',blank=True, null=True)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=False,default=" ", blank=False,verbose_name="Sub-category Name")
    subparent = models.ForeignKey('self', null=True, on_delete=models.CASCADE, blank=True,related_name="parent_sub",verbose_name="Parent")
    # tags = models.CharField(max_length=200, null=False,default=" ", blank=False,verbose_name="Men/Women/Kid")
    slug = models.SlugField(max_length=55, blank=True, null=True)

    def get_slug(self):

        slug = self.name
        return slugify(slug)

    def save(self, *args, **kwargs):
        self.slug = self.get_slug()
        super(subcategory, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name) +"-"+ str(self.subcat.first().CategoryName)


class Category(models.Model):
    Name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_slug(self):
        slug = self.Name
        return slugify(slug)

    def save(self, *args, **kwargs):
        self.slug = self.get_slug()
        super(Category, self).save(*args, **kwargs)


class product(models.Model):
    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),

    )
    id = models.AutoField(primary_key=True)
    ProductName = models.CharField(max_length=200, null=False,default=" ", blank=False,verbose_name="Product Name")
    CategoryName = models.ManyToManyField(Category,related_name='procat', blank=False,verbose_name="Category Name")
    SubcatName = models.ManyToManyField(subcategory,related_name='prosubcat', blank=False,verbose_name="Sub-category Name")
    short_description = RichTextUploadingField(blank= True,verbose_name="Short Description")
    description = RichTextUploadingField(blank= False,verbose_name="Description")
    additional_info = RichTextUploadingField(blank= True, verbose_name="Additional Information")
    variant = models.CharField(max_length=10,choices=VARIANTS, default='None')
    price = models.IntegerField(default=100, null=True, blank=True, verbose_name='MRP')
    discount_price = models.IntegerField(default=0, null=True, blank=True, verbose_name='Discount Price')
    discount_percent = models.IntegerField(default=0, null=True, blank=True, verbose_name='Discount Percentage')
    gst = models.IntegerField(default=0, null=True, blank=True,verbose_name='GST')
    tax_amount = models.DecimalField(default=0, null=True, blank=True, max_digits=8 ,decimal_places=2,verbose_name='Tax Amount')
    unit_price = models.DecimalField(default=0, null=True, blank=True, max_digits=8 ,decimal_places=2,verbose_name='Unit Price(without GST)')
    quantity = models.IntegerField(default=10,blank=True,verbose_name='Quantity in Stock')
    flipkart = models.CharField(max_length=200, null=True, blank=True,verbose_name="Flipkart Link")
    amazon = models.CharField(max_length=200, null=True, blank=True,verbose_name="Amazon Link")
    meta = models.CharField(max_length=100000,default="",null=True,blank=True)
    slug = models.SlugField(max_length=500, blank=True, null=True)


    # @receiver(post_save, sender=product)
    def get_slug(self):
        slug = self.ProductName.replace(',','-')

        return slugify(slug)



    # @receiver(post_save, sender=product, slug_uid="slug")
    # def update_stock(sender, instance, **kwargs):
    #     instance.product.stock -= instance.amount
    #     instance.product.save()
    def per_cal(self):

        dis= self.discount_percent
        price = self.price
        per = price-(price*(dis/100))
        # dis_per = 100 - per
        self.discount_price = int(per)
        # print(self.discount_price)
        return(self.discount_price)

    def dic_amt(self):
        dis= self.discount_price
        price = self.price
        if self.discount_percent > 0 :
            amt = dis - price
        else:
            amt = 0
        return amt

    def gst_cal(self):
        gstcal = self.gst
        price = self.price
        dis= self.per_cal()
        if self.discount_percent > 0 :
            tax = dis*(gstcal/100)
        else:
            tax = price*(gstcal/100)
        return(tax)

    def unit_cal(self):
        price = self.price
        dis= self.per_cal()
        gstcal = self.gst_cal()
        if self.discount_percent > 0 :
            unit = dis-gstcal
        else:
            unit = price-gstcal
        return(unit)

    def save(self, *args, **kwargs):
        self.discount_price=self.per_cal()
        self.tax_amount = self.gst_cal()
        self.unit_price = self.unit_cal()
        meta_save = self.ProductName.replace(',',' ')
        # for items in self.SubcatName.all():
        #     meta_save += ' ' + items.name+' '
        #     print('slug==',meta_save )
        # for items in self.CategoryName.all():
        #     meta_save += ' ' +items.CategoryName
        print('slug==================',self.meta)
        self.meta = meta_save
        self.slug = self.get_slug()
        super(product, self).save(*args, **kwargs)


    def __str__(self):
        return self.ProductName + str(self.id)


class product_images(models.Model):
    id = models.AutoField(primary_key=True)
    Product = models.ForeignKey(product, on_delete=models.CASCADE, related_name='productimages',blank=False,null=True)
    name = models.CharField(max_length=200, null=False,default="Sayra", blank=False,verbose_name="Product Name")
    image = models.FileField(upload_to="product/",blank=True, null=True, verbose_name='image1(1860 x 1860)')

    def __str__(self):
        return self.name



class Color(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True,null=True)
    def __str__(self):
        return self.name
    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color:{}">Color </p>'.format(self.code))
        else:
            return ""


class Size(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True,null=True)
    def __str__(self):
        return self.name

class Variants(models.Model):
    title = models.CharField(max_length=100, blank=True,null=True)
    product = models.ForeignKey(product, on_delete=models.CASCADE,related_name="var_product")
    color = models.ForeignKey(Color, on_delete=models.CASCADE,related_name='var_color',blank=True,null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE,related_name='var_size',blank=True,null=True)
    image_id = models.ForeignKey(product_images, verbose_name='Product Images', on_delete=models.CASCADE, related_name='variantimages',blank=True,null=True)
    quantity = models.IntegerField(default=10,blank=True,verbose_name='Quantity in Stock')
    short_description = models.TextField(blank= True,verbose_name="Short Description")
    description = models.TextField(blank= False,default="",verbose_name="Description")
    additional_info = models.TextField(blank= True, verbose_name="Additional Information")
    price = models.IntegerField(default=100, null=True, blank=True, verbose_name='MRP')
    discount_price = models.IntegerField(default=0, null=True, blank=True, verbose_name='Discount Price')
    discount_percent = models.IntegerField(default=0, null=True, blank=True, verbose_name='Discount Percentage')
    gst = models.IntegerField(default=0, null=True, blank=True,verbose_name='GST')
    tax_amount = models.DecimalField(default=0, null=True, blank=True, max_digits=8 ,decimal_places=2,verbose_name='Tax Amount')
    unit_price = models.DecimalField(default=0, null=True, blank=True, max_digits=8 ,decimal_places=2,verbose_name='Unit Price(without GST)')
    slug = models.SlugField(max_length=500, blank=True, null=True)
    def get_slug(self):
        slug = self.title.replace(',','-')

        return slugify(slug)

    def per_cal(self):

        dis= self.discount_percent
        price = self.price
        per = price-(price*(dis/100))
        # dis_per = 100 - per
        self.discount_price = per
        # print(self.discount_price)
        return(self.discount_price)

    def dic_amt(self):
        dis= self.discount_price
        price = self.price
        if self.discount_percent > 0 :
            amt = dis - price
        else:
            amt = 0
        return amt

    def gst_cal(self):
        gstcal = self.gst
        price = self.price
        dis= self.per_cal()
        if self.discount_percent > 0 :
            tax = dis*(gstcal/100)
        else:
            tax = price*(gstcal/100)
        return(tax)

    def unit_cal(self):
        price = self.price
        dis= self.per_cal()
        gstcal = self.gst_cal()
        if self.discount_percent > 0 :
            unit = dis-gstcal
        else:
            unit = price-gstcal
        return(unit)

    def save(self, *args, **kwargs):
        self.discount_price=self.per_cal()
        self.tax_amount = self.gst_cal()
        self.unit_price = self.unit_cal()
        self.slug = self.get_slug()
        abc = Variants.objects.all().last()
        self.slug += '-'+ str(abc.id + 1 )
        super(Variants, self).save(*args, **kwargs)


    def __str__(self):
        return self.title

    def image(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
             varimage=img.image.url
        else:
            varimage=""
        return varimage

    def image_tag(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
             return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
        else:
            return ""


class ProductFilter(django_filters.FilterSet):
    Category = django_filters.ModelMultipleChoiceFilter(
        field_name = 'CategoryName__CategoryName',

        to_field_name='CategoryName',
        #
        queryset=Category.objects.all(),
    # widget = forms.CheckboxSelectMultiple
    )

    Sub_category = django_filters.ModelMultipleChoiceFilter(
        field_name='SubcatName__name',

        to_field_name='name',
        #
        queryset=subcategory.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )




    class Meta:
        model = product
        fields = ['Category', 'Sub_category']

class Comment(models.Model):
    product= models.ForeignKey(product,on_delete=models.CASCADE,related_name='Comments',null=True, verbose_name='Product')
    user_id= models.ForeignKey(UserProfile,on_delete=models.CASCADE, verbose_name='User Id', null= True, blank= True, related_name='comment_user')
    name = models.CharField(max_length=100,null=True,blank=True)
    subject = models.CharField(max_length=100,null=True,blank=True)
    # ip = models.CharField(max_length=40)
    rate = models.IntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(5)],null=True,blank=True)
    comment = models.TextField(verbose_name='Comment',null=True,blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ( 'name','subject','comment' )

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'pl-4 pr-4 mr-4 ml-4 form-control form-control-alternative form-control-md ml-auto mr-auto'
            visible.field.widget.attrs['stlye'] = 'width:95%'


class Contactus(models.Model):
    name = models.CharField(max_length=200, blank=True, verbose_name='Name')
    # models.ForeignKey(UserProfile, on_delete=models.SET_NULL, related_name="order_profile", null= True, blank= True)
    email = models.CharField(max_length=200, blank=True, verbose_name='Email')
    subject = models.CharField(max_length=300, blank=True, verbose_name='Subject')
    message = models.TextField(max_length=200, blank=True, verbose_name='Message')

    def __str__(self):
        return self.name

class contactUsForm(ModelForm):
    class Meta:
        model = Contactus
        fields = [ 'name', 'email', 'subject', 'message']

class bestseller(models.Model):
    product = models.ForeignKey(product,on_delete=models.CASCADE,related_name='bestseller_product',null=True, verbose_name='Product')
    slug = models.SlugField(max_length=500, blank=True, null=True)

    def get_slug(self):
        slug = self.product.ProductName.replace(',','-')
        return slugify(slug)

    def save(self, *args, **kwargs):
        self.slug = self.get_slug()
        super(bestseller, self).save(*args, **kwargs)


    def __str__(self):
        return self.product.ProductName


class FeaturedItem(models.Model):
    product = models.ForeignKey(product,on_delete=models.CASCADE,related_name='featured_product',null=True, verbose_name='Product')
    slug = models.SlugField(max_length=500, blank=True, null=True)

    def get_slug(self):
        slug = self.product.ProductName.replace(',','-')
        return slugify(slug)

    def save(self, *args, **kwargs):
        self.slug = self.get_slug()
        super(FeaturedItem, self).save(*args, **kwargs)


    def __str__(self):
        return self.product.ProductName


class Widgets(models.Model):
    name = models.CharField(max_length=100)
    priority = models.IntegerField()
    image_size = models.CharField(max_length=100,default='1920 x 650')


class Banner(models.Model):
    image = models.FileField(upload_to="banner/", verbose_name="Banner 1(1920 x 650)",null=True)
    redirect_url = models.URLField(null=True)
    widget = models.ForeignKey(Widgets, on_delete=models.CASCADE, null=True)
    priority = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'banner'


class SimilarProduct(models.Model):
    prod = models.ForeignKey(product, on_delete=models.CASCADE, related_name='similar_product')
    # prod_slug = models.CharField(max_length=100)
    # similar_prod_slug = models.CharField(max_length=100)
    similar_prod = models.ForeignKey(product, on_delete=models.CASCADE)
