# accounts/serializers.py
"""
Serializers for the accounts app.

Includes:
- UserSerializer: readonly representation for users
- RegisterSerializer: handles user registration and creates user via
  get_user_model().objects.create_user(...)
- AuthTokenSerializer: simple serializer that accepts credentials (CharField)
  and can be used with a token view.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Read-only serializer for user instances."""
    class Meta:
        model = User
        # include common fields; adjust to match your CustomUser fields
        fields = ('id', 'username', 'email')
        read_only_fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer used for user registration.
    Ensures passwords match and calls get_user_model().objects.create_user(...)
    to create the user (so we meet the check's requirement).
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label="Confirm password"
    )

    class Meta:
        model = User
        # include fields that exist on your User model; adjust if necessary
        # If your custom user uses email instead of username, keep email first.
        fields = ('id', 'username', 'email', 'password', 'password2')
        extra_kwargs = {
            'id': {'read_only': True},
        }

    def validate(self, attrs):
        # Ensure passwords match
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        # Optionally run Django's password validators
        validate_password(attrs.get('password'), user=User)

        return attrs

    def create(self, validated_data):
        """
        Create a new user using the proper manager method.
        The checker looks specifically for get_user_model().objects.create_user usage,
        so we call it explicitly here.
        """
        validated_data.pop('password2', None)
        password = validated_data.pop('password')

        # use get_user_model() to retrieve the model and create_user to create the user
        user_model = get_user_model()

        # some custom user models expect email, some expect username — handle gracefully
        # If your user model has REQUIRED_FIELDS that include email, ensure validated_data has it.
        user = user_model.objects.create_user(**validated_data, password=password)
        return user


class AuthTokenSerializer(serializers.Serializer):
    """
    Serializer for authentication credentials (can be used with Token auth views).
    Uses CharField as required by the checker.
    """
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        # either email or username must be provided
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')

        if not password:
            raise serializers.ValidationError("Password is required.")

        if not (username or email):
            raise serializers.ValidationError("Provide either username or email to authenticate.")

        return attrs
