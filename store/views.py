from django.shortcuts import render, redirect
from .models import Product, Category, Customer
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm


def category(request, foo):
    foo = foo.replace("-", " ")
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {"products": products, "category": category})

    except:
        messages.error(request, "Ushbu kategoriya topilmadi")
        return redirect('home')


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})


def home(request):
    products = Product.objects.all()[:4]
    return render(request, 'home.html', {'products': products})


def about(request):
    return render(request, 'about.html', {})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Siz tizimga muvofaqqiyatli kirdingiz')
            return redirect('home')
        else:
            messages.error(request, 'Xatolik qaytadan urinib ko\'ring')
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "Siz profilingizdan chiqdingiz")
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Muvofaqqiyatli ro\'hatga olindi')
            return redirect('home')
        else:
            messages.error(request, 'Ro\'hatdan o\'tishda hatoik. Boshqattan urinib ko\'ring')
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})


def profile_view(request, username):
    user = Customer.objects.filter(username=username)
    if not user:
        return redirect('home')
    return render(request, 'profile_detail.html', {'context': user})
