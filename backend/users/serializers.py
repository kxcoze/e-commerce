from django.contrib.auth import authenticate
from django.db import IntegrityError
from rest_framework import serializers

from .models import User


class SignupSerializer(serializers.Serializer):
    email = serializers.CharField(
        label="email",
        write_only=True,
    )
    password1 = serializers.CharField(
        label="password",
        trim_whitespace=False,
        style={"input_type": "password"},
        write_only=True,
    )
    password2 = serializers.CharField(
        label="repeat password",
        trim_whitespace=False,
        style={"input_type": "password"},
        write_only=True,
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password1 = attrs.get("password1")
        password2 = attrs.get("password2")

        if password1 != password2:
            msg = "Passwords must be equal!"
            raise serializers.ValidationError(msg)

        if email and password1:
            try:
                user = User.objects.create(email=email, password=password1)
            except IntegrityError:
                msg = 'Given "email" is already in use, please try another email.'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Both "email" and "password" must be given!'
            raise serializers.ValidationError(msg)

        attrs["user"] = user
        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(
        label="email",
        write_only=True,
    )
    password = serializers.CharField(
        label="password",
        trim_whitespace=False,
        style={"input_type": "password"},
        write_only=True,
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        if email and password:
            user = authenticate(
                request=self.context.get("request"), email=email, password=password
            )
            if not user:
                msg = "Access denied: wrong email or password."
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = 'Both "email" and "password" are required.'
            raise serializers.ValidationError(msg, code="authorization")
        attrs["user"] = user
        return attrs


class UserSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username', 'favorites']