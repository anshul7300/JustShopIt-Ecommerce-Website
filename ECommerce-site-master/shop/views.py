# Create your views here.
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Product,Contact,Order,OrderUpdate,Login
from django.views.decorators.csrf import  csrf_exempt
from math import ceil
from paytm import Checksum
import json
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User

MERCHANT_KEY = 'Your paytm Merchant account key '

def index(request):
    allProds=[]
    catprods = Product.objects.values('category','id')
    cats={item['category'] for item in catprods}
    for cat in cats:
        prod= Product.objects.filter(category=cat)
        print(prod)
        n=len(prod)
        nslides = n//4 + ceil((n/4)-(n//4))
        allProds.append([prod,range(1,nslides),nslides])
    params= {'allProds':allProds}                                   
    #params={'product':products,'no_of_slides':nslides,'range':range(1,nslides)}
    return render(request, 'shop/index.html',params)

def searchMatch(query,item):
    if (query.lower() in item.Disc.lower() or query.lower() in item.product_name.lower() or query.lower() in item.category.lower() or query.lower() in item.subcategory.lower()):
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    allProds=[]
    catprods = Product.objects.values('category','id')
    cats={item['category'] for item in catprods}
    for cat in cats:
        prodtemp= Product.objects.filter(category=cat)
        prod= [item for item in prodtemp if searchMatch(query,item)]
        n=len(prod)
        nslides = n//4 + ceil((n/4)-(n//4))
        if len(prod)!= 0:
           allProds.append([prod,range(1,nslides),nslides])
    params= {'allProds':allProds,'msg':""}
    if len(allProds)==0 or len(query)< 4 :
        params={'msg':"Please enter relavant items no search result found!!"}                               
    #params={'product':products,'no_of_slides':nslides,'range':range(1,nslides)}
    return render(request, 'shop/index.html',params)


def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    thank = False
    if request.method =="POST":
        name =request.POST.get('name','')
        Email=request.POST.get('Email','')  
        phone=request.POST.get('phone','')
        Disc=request.POST.get('Disc','')
        contact=Contact(name=name,email=Email,phone=phone,Disc=Disc)
        contact.save()
        thank = True    
    return render(request,'shop/contact.html',{'thank': thank})

    
def tracker(request):
    if request.method =="POST":
        orderId =request.POST.get('orderid','')
        email =request.POST.get('email','')
    
        try:
            order= Order.objects.filter(order_id=orderId,email=email) # order will be in the form of list so we use order[0]
            if len(order) >0:
                update = OrderUpdate.objects.filter(order_id= orderId)
                updates= []
                for item in update:
                    updates.append({'text': item.update_disc,'time':item.timestamp})
                    response = json.dumps([updates, order[0].Items_list],default=str) # Convert python code into json text
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
                return HttpResponse('{}') 
    return render(request,'shop/tracker.html')


def prodView(request,id):
    product=Product.objects.get(id =id)
    #print(product)
    return render(request,'shop/prodView.html',{'product':product})

def checkout(request):
    if request.method =="POST":
        name =request.POST.get('name','')
        amount = request.POST.get('amount','')
        item_list =request.POST.get('items_list','')
        address= request.POST.get ('address1','') + " " + request.POST.get ('address2','')
        email=request.POST.get('email','')  
        phone=request.POST.get('phone','')
        city=request.POST.get('city','')
        state= request.POST.get('state','')
        zip_code = request.POST.get('zip_code','')
        order=Order(name=name,email=email,phone=phone,city=city,state=state,amount=amount,Items_list=item_list,zipcode=zip_code,address=address)
        order.save()
        update= OrderUpdate(order_id= order.order_id,update_disc="The order has been placed")
        update.save()
        thank = True
        id= order.order_id
        #return render(request,'shop/checkout.html',{'thank':thank,'id': id})
        # Request paytm to transfer amount to my account after payment is done by user
        param_dict ={
            'MID':'Paytm Merchant Account Id',
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'WEBSTAGING', 
            'CHANNEL_ID':'WEB',
	        
        }
        
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum_by_str(param_dict,MERCHANT_KEY,salt=None)

        return render(request,'shop/paytm.html',{'param_dict':param_dict,'thank':True})
    return render(request,'shop/checkout.html')


@csrf_exempt # It will provide relaxation of csrf_token or bypass the csrf token and we will able to recieve post request from paytm
def handlerequest(request):
    # paytm will send us post request after we send a post request to paytm
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})

def handlelogin(request):
    if request.method == 'POST':
      loginusername= request.POST.get('loginusername')
      loginpassword= request.POST.get('loginpass')
    
      user=authenticate(username=loginusername,password=loginpassword)

      if user is not None:
          login(request,user)
          messages.success(request,"Successfully Loged In")           
          return redirect('index')
      else:
          messages.error(request,"Invalid Username and Password, please try again!")
          return redirect('ShopHome')

    return HttpResponse('404 - Not found')
   
def handlesignup(request):
    if request.method == 'POST':
        username= request.POST.get('username','')
        fname= request.POST.get('fname','')
        lname= request.POST.get('lname','')
        email= request.POST.get('signupemail','')
        pass1= request.POST.get('pass1','')
        pass2= request.POST.get('pass2','')

        if len(username) > 15:
            messages.error(request,"Username must be under 15 characters")
            return redirect('index')

        if not username.isalnum:
            messages.error(request,"Username must contain aplphabets or atleast one number  ")
            return redirect('index')

        if pass1 != pass2:
            messages.error(request,"Confirmed password do not matched with Above password ")
        
        if len(pass1)<= 8 or len(pass2)<= 8:
            messages.error(request,"Length of password should be greater than or equal to 8")
            return redirect('index')

        if User.objects.filter(username__iexact=username).exists():
            messages.error(request,'Username already exists!')
        else:
            myuser=User.objects.create_user(username,email,pass1)
            myuser.first_name = fname
            myuser.last_name= lname
            myuser.save()
            messages.success(request,"Your Account has been Successfully Created!")
        return redirect('index')
    else:
        return HttpResponse('404-Error Authentication not allowed')

def handlelogout(request):   
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('index')
    return HttpResponse('404-Error Page not found')
