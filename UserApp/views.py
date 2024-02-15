from django.shortcuts import render,redirect
from UserApp.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
# Create your views here.

def indexPageView(request):
    return render(request, "User/index.html")


def signupPageView(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')
        if Users.objects.filter(email=email).exists():
            return render(request, "Auth/signup.html")
        if password == re_password:
            user = Users(full_name=str(full_name).title(), email=str(email).lower(), password=password,username=str(email).lower())
            user.save()
            login(request,user)
            return redirect('home-page')
        else:
            return render(request, "Auth/signup.html")
    return render(request, "Auth/signup.html")

def loginPageView(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home-page')
        else:
            return render(request, "Auth/login.html")
    return render(request, "Auth/login.html")

def logoutPageView(request):
    logout(request)
    return redirect('index-page')


def homePageView(request):
    categories = DishCategory.objects.all()
    return render(request, "User/home.html",context={'categories':categories})

def packagePageView(request):
    return render(request, "User/package.html")


def displaySubCategoryView(request,category):
    category_title = DishCategory.objects.get(id=category).title
    categorys = DishSubCategory.objects.filter(dish_category=category).all()
    return render(request, 'User/display_sub_category.html',context={'category_title':category_title,'categorys':categorys})

def displayMenuView(request,sub_category):
    sub_category_title = DishSubCategory.objects.get(id=sub_category).sub_title
    dishes = Dish.objects.filter(sub_category=sub_category)
    return render(request, 'User/display_menu.html',context={'sub_category_title':sub_category_title,'dishes':dishes})

def chooseMenuView(request):
    if request.method == 'POST':
        data_dict = []
        def test(id):
            obj = Dish.objects.get(id=int(id))
            return [obj.sub_category.sub_title,obj.dish_name,obj.dish_price]
        
        for key,value in request.POST.items():
            if key == "csrfmiddlewaretoken" or key == "guests_count":
                continue
            data_dict.append(test(value))

        request.session['data'] = data_dict
        request.session['guests_count'] = int(request.POST.get('guests_count'))
        return redirect('display-quotation')

            
    sub_categorys = DishSubCategory.objects.all()
    dishes = Dish.objects.all()
    return render(request, "User/choose_menu.html",context={'sub_categorys':sub_categorys,'dishes':dishes})


def displayQuotationView(request):
    try:
        resp = request.session.get('data') # get the value from session
        guests_count = request.session.get('guests_count') # get the value from session
        data_dict = resp
        total = sum([int(x[-1]) for x in data_dict])
        total = total*int(guests_count)
        final_amt = total + (total*0.18) + (total*0.18) - (total*0.10)
        return render(request, "User/display_quotation.html",context={'data':data_dict,'total':total,'guests_count':guests_count,
                                                                    'final_amt':final_amt})
    except:
        return render(request, "User/display_quotation.html",context={'data':None,'total':None,'guests_count':None,
                                                                    'final_amt':None})