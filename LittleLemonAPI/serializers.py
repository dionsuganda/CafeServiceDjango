from rest_framework import serializers
from .models import MenuItem, Category, Cart, Order, OrderItem
from django.contrib.auth.models import User, Group
from rest_framework.fields import CurrentUserDefault
from rest_framework.validators import UniqueTogetherValidator

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    # category = CategorySerializer
    category = CategorySerializer
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']

class CartSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer
    price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price']

    validators = [
        UniqueTogetherValidator(
            queryset=Cart.objects.all(),
            fields=['user', 'menuitem']
        )
    ]
    
    def create(self, validated_data):
        return Cart.objects.create(
            user = validated_data['user'],
            menuitem = validated_data['menuitem'],
            quantity = validated_data['quantity'],
            unit_price = validated_data['unit_price'],
            price = validated_data['quantity']*validated_data['unit_price'],
        )

class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer
    price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'menuitem', 'quantity', 'unit_price', 'price']

    validators = [
        UniqueTogetherValidator(
            queryset=OrderItem.objects.all(),
            fields=['order', 'menuitem']
        )
    ]
    
    def create(self, validated_data):
        return OrderItem.objects.create(
            order = validated_data['order'],
            menuitem = validated_data['menuitem'],
            quantity = validated_data['quantity'],
            unit_price = validated_data['unit_price'],
            price = validated_data['quantity']*validated_data['unit_price'],
        )
    
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date']
        
    def create(self, validated_data):
        return Order.objects.create(
            user = validated_data['user'],
            total = self.context.get('request').data['price'],
            date = validated_data['date']
        )