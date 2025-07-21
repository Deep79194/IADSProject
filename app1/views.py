from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from .forms import SimpleSignupForm, UserLoginForm ,UserUpdateForm,BillingAddressForm, ShippingAddressForm # We'll create this next
from .models import ContactSubmission,Product,User, Cart, CartItem, BillingAddress, ShippingAddress, Order, OrderItem
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import PasswordChangeView
from django.db.models import Q
import requests, xml.etree.ElementTree as ET
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .models import Article

# Create your views here.

def home(request):
    welcome_message = request.session.pop('welcome_message', None)
    if welcome_message:
        messages.success(request, welcome_message)
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

# def shop(request):
#     return render(request, 'shop.html')


# def shop(request):
#     products = Product.objects.all()
#     categories = dict(Product.CATEGORY_CHOICES)
#
#     context = {
#         'products': products,
#         'categories': categories,
#     }
#     return render(request, 'shop.html', context)
# def shop(request):
#     category = request.GET.get('category')  # Get the category from URL parameters
#
#     # Get all products or filter by category
#     if category and category in dict(Product.CATEGORY_CHOICES):
#         products = Product.objects.filter(category=category)
#     else:
#         products = Product.objects.all()
#
#     context = {
#         'products': products,
#         'categories': dict(Product.CATEGORY_CHOICES),
#         'selected_category': category,  # Pass the selected category to template
#     }
#     return render(request, 'shop.html', context)
def shop(request):
    products = Product.objects.all()
    categories = dict(Product.CATEGORY_CHOICES)

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'shop.html', context)
# def login(request):
#     return render(request, 'login.html')
#
# def signup(request):
#     return render(request, 'signup.html')
#
# def forgotpwd(request):
#     return render(request, 'forgotpwd.html')

def cart(request):
    return render(request, 'cart.html')

# product view
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:3]

    context = {
        'product': product,
        'related_products': related_products
    }
    return render(request, 'single_product.html', context)




# Updated authentication views
# def login_view(request):
#     if request.method == 'POST':
#         form = UserLoginForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 messages.success(request, f'Welcome back, {username}!')
#                 next_url = request.GET.get('next', 'home')  # Redirect to 'next' or home
#                 return redirect(next_url)
#         messages.error(request, 'Invalid username or password')
#     else:
#         form = UserLoginForm()
#
#     context = {
#         'form': form,
#         'title': 'Login'
#     }
#     return render(request, 'login.html', context)
#
#
# def signup_view(request):
#     if request.method == 'POST':
#         form = SimpleSignupForm(request.POST)
#         if form.is_valid():
#             try:
#                 user = form.save()
#                 login(request, user)
#                 return redirect('home')  # Replace with your home URL name
#             except IntegrityError:
#                 form.add_error('username', 'This username is already taken')
#     else:
#         form = SimpleSignupForm()
#
#     return render(request, 'signup.html', {'form': form})
#
# def logout_view(request):
#     logout(request)
#     messages.success(request, 'You have been logged out.')
#     return redirect('home')


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Store the welcome message in session
            request.session['welcome_message'] = f"Welcome back, {user.first_name}"
            return redirect('home')  # Redirect to index/home page
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SimpleSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after signup
            messages.success(request, f"Account created for {user.first_name}!")
            return redirect('home')
    else:
        form = SimpleSignupForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "You've been logged out successfully.")
    return redirect('home')


def forgotpwd(request):
    return render(request, 'forgotpwd.html')

#search function
def product_search_page(request):
    query = request.GET.get('q', '')
    products = []
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    return render(request, 'search_results.html', {'products': products, 'query': query})

def product_search_ajax(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )[:10]
        results = [{
            'name': product.name,
            'price': product.price,
            'image': product.image.url if product.image else '',
            'url': product.get_absolute_url()
        } for product in products]
    return JsonResponse({'results': results})

#singup messages
# def signup_view(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             # Set last_login to None for new users
#             user.last_login = None
#             user.save()
#
#             messages.success(request, f'Account created successfully! Welcome, {user.username}!')
#             return redirect('login')  # Redirect to login after signup
#     else:
#         form = UserCreationForm()  # Initialize empty form for GET requests
#
#     return render(request, 'signup.html', {'form': form})


def contact_view(request):
    if request.method == 'POST':
        # Get form data from request
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save to database
        ContactSubmission.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )

        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')  # Redirect back to contact page

    return render(request, 'contact.html')


@login_required
def account(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('account')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'account.html', {'form': form})


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'password_change.html'
    success_url = reverse_lazy('account')



#Adding to cart views start from here

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if product already in cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'price': product.price}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart.html', {'cart': cart})


@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart')

#
#
# @login_required
# def checkout_view(request):
#     print("Checkout view accessed!")  # This will show in your console
#
#     cart = request.user.cart
#     subtotal = cart.total_price
#     tax = subtotal * Decimal('0.13')  # 13% tax
#     shipping = Decimal('45.00') if cart.items.count() > 0 else Decimal('0.00')
#     total = subtotal + tax + shipping
#
#     context = {
#         'cart': cart,
#         'subtotal': subtotal,
#         'tax': tax,
#         'shipping': shipping,
#         'total': total,
#     }
#
#     return render(request, 'checkout.html',context)

@login_required
def checkout_view(request):
    cart = request.user.cart
    cart_items = cart.items.all()

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty!")
        return redirect('cart')

    # Calculate order totals
    subtotal = cart.total_price
    tax = subtotal * Decimal('0.13')
    shipping = Decimal('45.00') if cart_items.count() > 0 else Decimal('0.00')
    total = subtotal + tax + shipping

    if request.method == 'POST':
        # Create billing address form instance
        billing_data = {
            'first_name': request.POST.get('billing_first_name'),
            'last_name': request.POST.get('billing_last_name'),
            'email': request.POST.get('billing_email'),
            'phone': request.POST.get('billing_phone'),
            'street_address': request.POST.get('billing_street_address'),
            'apartment_address': request.POST.get('billing_apartment_address'),
            'city': request.POST.get('billing_city'),
            'state': request.POST.get('billing_state'),
            'zip_code': request.POST.get('billing_zip'),
            'country': request.POST.get('billing_country'),
        }

        # Validate required fields
        required_fields = ['first_name', 'last_name', 'email', 'phone',
                           'street_address', 'city', 'state', 'zip_code', 'country']

        missing_fields = [field for field in required_fields if not billing_data.get(field)]
        if missing_fields:
            messages.error(request, f"Please fill in all required billing fields: {', '.join(missing_fields)}")
            return redirect('checkout')

        # Validate email format
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError
        try:
            validate_email(billing_data['email'])
        except ValidationError:
            messages.error(request, "Please enter a valid email address")
            return redirect('checkout')

        # If all validation passes, proceed with order creation
        try:
            # Create billing address
            billing_address = BillingAddress.objects.create(
                user=request.user,
                **billing_data
            )

            # Handle shipping address
            same_as_billing = request.POST.get('same_as_billing') == 'on'

            if same_as_billing:
                shipping_address = ShippingAddress.objects.create(
                    user=request.user,
                    first_name=billing_data['first_name'],
                    last_name=billing_data['last_name'],
                    phone=billing_data['phone'],
                    street_address=billing_data['street_address'],
                    apartment_address=billing_data['apartment_address'],
                    city=billing_data['city'],
                    state=billing_data['state'],
                    zip_code=billing_data['zip_code'],
                    country=billing_data['country'],
                    notes=request.POST.get('shipping_notes', '')
                )
            else:
                shipping_data = {
                    'first_name': request.POST.get('shipping_first_name'),
                    'last_name': request.POST.get('shipping_last_name'),
                    'phone': request.POST.get('shipping_phone'),
                    'street_address': request.POST.get('shipping_street_address'),
                    'apartment_address': request.POST.get('shipping_apartment_address'),
                    'city': request.POST.get('shipping_city'),
                    'state': request.POST.get('shipping_state'),
                    'zip_code': request.POST.get('shipping_zip'),
                    'country': request.POST.get('shipping_country'),
                    'notes': request.POST.get('shipping_notes', '')
                }

                # Validate shipping fields if not same as billing
                shipping_missing = [field for field in required_fields
                                    if field != 'email' and not shipping_data.get(field)]
                if shipping_missing:
                    messages.error(request,
                                   f"Please fill in all required shipping fields: {', '.join(shipping_missing)}")
                    return redirect('checkout')

                shipping_address = ShippingAddress.objects.create(
                    user=request.user,
                    **shipping_data
                )

            # Create order
            payment_method = request.POST.get('payment_method', 'credit_card')

            order = Order.objects.create(
                user=request.user,
                billing_address=billing_address,
                shipping_address=shipping_address,
                payment_method=payment_method,
                subtotal=subtotal,
                tax=tax,
                shipping_cost=shipping,
                total=total
            )

            # Create order items
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.price
                )

            # Clear the cart
            cart.items.all().delete()

            messages.success(request, f"Order #{order.order_number} placed successfully!")
            return redirect('order_confirmation', order_id=order.id)

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('checkout')

    # For GET requests
    context = {
        'cart': cart,
        'subtotal': subtotal,
        'tax': tax,
        'shipping': shipping,
        'total': total,
    }

    return render(request, 'checkout.html', context)

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})

def fetch_reddit():
    try:
        resp = requests.get(
            "https://www.reddit.com/r/environment/.json",
            headers={"User-Agent": "eco-news-bot"},
            timeout=5
        ).json()
        out = []
        for post in resp["data"]["children"]:
            d = post["data"]
            # try preview first
            img = None
            if d.get("preview") and d["preview"]["images"]:
                img = d["preview"]["images"][0]["source"]["url"].replace("&amp;", "&")
            elif d.get("thumbnail", "").startswith("http"):
                img = d["thumbnail"]
            # only include if we have a real URL
            if img:
                out.append(Article(
                    title       = d["title"],
                    url         = "https://reddit.com" + d["permalink"],
                    description = "",
                    image_url   = img,
                    source      = "Reddit"
                ))
        return out
    except Exception:
        return []

@cache_page(60 * 10)  # cache for 10 minutes
def eco_news(request):
    # wipe old and reload fresh
    Article.objects.all().delete()
    # fetch only Reddit (all are environmental) and only those with images
    articles = fetch_reddit()
    Article.objects.bulk_create(articles)
    qs = Article.objects.order_by('-published_at')
    return render(request, "news.html", {"articles": qs})