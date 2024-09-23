from django.shortcuts import render,redirect
from django.http import HttpResponse
from AdminApp.models import Category,Cake
from .models import UserInfo,MyCart,Payment,OrderMaster,Status

# Create your views here.
def home(request):
    #Fetch all categories
    cats = Category.objects.all()
    cakes = Cake.objects.all()
    return render(request,"UserApp/homepage.html",{"cats":cats,"cakes":cakes})


def showCakes(request,cid):
    cats = Category.objects.all()
    cakes = Cake.objects.filter(cat_id = cid)
    cat_name = Category.objects.get(id=cid)

    return render(request,"UserApp/homepage.html",{"cats":cats,"cakes":cakes,"cat_name":cat_name})

def ViewDetails(request,cake_id):
    if(request.method == "GET"):
        cats = Category.objects.all()
        cake = Cake.objects.get(id=cake_id)
        return render(request,"UserApp/ViewDetails.html",{"cats":cats,"cake":cake})
    else:
        #Add to cart
        cake_id = request.POST["cake_id"]
        qty = request.POST["qty"]
        
        if("username" in request.session):
            msg = addToCart(request,cake_id,qty)
            if msg == "":
                return redirect("/") #Success
            else:
                return HttpResponse(msg)
        else:
            return redirect("/Login")
        
def addToCart(request,cake_id,qty):
    username = request.session["username"]
    user = UserInfo.objects.get(username=username)
    cake = Cake.objects.get(id = cake_id)
    try:
        item = MyCart.objects.get(user=user,cake=cake)
    except:
        status = Status.objects.get(status_name = 'cart')
        item = MyCart(user = user,cake = cake,qty=qty,status=status)
        item.save()
        return ""
    else:
        return "Item already in cart"

def Register(request):
    if request.method == "GET":
        return render(request,"UserApp/Register.html",{})
    else:
        username = request.POST["uname"]
        pwd = request.POST["pwd"]
        email = request.POST["email"]
        try:
            user = UserInfo.objects.get(username=username)
        except:
            #User is not present
            #This operation must be performed only after checking for duplicate entry
            user = UserInfo(username,pwd,email)
            user.save()
            return redirect("/")
        else:
            return HttpResponse("User already present")
        
    
def Login(request):
    if request.method == "GET":
        return render(request,"UserApp/Login.html",{})
    else:
        username = request.POST["uname"]
        pwd = request.POST["pwd"]
        
        try:
            user = UserInfo.objects.get(username=username,password=pwd)
        except:
            #User is not present
            #This operation must be performed only after checking for duplicate entry
            return redirect("/Login")
        else:
            #We need to user request.session
            request.session["username"] = username           
            return redirect("/")
    
def Logout(request):
    request.session.clear()
    return redirect("/")

def showcart(request):
    if(request.method == "GET"):
        #Filter out cart items based on user
        username = request.session["username"]
        user = UserInfo.objects.get(username= username)
        status = Status.objects.get(status_name='cart')
        items = MyCart.objects.filter(user = user,status=status)
        total = 0
        for item in items:
            total += item.qty * item.cake.price
        request.session["total"] = total
        return render(request,"UserApp/showcart.html",{"items":items})
    else:
        cart_id = request.POST["cart_id"]
        action = request.POST["action"] 
        item = MyCart.objects.get(id=cart_id)
        if action == "delete":                        
            item.delete()            
        else:
            #update
            qty = request.POST["qty"]
            item.qty = qty
            item.save()
        return redirect("/Cart")

def MakePayment(request):
    if(request.method == "GET"):
        return render(request,"UserApp/MakePayment.html",{})
    else:
        cardno = request.POST["cardno"]
        cvv = request.POST["cvv"]
        expiry = request.POST["expiry"]
        try:
            buyer = Payment.objects.get(cardno = cardno,cvv=cvv,expiry=expiry)
        except:
            return redirect("/MakePayment")
        else:
            owner = Payment.objects.get(cardno = '222',cvv='222',expiry='12/2030')
            owner.balance += request.session["total"]
            if buyer.balance > request.session["total"]:
                buyer.balance-=request.session["total"]
                owner.save()
                buyer.save()
                updateOrder(request)
                return redirect("/")
            else:
                return HttpResponse("Insufficient Balance")

def updateOrder(request):
    total = request.session["total"]
    username = request.session["username"]
    user = UserInfo.objects.get(username= username)
    status = Status.objects.get(status_name='cart')
    items = MyCart.objects.filter(user = user,status=status)
    status  =Status.objects.get(status_name='order')
    for item in items:
        item.status=status
        item.save()
    order = OrderMaster(user = user,amount = total)
    order.save()


def MyOrders(request):
    username = request.session["username"]
    user = UserInfo.objects.get(username= username)
    status = Status.objects.get(status_name='order')
    items = MyCart.objects.filter(user = user,status=status)

    order = OrderMaster.objects.get(user = user)

    return render(request,"UserApp/MyOrders.html",{"items":items,"order":order})
