from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Profile, Restaurant
from django.contrib.auth.hashers import make_password
from datetime import timedelta, timezone

User = get_user_model()

# -- -- -- -- -- -- -- -- -- --
class ProfileSerializer(serializers.ModelSerializer):
    pin_code = serializers.CharField(write_only=True, required=False)
    class Meta: 
        model  = Profile 
        fields = ['avatar', 'pin_code', 'phone', 'pasport']

# -- -- -- -- -- -- -- -- -- --
class UserSerializer(serializers.ModelSerializer):
    # profile = ProfileSerializer(read_only=True, required=False, allow_null=True)
    class Meta:
        model  = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name'] 

    def get_profile_data(self, obj):
        if hasattr(obj, 'profile') and obj.profile:
            return ProfileSerializer(obj.profile).data
        return None

# -- -- -- -- -- -- -- -- -- --
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, max_length=12)
    password2 = serializers.CharField(write_only=True, min_length=8, max_length=12)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 
                  'password2', 'first_name', 'last_name']
    # -- -- -- -- --
    def validate(self, data): # data user tomonidan kiritilgan ma'lumot
        if data['password'] != data['password2']:
            raise serializers.ValidationError({
                'message': 'Parollar mos kelmadi'
            })
        return data
    
    # -- -- -- -- --
    def create(self, validated_data): # bu yuqoridagi datani is_valid()dan o'tgani
        validated_data.pop('password2')

        password = validated_data.pop('password')
        user = User(**validated_data) # dict -> userobject
        user.set_password(password) #hashed
        user.save()

        return user

# -- -- -- -- -- -- -- -- -- -- for login
class MytokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
    
        token['username'] = user.username
        token['email']    = user.email
        token['role']     = user.profile.role if hasattr(user, 'profile') else None

        return token 
    
    # -- -- -- -- --
    def validate(self, attrs): # attrs userdan kelgan hom input
        data = super().validate(attrs) # super() uni tekshirib token qo'shadi
        data['user'] = UserSerializer(self.user).data
        return data

# -- -- -- -- -- -- -- -- -- -- 
class RestaurantSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model  = Restaurant
        fields = ['id', 'name', 'address', 'password', 'created_at']
    
    # -- -- -- -- --
    def create(self, validated_data):
        password = validated_data.pop('password')
        restaurant = Restaurant(**validated_data) # unpacking qilindi. password'dan boshqa
        restaurant.password = make_password(password) # hashlaymiz
        # 3kunlik trial yangi mijoz uchun
        restaurant.paid_until = timezone.now() + timedelta(days=5)
        restaurant.is_active = True

        restaurant.save() # saqlaymiz
        
        return restaurant
