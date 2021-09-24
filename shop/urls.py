from django.urls import path
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

app_name = 'shop'

urlpatterns = [
    path('cart',views.cart,name='cart'),
    path('checkout',views.checkout,name='checkout'),

    path('wishlists/<int:id>',views.wishlists,name='wishlists'),
    path('add-to-cart',views.addtocart,name='addtocart'),
    path('delete-from-cart/<int:id>',views.deletefromcart,name='deletefromcart'),
    path('Checkout-Page-Details/', views.checkoutDetails, name='checkoutDetails'),



    path('Check-Response/', views.check_response, name='check_response'),

    # path('invoice123',views.invoice_check,name='invoice_check'),
    # path('invoice',views.invoice_check1,name='invoice_check1')


    url(r'^order-summary/$', views.orderlist, name="order_summary"),
    # url(r'^success/$', views.success, name='purchase_success'),
    # url(r'^update-transaction/(?P<token>[-\w]+)/$', views.update_transaction_records,name='update_records'),

]
