from genius_plaza import models
from rest_framework import serializers
import re


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        label='Password',
        required=False,
        max_length=32,
        allow_blank=True,
        write_only=True,
        style={'input_type': 'password', 'placeholder': 'Password'},
    )
    password_confirmation = serializers.CharField(
        label='Password (confirmation)',
        required=False,
        max_length=32,
        allow_blank=True,
        write_only=True,
        style={'input_type': 'password', 'placeholder': 'Password (confirmation)'},
    )
    is_active = serializers.BooleanField(
        label='Is active',
        required=True,
        initial=True
    )

    class Meta:
        model = models.User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'password', 'password_confirmation', 'is_active', 'created', 'modified')
        # fields = '__all__'
        # extra_kwargs = {'password': {'write_only': True}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate_username(self, username):
        if re.match('^[a-z0-9_]+$', username):
            return username
        else:
            raise serializers.ValidationError(
                'Letters, digits and _ only.'
            )

    def validate_password(self, password):
        if len(password) >= 3:
            return password
        else:
            if self.instance is not None and password is '':
                return password
            else:
                raise serializers.ValidationError(
                    'Ensure this field has at least 3 characters.'
                )

    def validate_password_confirmation(self, password_confirmation):
        if password_confirmation != self.initial_data['password']:
            raise serializers.ValidationError(
                'The password and your confirmation do not match.'
            )
        return password_confirmation

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        instance = models.User.objects.create(**validated_data)
        instance.encrypt_password(password=validated_data.pop('password'))
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        password = validated_data.get('password')
        if password is not '':
            instance.encrypt_password(password=validated_data.get('password', ''))
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Recipe
        fields = ('id', 'name', 'user', 'steps', 'ingredients')


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Step
        fields = ('id', 'step_text')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ingredient
        fields = ('id', 'text')
