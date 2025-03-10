from rest_framework import serializers
from .models import Note
from django.contrib.auth.models import User


from rest_framework import serializers
from django.contrib.auth.models import User  # Assuming you're using Django's default User model

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  #  Ensures password is only used for input, not output

    class Meta:
        model = User  #  Specifies that this serializer is for the `User` model
        fields = ['username', 'email', 'password']  #  Defines the fields that should be included

    def create(self, validated_data):
        #  Create a new user instance with username and email
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        
        #  Hash the password before saving (prevents storing raw passwords in DB)
        user.set_password(validated_data['password'])

        #  Save the user to the database
        user.save()

        return user  # 🔹 Return the newly created user



class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model =User 
        fields=['username']
