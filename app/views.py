from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import reverse
from django.shortcuts import redirect
from django.shortcuts import Http404

from .models import POSTS
from .models import Comments
from .models import Category
from .models import buys
from .models import SabadKharid

from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth import logout as _logout

from django.contrib.auth.models import User

from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage

from rest_framework.views import APIView
from rest_framework.response import Response

from zeep import Client
from .forms import SignUpForm
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.db.models import Q

from .models import Grouping

# Create your views here.

MERCHANT = '2b2d5972-8ba6-11e9-bfc4-000c29344814'

client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl') 

def Buty(request): 
    riall = str(request)[::-1]
    RIAL = ''
    if len(str(riall)) > 3:
        count = 0
        c2 = 1
        for x in riall:
            if count == 2 :
                RIAL = RIAL + x
                if len(riall) > c2: 
                    RIAL = RIAL + ","
                count = 0
            else :
                RIAL = RIAL + x
                count += 1
            c2 += 1
    else :
        RIAL = riall
    return RIAL[::-1]

def get_cats():
    category = Category.objects.all()
    return category

def groups():
    return Grouping.objects.all()

def HOME(request): 
 
    posts = POSTS.objects.filter(published='published')[:9]
    for post in posts:
        if post.Discount:
            post.Discount = Buty(post.price - post.Discount)
        post.price = Buty(post.price)

    page = request.GET.get('page', 1)

    paginator = Paginator(posts, 12)  
    try:
        Results = paginator.page(page)
    except PageNotAnInteger:
        Results = paginator.page(12)
    except EmptyPage:
        Results = paginator.page(paginator.num_pages)
 
    context = {
        "posts": Results,
        'cats': get_cats(),
        "groups": groups()
    }
    return render(request, 'index.html', context)

def STORE(request):
    return redirect('/')

def DETAIL(request, pk):
    Post = get_object_or_404(POSTS, pk = pk)
    
    if not Post.views:
        Post.views = 1
    else:
        Post.views += 1
    Post.save()
    if Post.Discount:
        Post.Discount = Buty(Post.price - Post.Discount)
    Post.price = Buty(Post.price) 
    Post.tags = Post.tags.split(",") 
    len_if_accepted_comments = Comments.objects.filter(post = Post, status = True)
    context = {
        "len_if_accepted_comments": len_if_accepted_comments,
        "post": Post, 
        'comments': Comments.objects.filter(post = Post),
        'cats': get_cats(),
        "groups": groups()
        }

    return render(request, 'product-page.html', context)

def comment(request):
    post_id = str()
    if request.method == "POST":
        post_id = request.POST['post_id']
        Comments(
            name = request.POST['name'],
            email = request.POST['mail'],
            comment = request.POST['comment'],
            post = get_object_or_404(POSTS, pk =post_id)
        ).save()
        messages.success(request, "نظر شما با موفقیت ثبت شد ") 
        print(post_id)
        return redirect(f"/store/{post_id}")
    else:
        return redirect("/store/")

def categorys(request, cat=None):
    if not cat:
        return redirect('/')

    cats = POSTS.objects.all()
    for post in cats:
        post.price = Buty(post.price)
    posts = list()
    for catt in cats:
        for c in catt.category.all():
            if c.name == cat:
                posts.append(catt)
 
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 1)  
    try:
        Results = paginator.page(page)
    except PageNotAnInteger:
        Results = paginator.page(1)
    except EmptyPage:
        Results = paginator.page(paginator.num_pages)
 
    context = {
        "posts": Results,  
        'cats': get_cats(),
        "groups": groups()
        }
    return render(request, 'categorys.html', context)

def search(request):
     
    if not request.method == 'POST': return redirect('/')
    
    query = request.POST['q']
    lookups= Q(title__icontains=query) | Q(content__icontains=query)
    Results = list()
    for post in POSTS.objects.filter(lookups).distinct(): 
        post.price = Buty(post.price)
        Results.append(post)
    page = request.GET.get('page', 1)
    paginator = Paginator(Results, 1)  
    try:
        Results = paginator.page(page)
    except PageNotAnInteger:
        Results = paginator.page(1)
    except EmptyPage:
        Results = paginator.page(paginator.num_pages)
    context = {
        'query': query,
        "posts": Results,  
        'cats': get_cats(),
        "groups": groups()
        }
    return render(request, 'search.html', context)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']
        user = authenticate(username = username, password = password)
        if user:
            auth_login(request, user)
            return redirect('/')
        else:
            messages.success(request, 'نام کاربری یا رمز عبور اشتباست')
            return redirect('/login/')

    else:
        return render(request, 'login.html')

def signup(request): 

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        _errors = form.errors.as_data()
        if 'password2' in _errors or 'password':
            messages.success(request, 'رمز عبوری که وارد کرده اید قابل قبول نیست.')
        elif 'code_posti' in _errors:
            messages.success(request, 'کد پستی قابل قبول نیست!')
        elif 'phone_number' in _errors:
            messages.success(request, 'شماره تماس قابل قبول نیست')
        elif 'email' in _errors:
            messages.success(request, 'ایمیل قابل قبول نیست')
        elif 'username' in _errors:
            messages.success(request, 'نام کاربری قابل استفاده نمیباشد، لطفا نام کاربری دیگری انتخاب نمائید.')
        else:
            messages.success(request, 'لطفا دوباره تلاش نمائید.!')
  
        if form.is_valid():
            user = form.save()

            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.phone_number = form.cleaned_data.get('phone_number')
            user.profile.address = form.cleaned_data.get('address')
            user.profile.code_posti = form.cleaned_data.get('code_posti')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            auth_login(request, user)
            return redirect('/')
        else:
            print("\n \n NO \n \n \n ")
    else:
        print("elsee\n \n \n else ")
        form = SignUpForm()

    context={
        'form':form,
    }
    print("\n \n unsuccess\n \n ")
    return render(request, 'signup.html', context)

def logout(request):
    try:
        _logout(request)
    except:
        pass
    return redirect('/')

def payment(request):
    if request.method == 'POST': 
 
        wallets = SabadKharid.objects.filter(user = request.user.id)
        
        error = None
        amount = int() # thats mean zero
        for wallet in wallets:
            product = get_object_or_404(POSTS, pk = wallet.product) 
            
            if product.count < wallet.count:
                messages.success(request, f"تعداد موجودی انبار از درخواست شما کمتر است ({product.title})")
                error = True
                continue
            if product.Discount:
                product.price = product.price - product.Discount
            amount += product.price * wallet.count
        print(amount)
        if error: return redirect(f"/cart/")
 
        description = "با تشکر از اعتماد شما"  
        email = 'support@shop.shop'   
        mobile = '+989354367900'   
        CallbackURL = f'http://localhost:8000/submit/{request.user.id}/'  
        result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
        if result.Status == 100:
            return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
        else: 
            messages.error(request, f'این پرداخت معتبر نیست، لطفا دوباره تلاش کنید ')
            return redirect(f'/cart/')
            
    else:
        return redirect('/')

def submit(request, user_id):  
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], post.price) 
        if result.Status == 100:          
            wallets = SabadKharid.objects.filter(user = user_id)
            for wallet in wallets: 
                post = get_object_or_404(POSTS, pk = wallet.product) 
                post.count = (post.count - wallet.count)
                post.save()
                if post.Discount:
                    post.price = Buty(post.price - post.Discount)
                
                order = buys()
                order.user = user_id
                order.price =  int(post.price) * int(wallet.count)
                order.POST = post.id
                order.count = wallet.count
                order.save()
            all_products = SabadKharid.objects.all()
            for pro in all_products:
                pro.delete()    
            messages.success(request,"با تشکر از خرید شما، پرداخت شما با موفقیت انجام شد، زمان تحویل، بسته به نوع و تعداد سفارش شماست و حداکثر تا 48 ساعت آینده به دست شما خواهد رسید. ")
            return HttpResponseRedirect(reverse('app:detail', args=[slug]))
        elif result.Status == 101:
            messages.success(request,"پرداخت شما از قبل تایید شده است و لینک های دانلود به ایمیل شما ارسال شده است.")
            return HttpResponseRedirect(reverse('app:detail', args=[pk]))
        else: 
            messages.error(request,"پرداخت ناموفق، لطفا دوباره تلاش بفرمائید.")
            return HttpResponseRedirect(reverse('app:detail', args=[pk]))
    else:  
        wallets = SabadKharid.objects.filter(user = user_id)
        for wallet in wallets: 
            post = get_object_or_404(POSTS, pk = wallet.product) 
            post.count = (post.count - wallet.count)
            post.save()
          
            order = buys()
            order.user = user_id
            order.price =  int(post.price - post.Discount) * int(wallet.count)
            order.POST = post.id
            order.count = wallet.count
            order.save()
        all_products = SabadKharid.objects.all()
        for pro in all_products:
            pro.delete()    
        messages.success(request,"با تشکر از خرید شما، پرداخت شما با موفقیت انجام شد، زمان تحویل، بسته به نوع و تعداد سفارش شماست و حداکثر تا 48 ساعت آینده به دست شما خواهد رسید. ")
       # messages.error(request,"پرداخت با موفقیت لغو شد")


        return HttpResponseRedirect(reverse('app:home'))

def sabad_kharid(request):
    if request.method != 'POST': return redirect("/")
    count = int(request.POST['count'])
    pk = request.POST['post']
    POST = get_object_or_404(POSTS, pk = pk)
    if count == 0:
        messages.error(request, "لطفا تعدادی مد نظر خود را وارد نمائید.")
        return redirect(f'/store/{pk}/')
    if count > POST.count:
        messages.error(request, "موجودی انبار کافی نیست، لطفا عددی دیگری وارد نمائید.")
        return redirect(f'/store/{pk}/')
     
    results = SabadKharid.objects.filter(user = request.user.id, product = pk)

    if results:
        for result in results:
            result.count = count 
            result.save()
    else:
        sabad = SabadKharid()
        sabad.user = request.user.id
        sabad.product = pk
        sabad.count = count 
        sabad.save()

    messages.success(request, 'محصول مورد نظر با موفقیت به سبد خرید اضافه شد.') 
    return redirect(f'/store/{pk}/')

def cart(request):
    print(request.method, request.user.is_authenticated)
    if request.method != "GET" or not request.user.is_authenticated: return redirect("/")

    results = list()
    prices = int()
    querys = SabadKharid.objects.filter(user = request.user.id)
    print(len(querys))
    for query in querys:

        post = get_object_or_404(POSTS, pk = query.product)
        if post.Discount:
            prices += query.count * (post.price - post.Discount)
            post.Discount = Buty(post.price - post.Discount)
      
        post.price = Buty(post.price)
        results.append({
            "post": post, 
            "count": query.count
        })

    prices = Buty(prices)

    print(results)
    context = {"carts": results, "All": prices, "groups": groups(), 'cats': get_cats(),}
    return render(request, "cart.html", context=context)


def update_prices(user):
    prices = int()
    for post in SabadKharid.objects.filter(user = user):
        P = get_object_or_404(POSTS, pk = post.product)
        if P.Discount:
            prices += (P.price - P.Discount) * post.count
        else:
            prices += P.Discount * post.count
 
    return prices

def change_count(request):
    if not request.is_ajax: return redirect("/")
    count = request.GET.get("values")
    product_id = request.GET["post_id"]
    User_ID = request.user.id
    print(product_id, User_ID, count)
    product = get_object_or_404(SabadKharid, user = User_ID, product = product_id)
    product.count = count
    product.save()
 
    data = {
        'All': Buty(update_prices(User_ID))
    }
    print(data)
    return JsonResponse(data)

def Second_Update_Prices(request):
    if not request.is_ajax: return redirect("/")

    return JsonResponse({'All': Buty(update_prices(request.user.id))})

def remove_product(request):
    if not request.is_ajax: return redirect("/")
    product_id = request.GET['this_id'] 
    User_ID = request.user.id
    try:
        get_object_or_404(SabadKharid, user = User_ID, product = product_id).delete()
    except Exception as error:
        print(error)
    return JsonResponse({})

class check(APIView):
    def get(self, request, format = None):
        try:
            username = request.data["username"]
            password = request.data["password"]
        except:
            return Response(None)
 
        user = authenticate(username = username, password = password)
        
        if user:

            result = {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "date_joined": user.date_joined,
                "last_login": user.last_login,
            } 
            return Response(result)
        else:
            return Response(None)
        
class get_users(APIView):
    def get(self, request):
        users = User.objects.filter(is_superuser=False, is_staff = False)

        __ = list()
        
        for user in users: 
            print(user.id)
            for pay in buys.objects.all(): 
                _all = int()    
                if user.id == pay.user:
                    for _pay in buys.objects.filter(user = user.id):
                        _all += _pay.price
                _last_buy = buys.objects.filter(user = user.id)
                if _last_buy:
                    _last_buy = _last_buy[0].price
                else:
                    _last_buy = 0
            __.append(
                {
                    'user_id': user.id,
                    'name': user.first_name + " " + user.last_name,
                    'phone': user.profile.phone_number,
                    'register': user.date_joined,
                    'last_buy': _last_buy,
                    'all': _all
                }
            ) 

 
        data = {'users': __}
        return Response(data)

class search_clients(APIView):
    def get(self, request):
        try:
            try:
                if request.data['data'] == 'name':
                    users = User.objects.filter(is_superuser=False, is_staff = False, first_name = request.data['query'])
                else:
                    users = User.objects.filter(is_superuser=False, is_staff = False, pk = request.data['query'])
            except:
                return Response({'users': []})

            __ = list()

            for user in users: 
                print(user.id)
                for pay in buys.objects.all(): 
                    _all = int()    
                    if user.id == pay.user:
                        for _pay in buys.objects.filter(user = user.id):
                            _all += _pay.price
                    _last_buy = buys.objects.filter(user = user.id)
                    if _last_buy:
                        _last_buy = _last_buy[-1].price
                    else:
                        _last_buy = 0
                __.append(
                    {
                        'user_id': user.id,
                        'name': user.first_name + " " + user.last_name,
                        'phone': user.profile.phone_number,
                        'register': user.date_joined,
                        'last_buy': _last_buy,
                        'all': _all
                    }
                ) 

    
            data = {'users': __}
            return Response(data)
        except:
            return Response({'users': []})

class adduser(APIView):
    def get(self, request):
        try:
            name = request.data['name']
            username = request.data['username']
            email = request.data['email'] 
            createuser = User()
            createuser.first_name = name
            createuser.username = username
            createuser.email = email
            userid = createuser.save() 
             

            return Response({'data': True})
        except Exception as e:
            print(e)
            return Response({'data': False})

class delete(APIView):
    def get(self, request):
        try:
            userid = request.data['userid'] 
            get_object_or_404(User, pk = userid).delete()
            return Response({'data': True})
        except Exception as e:
            print(e)
            return Response({'data': False})

class get_user(APIView):
    def get(self, request):
        data = get_object_or_404(User, pk = request.data['userid'])
        DATA = {
            'name': data.first_name + " " + data.last_name,
            'username': data.username,
            'email': data.email ,
        }
        return Response(DATA)

class update_user(APIView):
    def get(self, request):
        try:
            name = request.data['name']
            email = request.data['email']
            username = request.data['username']
            user = get_object_or_404(User, pk = request.data['id'])
            if len(name.split(" ")) > 1:
                first_name = name.split(" ")[0]
                last_name = name.split(" ")[-1]
            else:
                first_name = name 
                last_name = ''
             
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()
        except:
            return Response({"response": False})
        else:
            return Response({"response": True})

class update_store(APIView):
    def get(self, request):
        posts = list()
        for post in POSTS.objects.all():
            posts.append(
                {
                    'post_id': post.id,
                    'title': post.title,
                    'count': post.count,
                    'price': post.price
                }
            )
        return Response({'posts': posts})

class add_product(APIView):
    def get(self, request):
        try:
            namekala = request.data['namekala']
            countkala = request.data['countkala']
            pricekala = request.data['pricekala']

            POSTS(
               title = namekala, 
               price = pricekala,
               count =  countkala
            ).save()
            return Response({'status': True})
        except:
            return Response({'status': False})

class get_product(APIView):
    def get(self, request):
        pk = request.data['pk']
        post = get_object_or_404(POSTS, pk = pk)
        DATA = {
            'title': post.title,
            'count': post.count,
            'price': post.price,
        }
        return Response(DATA)

class update_product(APIView):
    def get(self, request):
        try:
            ID = request.data['id']
            title = request.data['title']
            count = request.data['count']
            price = request.data['price']

            post = get_object_or_404(POSTS, pk = ID)

            post.title = title
            post.count = count
            post.price = price

            post.save()
        except:
            return Response({'response': False})
        else:
            return Response({'response': True})

class delete_product(APIView):
    def get(self, request):
        try:
            pk = request.data['pk']
            get_object_or_404(POSTS, pk = pk).delete()
        except:
            return Response({'response': False})
        else:
            return Response({'response': True})

class product_search(APIView):
    def get(self, request): 
        try:
            sata = get_object_or_404(POSTS, pk = request.data['pk'])
            A = {
                "pk": request.data['pk'],
                "title": sata.title,
                "price": sata.price,
                "count": sata.count
            }
            return Response({"data": A})
        except:
            return Response({'data': False})

class AllSells(APIView):
    def get(self, request):
        try:
            All = buys.objects.all()
            print(All)
            data = list()
            for _ in All:
                _.POST = 3
                _.save()
                try:
                    data.append(
                        {
                            'user': _.user,
                            'user_name': get_object_or_404(User, pk = _.user).first_name + " " + get_object_or_404(User, pk = _.user).last_name,
                            'price': _.price,
                            'POST': get_object_or_404(POSTS, pk = _.POST).title ,
                            'count': _.count,
                            'all_price': int(_.price) * int(_.count)
                        }
                    )
                except:
                    print("exepyt")
                    continue
            return Response({'data': data})
        except Exception as t:
            print(t)
            return Response({'data': False})

class get_product_for_buy(APIView):
    def get(self, request):
        code_kal = request.data['code_kala']
        count = request.data['count']
        client_id = request.data['client_id']
        try: posts = get_object_or_404(POSTS, pk = code_kal)
        except: return Response({"response": 404}) # Kala Not Found
        if posts.count < int(count): return Response({"response": 500})# kala ha kam hastan 
        try: user = get_object_or_404(User, pk = client_id)
        except Exception as e:
            print(e)
            return Response({"response": 400}) # user not found 

        data = {
            "response": True,
            "data":{
                "user": user.id,
                "pk": posts.id,
                'title': posts.title,
                "count": count,
                "price": posts.price 
            }
        }
        return Response(data)

class verify(APIView):
    def get(self, request):
        try:    
            projects = list()
            for x in dict(request.data)['response']:
                print(x)
                user = x.split("+")[1]
                kala = x.split("+")[2]
                count = str(x.split("+")[-1]).replace(",", "")
                projects.append({
                    'user': user,
                    'kala': kala,
                    'count': count
                })

            print(projects)
            for _ in projects:
                try: 
                    post = get_object_or_404(POSTS, pk = _['kala']) 
                    print(post.count)
                    post.count -= int(_['count'])
                    print(post.count)
                    post.save()
                    _buys = buys()
                    _buys.user = int(_['user'])
                    _buys.price = int(post.price) * int(_['count'])
                    _buys.count = int(_['count'])
                    _buys.POST = int(_['kala'])
                    x =  _buys.save() 
                    print("saved, ", x)
                except Exception as a:
                    print(a)
                    continue    
        except:
            return Response({'response': False, })
        else:


            return Response(
                {
                    'response': True,
                    'data': projects, 
                    }
                )

def aboutus(request):
    context = {
        "groups": groups(),
    }
    return render(request, "about-us.html", context)