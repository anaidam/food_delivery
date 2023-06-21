from rest_framework import serializers
from django.contrib.auth.models import User
from customer.models import MenuItems, Category, Carts, Order, Reviews


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email','password']

    def create(self, validated_data):   
        return User.objects.create_user(**validated_data)  # to hash password- overriding create method


class ReviewSerializer(serializers.ModelSerializer):
        item = serializers.CharField(read_only=True)
        user = serializers.CharField(read_only=True)

        class Meta:
            model = Reviews
            fields = '__all__'



class ItemsSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    reviews = ReviewSerializer(read_only = True,many=True)
    class Meta:
        model = MenuItems
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    item = ItemsSerializer(read_only = True)
    user = serializers.CharField(read_only=True)
    created_date = serializers.CharField(read_only=True)

    class Meta:
        model = Carts
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    item = ItemsSerializer(read_only=True)
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'



