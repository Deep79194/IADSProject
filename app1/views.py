from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .forms import SimpleSignupForm, UserLoginForm ,UserUpdateForm # We'll create this next
from .models import ContactSubmission,Product,User
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import PasswordChangeView

# Create your views here.

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

# def shop(request):
#     return render(request, 'shop.html')


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
            login(request, user)  # This creates the session
            messages.success(request, f"Welcome back, {user.first_name}!")
            return redirect('home')
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