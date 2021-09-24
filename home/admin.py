from django.contrib import admin
from django.forms import CheckboxSelectMultiple

# Register your models here.

from django.db import models
# from django.contrib import admin

from .models import *

from . models import *
import admin_thumbnails

from import_export.admin import ImportExportModelAdmin

#

@admin_thumbnails.thumbnail('image1')
class ProductImageInline(admin.TabularInline):
    model = product_images
    readonly_fields = ('id',)
    extra = 1

#
class ProductVariantsInline(admin.TabularInline):
    model = Variants
    readonly_fields = ('discount_price','slug')
    extra = 1
    show_change_link = True

@admin.register(Variants)
class VariantsAdmin(admin.ModelAdmin):
    list_display = ['title','price','discount_price','discount_percent','slug']
#
#
#
@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name','code','color_tag']

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name','code']
#
# @admin.register(Weight)
# class WeightAdmin(admin.ModelAdmin):
#     list_display = ['name','code']
#
@admin.register(product)
class product(admin.ModelAdmin):
    list_display = ['ProductName','price','discount_price','discount_percent','slug']
    search_fields = ('ProductName','price','discount_price','discount_percent')
    readonly_fields = ('discount_price','slug')
    inlines = [ProductImageInline,ProductVariantsInline]
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }




























@admin.register(subcategory)
class subcategory(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    # list_filter = ('name',)
    # date_hierarchy = 'publication_date'
    # ordering = ('-id',)

@admin.register(Category)
class category(admin.ModelAdmin):
    list_display = ['id', 'Name']
    # list_display = ['CategoryName','Sub_category','parent', 'slug']
    # search_fields = ('CategoryName', 'SubcatName')
    # # fields = ['CategoryName', 'SubcatName','slug']
    # formfield_overrides = {
    #     models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    # }
    # search_fields = ['CategoryName','SubcatName__name']




# @admin.register(product)
# class product(admin.ModelAdmin):
#     list_display = ['ProductName','price','discount_price','discount_percent','quantity','gst','flipkart','amazon','tax_amount','unit_price']
#     search_fields = ('ProductName','price','discount_price','quantity','discount_percent','gst','flipkart','amazon','tax_amount','unit_price','slug')
#     formfield_overrides = {
#         models.ManyToManyField: {'widget': CheckboxSelectMultiple},
#     }

@admin.register(product_images)
class product_images(admin.ModelAdmin):
    list_display = ['name','image']
    # search_fields = ('name','image1','image2','image3','image4')
    # list_filter= ('name','image1','image2','image3','image4')
    # formfield_overrides = {
    #     models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    # }

# @admin.register(Comment)
# class Comment(admin.ModelAdmin):
#     list_display = ['product','user_id','name','comment','create_at','update_at']
#     fields = ['product','user_id','name','comment','create_at','update_at']
#     search_fields = ('product','user_id','name','comment','create_at','update_at')
#     formfield_overrides = {
#         models.ManyToManyField: {'widget': CheckboxSelectMultiple},
#     }
#     readonly_fields = ['create_at','update_at']

@admin.register(Contactus)
class Contactus(admin.ModelAdmin):
    list_display = ['name','email','subject','message']
    search_fields = ('name','email','subject','message')
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

@admin.register(bestseller)
class bestseller(admin.ModelAdmin):
    list_display = ['product','slug']
    search_fields = ('product__ProductName','slug')


@admin.register(FeaturedItem)
class FeaturedItem(admin.ModelAdmin):
    list_display = ['product','slug']
    search_fields = ('product__ProductName','slug')


# class banner_mainInline(admin.TabularInline):
#     model = banner_main
#
#
# class bannerAdmin(admin.ModelAdmin):
#     list_display = ['name']
#     inlines = [banner_mainInline]
#
#
# admin.site.register(banner, bannerAdmin)

#NEHA
@admin.register(Widgets)
class banner(admin.ModelAdmin):
    list_display = ['name','priority','image_size']
@admin.register(Banner)
class banner(admin.ModelAdmin):
    list_display = ['image','redirect_url','widget']
#     list_display = ['name','banner1','b1_url','banner2','b2_url','banner3','b3_url','banner4','b4_url','banner5','b5_url']
#     search_fields = ('name','banner1','b1_url','banner2','b2_url','banner3','b3_url','banner4','b4_url','banner5','b5_url')

# @admin.register(SimilarProduct)
# class SimilarProduct(SimilarProduct):
#     list_display = ['product', 'product_slug', 'similar_product_slug']

@admin.register(SimilarProduct)
class SimilarProduct(admin.ModelAdmin):
    list_display = ['prod','similar_prod']
