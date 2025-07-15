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

]