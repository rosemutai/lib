from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate,logout
from django.http import HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from .forms import *
from .models import *
from random import randrange
from datetime import datetime, timedelta, date
from base64 import b64decode, b64encode
import requests
import json
from requests.auth import HTTPBasicAuth
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from mpesa_api.models import Stk



# Create your views here.
@csrf_exempt
def MpesaAccessToken(request):
    """
    Function to generate token from the consumer secret and key
    """
    consumer_key = '2P4cv9cG201Kp0xhCrnFpyELGqJxbAXe'
    consumer_secret = 'p2YWhvq3o9iO6yky'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    auth = json.loads(r.text)
    token = auth['access_token']
    return token

@csrf_exempt
def lipa_na_mpesa_online(request,phone,amount):
    """
    Initiate stk push to client. Pass phone number of the client and amount to be billed as parameters.
    Will be called by any the other fucntion that requires to perform a billing and return the data response from safaricom
    """
    phone = phone
    amount = amount

    api_transaction_URL = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    BusinessShortCode = 174379;
    LipaNaMpesaPasskey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919';
    access_token = MpesaAccessToken(request)
    data = None

    get_now = datetime.now()
    payment_time = get_now.strftime("%Y%m%d%H%M%S")
    to_encode = '{}{}{}'.format(
        BusinessShortCode, LipaNaMpesaPasskey, payment_time)
    payment_password = (b64encode(to_encode.encode('ascii'))).decode("utf-8")

    if access_token:
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": BusinessShortCode,
            "Password": payment_password,
              "Timestamp": payment_time,
              "TransactionType": "CustomerPayBillOnline",
              "Amount": amount,
              "PartyA": phone,
              "PartyB": BusinessShortCode,
              "PhoneNumber": phone,
              "CallBackURL": ' https://fff023fc.ngrok.io/stkconfirm/',
              "AccountReference": "ebook",
              "TransactionDesc": 'payment'
        }
        response = requests.post(
            api_transaction_URL, json=request, headers=headers)
        # somedata = response[i]
        # data2 = response[i]
        # Stk.objects.create(field =somedata, field2=data2)
        data = response.text

    else:
        print('access token failed')

    return data

@csrf_exempt
@require_POST
def stkconfirm(request):
    if request.method == "POST":
        mpesa_body =request.body.decode('utf-8')
        mpesa_payment = json.loads(mpesa_body)


        get_data = mpesa_payment['Body']['stkCallback']
        get_success_data = get_data['CallbackMetadata']

        if get_data:
            MerchantRequestID = get_data[
                'MerchantRequestID']
            CheckoutRequestID = get_data[
                'CheckoutRequestID']
            ResultCode = get_data['ResultCode']
            ResultDesc = get_data['ResultDesc']

            if get_success_data:
                get_items = get_success_data['Item']
                for i in get_items:
                    if i['Name'] == 'Amount':
                        Amount = i.get('Value')
                    elif i['Name'] == 'MpesaReceiptNumber':
                        MpesaReceiptNumber = i.get('Value')
                    elif i['Name'] == 'PhoneNumber':
                        PhoneNumber = i.get('Value')
                    elif i['Name'] == 'Balance':
                        Balance = i.get('Value')
                    elif i['Name'] == 'TransactionDate':
                        TransactionDate = i.get('Value')
                    else:
                        continue

            else:
                Amount = None
                MpesaReceiptNumber = None
                PhoneNumber = None
                Balance = None
                TransactionDate = None

            stk_response = Stk.objects.create(MerchantRequestID=MerchantRequestID, CheckoutRequestID=CheckoutRequestID, \
                                              ResultCode=ResultCode, ResultDesc=ResultDesc, Amount=Amount,
                                              MpesaReceiptNumber=MpesaReceiptNumber, \
                                              PhoneNumber=PhoneNumber, Balance=Balance, TransactionDate=TransactionDate)

        print(mpesa_payment)


        context = {
            "ResultCode": 0,
            "ResultDesc": "Accepted"
        }
        return JsonResponse(dict(context))

def home(request):
    group_of_categories = GroupOfCategory.objects.all()
    categories = Category.objects.all()
    response = render(request, 'index.html', {'categories': categories},{'group_of_categories':group_of_categories})
    #if request.COOKIES['ident']==0:
    response.set_cookie('ident',0)#request.COOKIES['ident'])
    #else:
    #    response.set_cookie('ident',0)
    return response

def signup(request):
    if request.method=="POST":
        f=Signup(request.POST)
        if f.is_valid():
            if f.cleaned_data['cpass']==f.cleaned_data['password']:
                x=User.objects.filter(email=request.POST.get('email'))
                print(f.cleaned_data['email']+" "+str(len(x)))
                if len(x)==0:
                    u=User(username=f.cleaned_data['username'],email=f.cleaned_data['email'],password=f.cleaned_data['cpass'],postcode=f.cleaned_data['postCode'])
                    u.save()
                    return render(request,'signin.html')
                else:
                    return render(request,'signup.html',{'error':"Email is already registered"})
            else:
                return render(request,'signup.html',{'error':"Passwords do not match"})
        else:
            return render(request,'signup.html',{'error':"Fill in all the fields and make sure your password is atleast 8 characters long"})
    else:
        return render(request,'signup.html')

def signin(request):
    if request.method=="POST":
        f=Login(request.POST)
        if f.is_valid():
            email=f.cleaned_data['email']
            password=f.cleaned_data['password']
            x=User.objects.filter(email=email,password=password)
            if len(x)==1:
                response=redirect('user',x[0].email)
                response.set_cookie('email',x[0].email)
                return response
            else:
                return render(request,'signup.html',{'error':"Wrong Email or Password"})
        else:
            return render(request,'signup.html',{'error':"Invalid Form"})
    else:    
        return render(request,'signin.html')

def user_logout(request):
    logout(request)
    return redirect('home')

def get_books_by_category(request, name):
    books = Book.objects.filter(category_name=name)
    return render(request, 'categories.html',  {books: 'books'})

def get_book_by_group_of_categories(request,name):
    books = Book.objects.filter(category__group_name=name)
    return render(request, 'categories.html', {books: 'books'})


def shop(request):
    # books=Book.objects.filter(~Q(book_img=''))
    books = Book.objects.all()[:1]
    print(books)
    return render(request, 'shop.html', {'books': books})

def books_view(request):
    books = ExerciseBook.objects.all()
    print(books)
    return render(request, 'books.html', {'books': books})

def pens_view(request):
    context = {}
    pen = Pen.objects.all()
    context['pens'] = pen
    print(pen)
    return render(request, 'pens.html', context)

def arts_view(request):
    context = {}
    art = Art.objects.all()
    context['arts'] = art
    print(art)
    return render(request, 'arts.html', context)

def sports_view(request):
    context = {}
    sport = Sport.objects.all()
    context['sports'] = sport
    print(sport)
    return render(request, 'sports.html', context)

def stationeries_view(request):
    context = {}
    stationeries = Stationery.objects.all()
    context['stationers'] = stationeries
    print(stationeries)
    return render(request, 'stationery.html', context)

def user(request,username):
    if request.method == "POST":
        books = Book.objects.filter(~Q(book_img=''))
        # query = 'math'
        # if query:
        #     # books = Book.objects.filter(Q(book_name__icontains=query) | Q(category__icontains=query))
        #     books = Book.objects.filter(book_name__icontains=query)

        user = User.objects.get(email=request.COOKIES['email'])
        return render(request, 'user.html', {'books': books, 'user': user})

    if request.COOKIES['email']:
        #select * books from db and send them
        books=Book.objects.filter(~Q(book_img=''))
        user=User.objects.get(email=username)
        return render(request,'user.html',{'books':books,'user':user})
    else:
        return redirect('signin')
def cart(request):
    if request.COOKIES['email']:
        u=User.objects.get(email=request.COOKIES['email'])
        items=Cart.objects.filter(user=u,paid=False)
        books=[]

        for item in items:
            books+=[Book.objects.get(ISBN=item.ISBN)]

        total=totalPrice(items)
        return render(request,'cart.html',{'items':items,'total':total,'user':request.COOKIES['email']})

    else:
        return render('signin')

def addToCart(request):
    if request.COOKIES['email']:
        if request.method=="POST":
            ISBN=request.POST.get('isbn')
            q=request.POST.get('quantity')
            if(q==None):
                q=1
            elif(len(q)<1 or q==0):
                q=1
            else:
                q==q
            u=User.objects.get(email=request.COOKIES['email'])
            b=Book.objects.get(ISBN=ISBN)
            c=Cart(user=u,book=b,price=b.price,ISBN=ISBN,quantity=q)
            c.save()
            return redirect('user',request.COOKIES['email'])
        else:
            return redirect('signin')
    else:
        return redirect('signin')


def removeItem(request,ISBN):
    if request.COOKIES['email']:
        u=User.objects.get(email=request.COOKIES['email'])
        b=Book.objects.get(ISBN=ISBN)
        c=Cart.objects.filter(user=u,book=b).delete()
        # c.delete(b)
        return redirect('cart')
    else:
        return redirect('signin')

def __len__(self):
    return sum(book['quantity'] for book in self.cart.values())

def order(request):
    if request.method=="POST" and len(request.COOKIES['ident'])>0:
        ibsm=request.POST.get('isbn')
        q=request.POST.get('quantity')
        if q==None:
            q=1
        elif len(q)==0:
            q=1
        elif int(q)==0:
            q=1
        else:
            q=q
        x=Book.objects.get(ISBN=ibsm)
        Guest(guest_id=request.COOKIES['ident'],ISBN=ibsm,quantity=int(q),price=x.price).save()
        return redirect('guestorder')
    else:
        return redirect('guest')


def guest(request):
    id=None
    if int(request.COOKIES['ident'])==0:
        id=randrange(0,1000000)
        g=Guest.objects.filter(guest_id=id)
        if(len(g)>0):
            while len(g)!=0:
                id=range(0,1000000)
                g=GuestSession.objects.filter(guest_id=id)
        GuestSession(guest_id=id).save()
        books=Book.objects.all()
        response=render(request,'shop.html',{'books':books})
        response.set_cookie('ident',id)
        print(id)
        return response
    else:
        id=request.COOKIES['ident']
        books=Book.objects.all()
        response=render(request,'shop.html',{'books':books})
        response.set_cookie('ident',id)
        return response
    # return render(request,'shop.html', {'books':books})

def guestorder(request):
    if request.COOKIES['ident']:
        id=request.COOKIES['ident']
        orders=Guest.objects.filter(guest_id=id)
        total=totalPrice(orders)
        return render(request,'orderc.html',{'items':orders,'total':total})
    else:
        return redirect('order_guest')

def order_user(request):
    if request.method == 'POST':
        print(request.COOKIES['email'])

        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            u = User.objects.get(email=request.COOKIES['email'])
            items = Cart.objects.filter(user=u, paid=False)
            books = []

            for item in items:
                book = Book.objects.get(ISBN=item.ISBN)
                books += [book]
                OrderItem.objects.create(order=order, books=Book.objects.get(ISBN=item.ISBN), price=item.price, quantity=item.quantity)
            total = totalPrice(items)
            order.total = total
            order.save()
            emailNotification(order.id)
        return render(request, 'orderCreated.html', {'order': order, 'items': items, 'total': total})
    else:
        form = OrderCreateForm()
    return render(request, 'orderCreate.html', {'form': form})

@csrf_exempt
def order_pay(request):
    if request.method == "POST":
        orderid = request.POST['orderid']
        order=Order.objects.get(id=orderid)
        phone='254'+ str(order.phone)
        amount=1
        mpesa = lipa_na_mpesa_online(request,phone,amount)
        print(mpesa)
        u = User.objects.get(email=request.COOKIES['email'])
        items = Cart.objects.filter(user=u, paid=False)
        books = []

        for item in items:
            book = Book.objects.get(ISBN=item.ISBN)
            books += [book]
            OrderItem.objects.create(order=order, books=Book.objects.get(ISBN=item.ISBN), price=item.price,
                                     quantity=item.quantity)
        total = totalPrice(items)
    return render(request, 'orderCreated.html', {'order': order, 'items': items, 'total': total})

def guestpay(request):
    if request.COOKIES['ident']:
        if request.method=="POST":
            id=request.COOKIES['ident']
            orders=Guest.objects.filter(guest_id=id)
            total=totalPrice(orders)
            return render(request,'pay.html',{'total':total,'user':'Guest'})
        else:
            id=request.COOKIES['ident']
            orders=Guest.objects.filter(guest_id=id)
            total=totalPrice(orders)
            return render(request,'pay.html',{'total':total,'user':'Guest'})

        # return render(request,'orderc.html',{'items':orders,'total':total})

        # return render(request,'orderc.html',{'items':orders,'total':total})

    else:
        return redirect('/')

def pay(request):
    if request.COOKIES['email']:
        if request.method=="POST":
            phoneNO=request.POST.get('phoneNO')
            amount=request.POST.get('amount')
            if(phoneNO==None):
                print("ERROR")
                return render(request,'pay.html',{'error':'Phone Number is Empty','user':request.COOKIES['email']})
            else:
                return redirect('checkpay')
        else:
            u=User.objects.get(email=request.COOKIES['email'])
            items=Cart.objects.filter(user=u,paid=False)
            books=[]
            for item in items:
                books+=[Book.objects.get(ISBN=item.ISBN)]
            total=totalPrice(items)
            return render(request,'pay.html',{'total':total,'user':request.COOKIES['email']})   
    else:
        return render('signin')
        
def checkpay(request):
    return render(request,'confirm.html',{'error':'Payment Received','state':'Payment Success','user':request.COOKIES['email']})

def totalPrice(books):
    price=0
    for book in books:
        price+=(book.price*book.quantity)
    return price


def search(request):
    books = Book.objects.filter(~Q(book_img=''))
    # query = 'math'
    # if query:
    #     # books = Book.objects.filter(Q(book_name__icontains=query) | Q(category__icontains=query))
    #     books = Book.objects.filter(book_name__icontains=query)
    if request.method == 'POST':
        search = request.POST['search']
        print(search)
        books = Book.objects.filter(~Q(book_img='') & Q(book_name__icontains=search))

    user = User.objects.get(email=request.COOKIES['email'])
    return render(request, 'user.html', {'books': books, 'user': user})

def upload_file(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        email = request.POST['email']
        file = request.POST['file']

        upload = BookLists.objects.create(first_name=first_name, last_name=last_name, phone=phone, email=email,
                                          list_img=file)
        if upload:
            message = 'Successfully uploaded your list.'
        else:
            message = 'There was an error uploading you list.'
        return render(request, 'upload.html', {'message': message})

    message = ''
    return render(request, 'upload.html', {'message': message})

def apply(request):
    message = ''
    if request.method == 'POST':
        shopname = request.POST['shopname']
        description = request.POST['description']

        u = User.objects.get(email=request.COOKIES['email'])

        print(u)
        check_if_shopowner = ShopApplication.objects.filter(user=u,accept=True)
        if not check_if_shopowner:
            application = ShopApplication.objects.create(user=u,shopName=shopname,description=description)
        else:
            application = None

        if application:
            subject = 'EBook order'
            message = 'Your application has been received and we will get back to you.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['chepngetichrose2030@gmail.com', ]
            # fail_silently = False
            mail_sent = send_mail(subject, message, email_from, recipient_list)
            print(mail_sent)
        else:
            pass

    else:
        pass

    return render(request, 'apply.html', {'message': message})

def approveseller(request):
    applications = ShopApplication.objects.filter(accept=False,cancel=False)
    return render(request, 'approveseller.html', {'applications':applications})

def payment(request):
    if request.method=="POST":
        form=OrderConfirmation(request.POST)
        if form.is_valid():
            form.save()
    return

def emailNotification(order_id):
    order = Order.objects.get(id=order_id)
    subject = 'EBook order'
    message = 'Dear {},\n\nYou have successfully placed an order.On payment collect your order from our office near you\Your order id is {}.'.format(order.first_name,order.id)

    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['chepngetichrose2030@gmail.com',]
    mail_sent = send_mail( subject, message, email_from, recipient_list )

    return mail_sent

def approveapplication(request,id):
    if request.COOKIES['email']:
        successfulApplicant=ShopApplication.objects.filter(id=id).update(accept=True)

        return redirect('approveseller')
    else:
        return redirect('signin')


def declineapplication(request,id):
    if request.COOKIES['email']:
        declined = ShopApplication.objects.filter(id=id).update(cancel=True)
        return redirect('approveseller')
    else:
        return redirect('signin')

def approvedshops(request):
    shops = ShopApplication.objects.filter(accept=True)
    return render(request, 'Approvedshops.html', {'shops':shops})

def uploaditem(request):
    if request.method == 'POST':
        title = request.POST['title']
        isbn = request.POST['isbn']
        price = request.POST['price']
        quantity = request.POST['quantity']
        description = request.POST['description']
        image = request.POST['image']
        author = request.POST['author']
        edition = request.POST['edition']

        u = User.objects.get(email=request.COOKIES['email'])

        shop_instance = ShopApplication.objects.get(user=u, accept=True)
        if not shop:
            pass
        else:
            newbook = Book.objects.create(book_name=title, book_img=image, ISBN=isbn, author=author, edition=edition,price=price,in_stock=quantity,description=description)
            shop_newbook = bookshop.objects.create(shop=shop_instance,book=newbook)

            message = 'Successfully uploaded item.'

            return render(request, 'uploaditems.html', {'message': message})

    message = ''
    return render(request, 'uploaditems.html', {'message': message})

def mybooks(request):
    u = User.objects.get(email=request.COOKIES['email'])

    shop_instance = ShopApplication.objects.get(user=u, accept=True)
    books = bookshop.objects.filter(shop=shop_instance)
    return render(request, 'Mybooks.html', {'books':books})

def uploadedfiles(request):
    files = BookLists.objects.all()
    return render(request, 'uploadedfiles.html', {'files':files})

def uploadedfile(request,id):

    message = ''

    file = BookLists.objects.get(id=id)
    books = Book.objects.filter(~Q(book_img=''))
    booklistitems = BookListsItems.objects.filter(booklist=file)
    total = totalPrice(booklistitems)
    return render(request, 'uploadedfile.html', {'file':file,'books':books,'message':message,'booklistitems': booklistitems, 'total': total})

def addbookitem(request):
    if request.method == 'POST':
        book = request.POST['book']
        quantity = request.POST['quantity']
        id = request.POST['id']
        book = Book.objects.get(ISBN=book)
        file = BookLists.objects.get(id=id)
        booklistitem = BookListsItems.objects.create(book=book,booklist=file,quantity=quantity)
        return redirect('uploadedfile',id=id)

def paybookitem(request):
    if request.method == 'POST':
        total = request.POST['total']
        id = request.POST['id']
        BookList = BookLists.objects.get(id=id)
        phone = '254' + str(BookList.phone)
        amount = 1
        mpesa = lipa_na_mpesa_online(request, phone, amount)
        print(mpesa)

        stk_response = json.loads(mpesa)

        BookListUpdate = BookLists.objects.filter(id=id).update(transaction_initiated=True,checkout_request_id=stk_response['CheckoutRequestID'])

        subject = 'Your order has been approved'
        message = 'Please click the link to pay for your order. '
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['chepngetichrose2030@gmail.com', ]
        mail_sent = send_mail(subject, message, email_from, recipient_list)


        return redirect('uploadedfile',id=id)

# def stationery(request):
#     stationeries = Stationery.objects.filter(~Q(item_img=''))
#     return render(request, 'shop.html', {'stationeries': stationeries})
#
# def sports(request):
#     return render(request, 'sports.html')
#     return price
#
def add_to_cart(request):
    if request.COOKIES['email']:
        if request.method=="POST":
            book_id=request.POST.get('book_id')
            q=request.POST.get('quantity')
            if(q==None):
                q=1
            elif(len(q)<1 or q==0):
                q=1
            else:
                q==q
            u=User.objects.get(email=request.COOKIES['email'])
            b=ExerciseBook.objects.get(book_id=book_id)
            c=Cart(user=u,book=b,price=b.price,book_id=book_id,quantity=q)
            c.save()
            return redirect('user',request.COOKIES['email'])
        else:
            return redirect('signin')
    else:
        return redirect('signin')

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Stationery, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item,user=request.user,ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("web:order")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("web:order")

    else:
        ordered_date = datetime.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("web:order")

