from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# def home(request): ( A FUNCTION BASED VIEW )
#  return render(request, 'app/home.html')

class ProductView(View):
 def get(self, request):
  totalitem = 0
  topwears = Product.objects.filter(category='TW')
  bottomwears = Product.objects.filter(category='BW')
  mobiles = Product.objects.filter(category='M')
  laptops = Product.objects.filter(category='L')
  if request.user.is_authenticated:
   totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'app/home.html', {'topwears':topwears, 'bottomwears':bottomwears, 'mobiles':mobiles, 'laptops':laptops,'totalitem':totalitem})

  

# def product_detail(request):  ( A FUNCTION BASED VIEW )
#  return render(request, 'app/productdetail.html')

class ProductDetailView(View):
 def get(self, request, pk):
  totalitem = 0
  product = Product.objects.get(pk=pk)
  item_already_in_cart = False
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
    item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
  return render(request, 'app/productdetail.html', {'product':product,'item_already_in_cart':item_already_in_cart,'totalitem':totalitem})


@login_required
def add_to_cart(request):
 if request.user.is_authenticated:
  user = request.user
  product_id = request.GET.get('product_id')
  redirect_to = request.GET.get('redirect_to')
  try:
   product = Product.objects.get(id=int(product_id))
   Cart(user=user, product=product).save()
   if redirect_to == 'checkout':
    return redirect('checkout')
   return redirect('showcart')
  except Exception as e:
   print(f"Error: {e}")
   return redirect('/')
 else:
  return redirect('/accounts/login')

@login_required
def show_cart(request):
 if request.user.is_authenticated:
  user = request.user
  totalitem = 0
  if request.user.is_authenticated:
   totalitem = len(Cart.objects.filter(user=request.user))
  cart = Cart.objects.filter(user=user)
  amount = 0.0
  shipping_amount = 70.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == user]
  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount
    totalamount = amount + shipping_amount
   return render(request, 'app/addtocart.html', {'carts': cart, 'amount': amount, 'totalamount': totalamount, 'totalitem': totalitem})
  else:
   return render(request, 'app/emptycart.html', {'totalitem': totalitem})
 else:
  return redirect('/accounts/login')
 

def plus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity += 1
  c.save()
  amount = 0.0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
   tempamount = (p.quantity * p.product.discounted_price)
   amount += tempamount

  data = {
   'quantity': c.quantity,
   'amount': amount,
   'totalamount': amount + shipping_amount
  }
  return JsonResponse(data)
 
def minus_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    if c.quantity > 1:
      c.quantity -= 1
      c.save()
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount

    data = {
      'quantity': c.quantity,
      'amount': amount,
      'totalamount': amount + shipping_amount
    }
    return JsonResponse(data)
  

def remove_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.delete()
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount

    data = {
    'amount': amount,
    'totalamount':  amount + shipping_amount
    }
    return JsonResponse(data)

# Use it to directly go to check out page without going to cart
@login_required
def buy_now(request):
  if request.user.is_authenticated:
    user = request.user
    product_id = request.GET.get('product_id')
    if product_id:
      product = Product.objects.get(id=product_id)
      # Create a temporary cart item
      Cart.objects.create(user=user, product=product, quantity=1)
      return redirect('checkout')
    return redirect('showcart')
  return redirect('login')

@login_required
def address(request):
  totalitem = 0
  if request.user.is_authenticated:
   totalitem = len(Cart.objects.filter(user=request.user))
  addr = Customer.objects.filter(user=request.user)
  return render(request, 'app/address.html', {'addr':addr, 'active':'btn-primary', 'totalitem': totalitem})

@login_required
def orders(request):
  totalitem = 0
  if request.user.is_authenticated:
   totalitem = len(Cart.objects.filter(user=request.user))
  op = OrderPlaced.objects.filter(user=request.user)
  return render(request, 'app/orders.html', {'order_placed':op, 'totalitem': totalitem})

def mobile(request, data=None):
  totalitem = 0
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
  if data == None:
   mobiles = Product.objects.filter(category='M')
  elif data == 'apple' or data == 'samsung':
   mobiles = Product.objects.filter(category='M').filter(brand=data)
  elif data == 'below':
   mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=25000)
  elif data == 'above':
   mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=25000)
  return render(request, 'app/mobile.html', {'mobiles':mobiles, 'totalitem': totalitem})

def laptop(request, data=None):
  totalitem = 0
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
  if data == None:
   laptops = Product.objects.filter(category='L')
  elif data == 'HP' or data == 'DELL':
   laptops = Product.objects.filter(category='L').filter(brand=data)
  elif data == 'below':
   laptops = Product.objects.filter(category='L').filter(discounted_price__lt=40000)
  elif data == 'above':
   laptops = Product.objects.filter(category='L').filter(discounted_price__gt=40000)
  return render(request, 'app/laptop.html', {'laptops':laptops, 'totalitem': totalitem})

def topwear(request, data=None):
  totalitem = 0
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
  if data == None:
   topwears = Product.objects.filter(category='TW')
  elif data == 'breakout' or data == 'outfitters' or data == 'brucci':
   topwears = Product.objects.filter(category='TW').filter(brand=data)
  elif data == 'below':
   topwears = Product.objects.filter(category='TW').filter(discounted_price__lt=300)
  elif data == 'above':
   topwears = Product.objects.filter(category='TW').filter(discounted_price__gt=300)
  return render(request, 'app/topwear.html', {'topwears':topwears, 'totalitem': totalitem})

def bottomwear(request, data=None):
  totalitem = 0
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
  if data == None:
   bottomwears = Product.objects.filter(category='BW')
  elif data == 'outfitters' or data == 'breakout' or data == 'brucci' or data == 'Levis':
   bottomwears = Product.objects.filter(category='BW').filter(brand=data)
  elif data == 'below':
   bottomwears = Product.objects.filter(category='BW').filter(discounted_price__lt=1000)
  elif data == 'above':
   bottomwears = Product.objects.filter(category='BW').filter(discounted_price__gt=1000)
  return render(request, 'app/bottomwear.html', {'bottomwears':bottomwears, 'totalitem': totalitem})

class CustomerRegistrationView(View):
 def get(self, request):
  form = CustomerRegistrationForm()
  return render(request, 'app/customerregistration.html', {'form':form})
 def post(self, request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Congrats! You have become a User')
   form.save()
  return render(request, 'app/customerregistration.html', {'form':form})
 
@login_required
def checkout(request):
 user = request.user
 totalitem = 0
 if request.user.is_authenticated:
  totalitem = len(Cart.objects.filter(user=user))
 add = Customer.objects.filter(user=user)
 cart_items = Cart.objects.filter(user=user)
 amount = 0.0
 shipping_amount = 70.0
 totalamount = 0.0
 cart_product = [p for p in Cart.objects.all() if p.user == request.user]
 if cart_product:
  for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount
  totalamount = amount + shipping_amount
  return render(request, 'app/checkout.html', {
    'add': add, 
    'amount': amount,
    'totalamount': totalamount, 
    'cart_items': cart_items, 
    'totalitem': totalitem
  })
 else:
  return redirect('showcart')


@login_required
def payment_done(request):
  user = request.user
  custid = request.GET.get('custid')
  customer = Customer.objects.get(id=custid)
  cart = Cart.objects.filter(user=user)
  for c in cart:
    OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
    c.delete()
  return redirect("orders")

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
 def get(self, request):
  totalitem = 0
  if request.user.is_authenticated:
   totalitem = len(Cart.objects.filter(user=request.user))
  form = CustomerProfileForm()
  return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary', 'totalitem': totalitem})
 def post(self, request):
  totalitem = 0
  if request.user.is_authenticated:
   totalitem = len(Cart.objects.filter(user=request.user))
  form = CustomerProfileForm(request.POST)
  if form.is_valid():
   user = request.user
   name = form.cleaned_data['name']
   locality = form.cleaned_data['locality']
   city = form.cleaned_data['city']
   state = form.cleaned_data['state']
   zipcode = form.cleaned_data['zipcode']
   reg = Customer(user=user,name=name, locality=locality, city=city, state=state, zipcode=zipcode)
   reg.save()
   messages.success(request, 'Congrats! Profile Updated')
  return render(request, 'app/profile.html',{'form':form, 'active':'btn-primary', 'totalitem': totalitem})

def search_products(request):
  query = request.GET.get('q', '')
  totalitem = 0
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
  
  if query:
    # Clean the query: strip whitespace and convert to lowercase
    cleaned_query = query.strip()
    
    # Start with an empty queryset for results
    products = Product.objects.none()
    
    # 1. Try exact search (case-insensitive)
    exact_matches = Product.objects.filter(title__icontains=cleaned_query)
    products = products.union(exact_matches)
    
    # 2. Try searching with words split
    search_words = cleaned_query.split()
    for word in search_words:
      if len(word) > 1:  # Ignore very short words
        word_matches = Product.objects.filter(title__icontains=word)
        products = products.union(word_matches)
    
    # 3. Handle cases where query might be combined (e.g., "jeans1" instead of "Jeans 1")
    # Get all products and check if removing spaces from title would match
    all_products = Product.objects.all()
    combined_matches = []
    
    for product in all_products:
      # Remove spaces from product title and query for comparison
      product_no_spaces = product.title.replace(" ", "").lower()
      query_no_spaces = cleaned_query.replace(" ", "").lower()
      
      # Check if the no-space version matches
      if query_no_spaces in product_no_spaces:
        combined_matches.append(product.id)
    
    # Add these matches to our results
    if combined_matches:
      combined_products = Product.objects.filter(id__in=combined_matches)
      products = products.union(combined_products)
  else:
    products = Product.objects.none()
    
  return render(request, 'app/search_results.html', 
    {'products': products, 'query': query, 'totalitem': totalitem})

@login_required
def add_address(request):
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            
            reg = Customer(user=user, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Address added successfully!')
            return redirect('address')
    else:
        form = CustomerProfileForm()
    return render(request, 'app/add_address.html', {'form': form, 'active': 'btn-primary'})

@login_required
def update_address(request, id):
    if request.method == 'POST':
        pi = Customer.objects.get(pk=id)
        form = CustomerProfileForm(request.POST, instance=pi)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address updated successfully!')
            return redirect('address')
    else:
        pi = Customer.objects.get(pk=id)
        form = CustomerProfileForm(instance=pi)
    return render(request, 'app/update_address.html', {'form': form, 'active': 'btn-primary'})

@login_required
def delete_address(request, id):
    if request.method == 'POST':
        try:
            pi = Customer.objects.get(pk=id, user=request.user)
            pi.delete()
            messages.success(request, 'Address deleted successfully!')
        except Customer.DoesNotExist:
            messages.error(request, 'Address not found or you do not have permission to delete it.')
    return redirect('address')