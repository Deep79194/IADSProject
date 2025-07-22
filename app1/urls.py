from django.urls import path
from app1 import views
    
    
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('shop/', views.shop, name='shop'),
    path('cart/', views.cart, name='cart'),

        # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgotpwd, name='forgotpwd'),
    path('contact/', views.contact_view, name='contact'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('my-account/', views.account, name='account'),
    path('password-change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('search/', views.product_search_page, name='product_search_page'),
    path('search/ajax/', views.product_search_ajax, name='product_search_ajax'),
    #checkout functionality
    path('checkout/', views.checkout_view, name='checkout'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path("news/", views.eco_news, name="eco_news"),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('reset-password-confirm/', views.reset_password_confirm, name='reset_password_confirm'),


]