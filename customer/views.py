from django.shortcuts import render

from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework import authentication,permissions


from customer.serializers import UserSerializer, ItemsSerializer, CartSerializer, OrderSerializer, ReviewSerializer
from customer.models import MenuItems, Category, Carts, Order, Reviews

# Create your views here.

class UsersView(viewsets.GenericViewSet,mixins.CreateModelMixin):  # we dont need full CRUD,only need POST method so no ModelViewset
    serializer_class=UserSerializer
    queryset=User.objects.all()



class ItemsView(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin):
    serializer_class=ItemsSerializer
    queryset=MenuItems.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        qs = MenuItems.objects.all()
        if 'categories' in self.request.query_params: #query_params is the  ? in the url
            cat = self.request.query_params.get('categories')
            qs=qs.filter(category__cat_name=cat)
        return qs




    @action(methods=['POST'],detail=True)
    def add_to_cart(self,request,*args,**kwargs):
        serializer = CartSerializer(data=request.data)
        item_obj = MenuItems.objects.get(id=kwargs.get('pk'))
        user = request.user
        if serializer.is_valid():
            serializer.save(item = item_obj,user=user)
            return Response(data=serializer.data)
        return Response(data=serializer.errors)
        

    @action(methods=['POST'],detail=True)
    def place_order(self, request,*args,**kwargs):
        serializer = OrderSerializer(data=request.data)
        item_obj = MenuItems.objects.get(id=kwargs.get('pk')) 
        user = request.user
        if serializer.is_valid():
            serializer.save(item = item_obj ,user=user)
            return Response(data=serializer.data)
        return Response(data=serializer.errors)
    


    @action(methods=['POST'],detail=True)
    def add_review(self,request,*args,**kwargs):
        serializer = ReviewSerializer(data=request.data)
        item_obj = MenuItems.objects.get(id=kwargs.get('pk'))
        user = request.user
        if serializer.is_valid():
            serializer.save(item = item_obj ,user=user)
            return Response(data=serializer.data)
        return Response(data=serializer.errors)

    @action(methods=['get'],detail=False)
    def categories(self,request,*args,**kwargs):
        cats=Category.objects.all().values_list('cat_name',flat=True)
        return Response(data=cats)


class CartsView(viewsets.GenericViewSet,mixins.ListModelMixin):
    serializer_class = CartSerializer
    queryset=Carts.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        return Carts.objects.filter(user=self.request.user)   # to list only loginned user cartlist


    



class OrdersView(viewsets.GenericViewSet,mixins.ListModelMixin):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user = self.request.user)





