from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category, Product,Order,OrderItem

User = get_user_model()


class SlugRelatedField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(slug=data)
        except self.queryset.model.DoesNotExist:
            raise serializers.ValidationError("Object with this slug does not exist.")

    def to_representation(self, value):
        return value
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['slug','name']

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['slug', 'name', 'description', 'price', 'category','date_created']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many =False)
    class Meta:
        model = OrderItem
        fields = ['slug','product', 'quantity','date_created']
    


class OrderSerializer(serializers.ModelSerializer):
    #order_items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = '__all__'




class OrderHistorySerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['slug', 'date_created', 'order_items']