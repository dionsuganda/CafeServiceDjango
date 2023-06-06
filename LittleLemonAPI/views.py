from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status, generics
from rest_framework.views import APIView
from django.shortcuts import redirect
from django.contrib.auth.models import User, Group
from .models import MenuItem, Category, Cart, Order, OrderItem
from . import models
from .serializers import MenuItemSerializer, CategorySerializer, CartSerializer, OrderSerializer, OrderItemSerializer
from django.core.paginator import Paginator, EmptyPage
import datetime
from json import JSONEncoder
# Create your views here.

@api_view(['GET', 'POST'])
def secret(request):
    return Response('secret menu', status=status.HTTP_200_OK)

@api_view()
@permission_classes([IsAuthenticated])
def me(request):
    return Response(request.user.email)

@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    return Response({'message': request.user.groups.filter(name='Manager')})
    if request.user.groups.filter(name='Manager').exists():
        return Response({'message': 'Only manager can view this page.'})
    else:
        return Response({'message': 'You are not authorized'}, 403)
    
@api_view(['PUT'])
def login(request):
    response = redirect('/auth/token/login')
    return response

@api_view(['PUT'])
def logout(request):
    response = redirect('/auth/token/logout')
    return response

@permission_classes([IsAdminUser])
class AssignUser(APIView):
    def put(self, request):
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            manager = Group.objects.get(name=request.data['group']) 
            manager.user_set.add(user)
            return Response({'message':'Successfully added user to group.'})
        
        return Response({'message':'Failed added user to group.'}) 
    
    def delete(self, request):
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            manager = Group.objects.get(name=request.data['group']) 
            manager.user_set.remove(user)
            return Response({'message':'Successfully remove user to group.'})
        
        return Response({'message':'Failed remove user to group.'}) 

@permission_classes([IsAdminUser])
class CategoryItem(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
@permission_classes([IsAdminUser])
class SingleCategoryItem(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
@permission_classes([IsAdminUser])
class MenuItem(generics.ListCreateAPIView):
    queryset = models.MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer

@permission_classes([IsAdminUser])
class SingleMenuItem(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = models.MenuItem.objects.all()

@api_view()
@permission_classes([IsAuthenticated])
def menu_items(request):
    items = models.MenuItem.objects.select_related('category').all()
    category_name = request.query_params.get('category')
    to_price = request.query_params.get('to_price')
    search = request.query_params.get('search')
    perpage = request.query_params.get('perpage', default=2)
    page = request.query_params.get('page', default=1)
    if category_name:
        items = items.filter(category=category_name)
    if to_price:
        items = items.filter(price__lte=to_price)
    if search:
        items = items.filter(title__startswith=search)

    paginator = Paginator(items, per_page=perpage)
    try:
        items = paginator.page(number=page)
    except:
        items = []
    serialized_item = MenuItemSerializer(items, many=True)
    return Response(serialized_item.data)

@permission_classes([IsAuthenticated])
class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.select_related('menuitem').all()
    serializer_class = CartSerializer

@permission_classes([IsAuthenticated])
class FlushCartView(APIView):
    def delete(self, request):
        user_id = request.data['user_id']
        if user_id:
            # cart = get_object_or_404(Cart, user=user_id)
            cart = Cart.objects.filter(user=user_id)
            cart.delete()
            # cart.all().delete()
            return Response({'message':'Successfully delete cart'})
        
        return Response({'message':'Failed delete cart'}) 

@permission_classes([IsAdminUser])
class OrderView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

@permission_classes([IsAdminUser])
class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
     
@permission_classes([IsAuthenticated])
class OrderItemView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.select_related('menuitem').all()
    serializer_class = OrderItemSerializer
    
    def post(self, request):
        quantity = request.data.get('quantity')
        unit_price = request.data.get('unit_price')
        total = int(quantity) * int(unit_price)
        data = Order.objects.create(
            user=request.user,
            total= total,
            date=datetime.date.today()
        )
        
        return Response({'status':'success', 'message' : 'success'})
    

