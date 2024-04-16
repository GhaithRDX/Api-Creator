from rest_framework import serializers
from dynamic_models.models import ModelSchema
from .models import Modelnames,CustomUser,Projects
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email','first_name', 'last_name','profile_picture')
        # fields = '__all__'



class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Ensure password is write-only

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'first_name', 'last_name','profile_picture'
                  ,'co_owner','read_P','write_P','user1','user2')

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            profile_picture=validated_data['profile_picture'],
            co_owner=validated_data['co_owner'],
            read_P =validated_data['read_P'],
            write_P=validated_data['write_P'],
            user1=validated_data['user1'],
            user2=validated_data['user2']
            
        )
        user.set_password(validated_data['password'])
        user.save()
        return user   
    
    
class models_S(serializers.ModelSerializer):
    class Meta:
        model = Modelnames
        fields = "__all__"

class projects_S(serializers.ModelSerializer):
    class Meta:
        model =Projects
        fields = "__all__"

def dynamic_serializer(model_class):
    class Stest(serializers.ModelSerializer):
        class Meta:
            model = model_class
            fields = "__all__"

    return Stest

class DynamicModelFieldSerializer(serializers.Serializer):
    name = serializers.CharField()
    data_type = serializers.CharField()
    max_length = serializers.IntegerField()
    null = serializers.BooleanField()
    unique = serializers.BooleanField()
    related_model =serializers.CharField()