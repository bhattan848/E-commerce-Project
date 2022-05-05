from django.shortcuts import render,redirect
from .models import *
# Create your views here.
from django.views.generic import View



class BaseView(View):
	views = {}


class HomeView(BaseView):
	def get(self,request):
		self.views['categories'] = Category.objects.all()
		self.views['subcategories'] = SubCategory.objects.all()
		self.views['sliders'] = Slider.objects.all()
		self.views['ads'] = Ad.objects.all()
		self.views['products'] = Product.objects.filter(stock = 'In Stock')
		self.views['sale_products'] = Product.objects.filter(labels = 'sale', stock = 'In Stock')
		self.views['hot_products'] = Product.objects.filter(labels = 'hot',stock = 'In Stock')
		self.views['new_products'] = Product.objects.filter(labels = 'new')

		return render(request,'shop-index.html',self.views)





class DetailView(BaseView):
	def get(self,request,slug):
		self.views['product_detail'] = Product.objects.filter(slug = slug)
		
		return render(request,'shop-item.html',self.views)


class CategoryView(BaseView):
	def get(self,request,slug):
		cat_id = Category.objects.get(slug = slug).id
		cat_name = Category.objects.get(slug = slug).name
		self.views['cat_name']= cat_name
		self.views['subcategories'] = SubCategory.objects.filter(category_id = cat_id)
		self.views['category_products'] = Product.objects.filter(category_id = cat_id)

		return render(request, 'category.html', self.views)

class SubCategoryView(BaseView):
	def get(self,request,slug):
		subcat_id = SubCategory.objects.get(slug = slug).id
		subcat_name = Category.objects.get(slug = slug).name
		self.views['subcat_name']= subcat_name
		self.views['subcategory_products'] = Product.objects.filter(subcategory_id = subcat_id)

		return render(request, 'subcategory.html', self.views)

from django.db.models import Q
class SearchView(BaseView):
	def get(self,request):
		if request.method == 'GET':
			query = request.GET['query']
			#self.views['search_product'] = Product.objects.filter(name_icontains = query) | (description_icontains = query)
			lookups = Q(name__icontains = query) | Q(description__icontains = query)
			self.views['search_product'] = Product.objects.filter(lookups).distinct()
			self.views['search_for'] = query
		return render(request,'shop-search-result.html',self.views)

from django.contrib import messages
from django.contrib.auth.models import User
def signup(request):
	if request.method == "POST":
		first_name = request.POST['fname']
		last_name = request.POST['lname']
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		cpassword = request.POST['cpassword']
		if password == cpassword:
			if User.objects.filter(username = username).exists():
				messages.error(request,'The username is already used')
				return render(request,'shop-standart-forms.html')

			elif User.objects.filter(email = email).exists():
				
				messages.error(request,'The email is already used')
				return render(request,'shop-standart-forms.html')
			else:
				user = User.objects.create_user(
					first_name = first_name,
					last_name = last_name,
					username = username,
					email = email,
					password = password
					)
				user.save()
		else:
			messages.error(request,'The password does not match')
			return render(request,'shop-standart-forms.html')
	return render(request,'shop-standart-forms.html')


def contact(request):
	if request.method== 'POST':
		name = request.POST['name']
		email = request.POST['email']
		message = request.POST['message']
		print(name,email,message)
		contact = Contact(
			name = name, 
			email = email, 
			message = message
			)
		contact.save()
				
		return render(request,'shop-contacts.html')

	else:
		return render(request,'shop-contacts.html')

def cart(request,slug):
	if Cart.objects.filter(slug = slug, user = request.user.username,checkout = False).exists():
		quantity = Cart.objects.get(slug = slug, user = request.user.username,checkout = False).quantity
		quantity = quantity +1
		Cart.objects.filter(slug = slug, user = request.user.username,checkout = False).update(quantity= quantity)
	else:
		username = request.user.username
		data = Cart.objects.create(
			user = username,
			slug = slug,
			items = Product.objects.filter(slug = slug)[0]
			)
		data.save()

	return redirect('/mycart')

def deletecart(request,slug):
	if Cart.objects.filter(slug = slug, user = request.user.username,checkout = False).exists():
		Cart.objects.get(slug = slug, user = request.user.username,checkout = False).delete()

	return redirect('/mycart')

def decreasecart(request,slug):
	if Cart.objects.filter(slug = slug, user = request.user.username,checkout = False).exists():
		quantity = Cart.objects.get(slug = slug, user = request.user.username,checkout = False).quantity
		if quantity>1:
			quantity = quantity -1
			Cart.objects.filter(slug = slug, user = request.user.username,checkout = False).update(quantity= quantity)
	return redirect('/mycart')


class CartView(BaseView):
	def get(self,request):
		self.views['cart_product'] = Cart.objects.filter(user = request.user.username,checkout = False)
		return render(request,'shop-shopping-cart.html',self.views)
		
#------------------------------------API------------------------------------------------------------------------------------------
from rest_framework import serializers, viewsets
from.serializers import *
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter,SearchFilter


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductFilterViewSet(generics.ListAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer

	filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
	filter_fields = ['id','name','price','labels','category','subcategory']
	ordering_fields = ['price','id','name']
	search_fields = ['name','description']