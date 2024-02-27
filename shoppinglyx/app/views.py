from django.shortcuts import render,redirect
from django.views import View
from .models import Customer,Product,Cart,OrderPlaced
from .form import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q 
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
 def get(self,request):
  totolItems = 0      
  topwear = Product.objects.filter(category="TW")
  bottomwear = Product.objects.filter(category="BW")
  mobiles = Product.objects.filter(category="M")
  if request.user.is_authenticated:
        totolItems = len(Cart.objects.filter(user=request.user))
  return render(request,'app/home.html',{"topwear":topwear,"bottomwear":bottomwear,"mobiles":mobiles,"totolItems":totolItems})
 

class ProductDetailsView(View):
 def get(self, request, pk):
  totolItems = 0
  product=Product.objects.get(pk=pk)
  item_already_in_cart = False
  
  if request.user.is_authenticated:    
    totolItems = len(Cart.objects.filter(user=request.user))
    item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
  return render(request,'app/productdetail.html',{'product':product,"item_already_in_cart":item_already_in_cart,"totolItems":totolItems})

@login_required
def add_to_cart(request):
 user = request.user
 productId = request.GET.get('prod_id')
 product = Product.objects.get(id=productId)
 Cart(user=user,product=product).save()
 return redirect('/show-cart')

@login_required
def show_cart(request):
 if request.user.is_authenticated:
  totolItems = 0
  user = request.user
  cartItems = Cart.objects.filter(user=user)
  productAmount = 0.0
  shippingCharges = 70.0
  totalAmount = 0.0
  if request.user.is_authenticated:
    totolItems = len(Cart.objects.filter(user=request.user))
  if cartItems:
   for item in cartItems:
    productAmount += (item.quantity * item.product.discounted_price)
   totalAmount = productAmount + shippingCharges
  
   return render(request, 'app/addtocart.html',{'cartItems':cartItems,'productAmount':productAmount,'totalAmount':totalAmount,"totolItems":totolItems})
  else:
   return render(request,'app/emptycart.html')

def plus_cart(request):
 if request.method == 'GET':
 
  prod_id = request.GET['prod_id']
  print("prod id:",prod_id)
  cartItem = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  cartItem.quantity+=1
  cartItem.save()

  cartItems = Cart.objects.filter(user=request.user)
  productAmount = 0.0
  shippingCharges = 70.0
  totalAmount = 0.0
  if cartItems:
   
   for item in cartItems:
    productAmount += (item.quantity * item.product.discounted_price)
    totalAmount = productAmount + shippingCharges
  
   data = {
    'quanity':item.quantity,
    'amount':productAmount,
    'totalAmount':totalAmount
   }

   return JsonResponse(data)

 

def minus_cart(request):
 if request.method == 'GET':
 
  prod_id = request.GET['prod_id']
  print("prod id:",prod_id)
  cartItem = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  cartItem.quantity-=1
  cartItem.save()

  cartItems = Cart.objects.filter(user=request.user)
  productAmount = 0.0
  shippingCharges = 70.0
  totalAmount = 0.0
  if cartItems:
   
   for item in cartItems:
    productAmount += (item.quantity * item.product.discounted_price)
    totalAmount = productAmount + shippingCharges
  
   data = {
    'quanity':item.quantity,
    'amount':productAmount,
    'totalAmount':totalAmount
   }

   return JsonResponse(data)

def remove_cart(request):
 if request.method == 'GET':
 
  prod_id = request.GET['prod_id']
  print("prod id:",prod_id)
  cartItem = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))

  cartItem.delete()

  cartItems = Cart.objects.filter(user=request.user)
  productAmount = 0.0
  shippingCharges = 70.0
  totalAmount = 0.0
  if cartItems:
   for item in cartItems:
    productAmount += (item.quantity * item.product.discounted_price)
    
  
  data = {
  'amount':productAmount,
  'totalAmount':productAmount + shippingCharges
  }

  return JsonResponse(data)

def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required
def address(request):
 totolItems = 0
 if request.user.is_authenticated:    
  totolItems = len(Cart.objects.filter(user=request.user))
 addr = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'addr':addr,"totolItems":totolItems})

@login_required
def orders(request):
 totolItems = 0
 if request.user.is_authenticated:
  totolItems = len(Cart.objects.filter(user=request.user))
 op = OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html',{'orderPlaced':op,"totolItems":totolItems})


def mobile(request,data=None):
 if data == None:
  mobiles = Product.objects.filter(category="M")
 elif data == "Apple" or data == 'Samsung' or data == 'Vivo':
  mobiles = Product.objects.filter(category='M').filter(brand=data)
 elif data == 'below':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=20000)
 elif data == 'above':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=20000)
 totolItems = 0
 if request.user.is_authenticated:
  totolItems = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/mobile.html',{'mobiles':mobiles,"totolItems":totolItems})



class CustomerRegistrationView(View):
 def get(self,request):
  form = CustomerRegistrationForm()
  return render(request,'app/customerregistration.html',{'form':form})
 
 def post(self,request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   form.save()
   messages.success(request,'congratulations!! Register Successfully')
  return render(request,'app/customerregistration.html',{'form':form})
  
@login_required
def checkout(request):
 user = request.user
 add = Customer.objects.filter(user=user)
 cartitems = Cart.objects.filter(user=user)
 totolItems = 0
 if request.user.is_authenticated:
  totolItems = len(Cart.objects.filter(user=request.user))
 if cartitems:
  amount = sum([item.quantity * item.product.discounted_price for item in cartitems])
  totalAmount = amount + 70

 return render(request, 'app/checkout.html',{'add':add,'totalAmount':totalAmount,'cartItems':cartitems,"totolItems":totolItems})

@login_required
def payment_done(request): 
 user = request.user
 custid = request.GET.get('custid')
 customer = Customer.objects.get(id=custid)
 carts = Cart.objects.filter(user=user)
 
 for cart in carts:
  OrderPlaced(user=user,customer=customer,product=cart.product,quantity=cart.quantity).save()
  cart.delete()
 return redirect("orders")

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
 def get(self,request):
  form = CustomerProfileForm()
  return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
 def post(self,request):
  form = CustomerProfileForm(request.POST)
  if form.is_valid():
   usr = request.user
   name = form.cleaned_data['name']
   locality = form.cleaned_data['locality']
   city = form.cleaned_data['city']
   state = form.cleaned_data['state']
   zipcode = form.cleaned_data['zipcode']

   cust = Customer(user = usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
   cust.save()
   messages.success(request,"Your profile has been updated successfully!")

  return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
 


