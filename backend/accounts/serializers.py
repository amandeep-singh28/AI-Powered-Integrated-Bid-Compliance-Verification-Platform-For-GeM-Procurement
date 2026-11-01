
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(
        write_only=True,
        required=True
    )

    requested_role = serializers.ChoiceField(
        choices=[
            ("BIDDER", "Bidder"),
            ("TENDER_MANAGER", "Tender Manager"),
            ("REVIEWER", "Reviewer"),
        ],
        required=True
    )

    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password",
            "confirm_password",
            "requested_role",
        ]

        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "email": {"required": True},
            "phone_number": {"required": True},
            "password": {
                "write_only": True,
                "min_length": 8
            },
        }

    def validate_email(self, value):

        value = value.strip().lower()

        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "This email is already registered."
            )

        return value

    def validate_phone_number(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Phone number is required."
            )

        return value

    def validate(self, data):

        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({
                "confirm_password": "Passwords do not match."
            })

        return data

    def create(self, validated_data):

        validated_data.pop("confirm_password")

        password = validated_data.pop("password")

        requested_role = validated_data.pop("requested_role")

        user = User.objects.create_user(
            password=password,
            role=User.Role.BIDDER,
            requested_role=requested_role,
            role_request_status=User.RoleRequestStatus.PENDING,
            is_profile_complete=False,
            is_active=True,
            **validated_data
        )

        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):

        data = super().validate(attrs)

        data["user"] = {
            "id": self.user.id,
            "email": self.user.email,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "phone_number": self.user.phone_number,
            "role": self.user.role,
            "requested_role": self.user.requested_role,
            "role_request_status": self.user.role_request_status,
            "is_profile_complete": self.user.is_profile_complete,
        }

        return data
