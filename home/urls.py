from django.urls import path
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<slug:slug>',views.category_page,name='category'),
    path('product/<slug:slug>',views.product_page,name='product'),
    # path('update_item/', views.updateItem, name="update_item"),
    path('ajaxsize/', views.ajaxsize, name='ajaxsize'),
    path('contact-us',views.contactus,name='contactus'),
    path('wishlist',views.wishlistPage,name='wishlistPage'),
    

    # path('order-list',views.orderlist,name='orderlist'),
    # path('invoice-details/<str:book>/', views.invoice_details_user, name='invoice_details_user'),
    # path('thankyou',views.thankyou,name='thankyou'),

]
