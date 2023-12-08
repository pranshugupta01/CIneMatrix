from rest_framework import serializers
from django.contrib.auth.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    confirmPassword = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )

    class Meta:
        model = User
        fields = ["email", "username", "password", "confirmPassword"]
        extra_kwargs = {"confirmPassword": {'write_only': True}}

    def save(self):
        
        password= self.validated_data['password']
        confirmPassword= self.validated_data['confirmPassword']
        
        if password!=confirmPassword:
            raise serializers.ValidationError({"error" : "password and confirmPassword should be the same"})
        
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({"error" : "email already exists"})

        account= User(email=self.validated_data['email'],username=self.validated_data['username'])
        account.set_password(password)
        account.save()
        return account