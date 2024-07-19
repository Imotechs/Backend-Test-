from django.urls import path
from rest_framework_simplejwt.views import  TokenRefreshView
from .views import CustomTokenObtain,UserRegistrationView,ProductView,CategoryView,OrderView

urlpatterns = [
     # JWT views
    path("token/", CustomTokenObtain.as_view(), name="token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh-token"),

    # other views
    path("register/", UserRegistrationView.as_view()),
    #products urls
    path('inventory/products/',ProductView.as_view()),# list all products
    path('inventory/product/create/',ProductView.as_view()),#Create a new  product
    path('inventory/product/<str:slug>/',ProductView.as_view()),#detail view of a single product
    path('inventory/product/<str:slug>/update/',ProductView.as_view()),# update a product
    path('inventory/product/<str:slug>/delete/',ProductView.as_view()),#delete a product
    #category urls
    path('inventory/categories/',CategoryView.as_view()),#list all categories
    path('inventory/category/<str:slug>/',CategoryView.as_view()),#list category item
    path('inventory/category/create/',CategoryView.as_view()),#create a category item
    #Order view
    path('inventory/order/create/',OrderView.as_view()),# create order
    path('inventory/order-history/',OrderView.as_view()),# all user order history
    path('inventory/order/<str:slug>/history/',OrderView.as_view()),# single user order history
]