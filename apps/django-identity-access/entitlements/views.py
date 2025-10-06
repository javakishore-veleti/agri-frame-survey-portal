# apps/django-identity-access/entitlements/views.py

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, viewsets, filters
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken

from .models import Tenant, Role, UserTenant, UserRole
from .serializer import (
    TenantSerializer,
    RoleSerializer,
    UserTenantSerializer,
    UserRoleSerializer,
)

from django.http import JsonResponse
from jwt.utils import base64url_encode
from cryptography.hazmat.primitives import serialization
from django.conf import settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken, UntypedToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

User = get_user_model()


# -------------------------------------------------------------------
# Permissions
# -------------------------------------------------------------------
class IsEntitlementsAdmin(BasePermission):
    """
    Simple gate for write access: user must be authenticated AND
    be staff/superuser. Adjust to tenant-scoped rules as needed.
    """
    def has_permission(self, request, view) -> bool:
        u = request.user
        return bool(u and u.is_authenticated and (u.is_staff or u.is_superuser))


# -------------------------------------------------------------------
# A minimal Hyperlinked serializer for auth.User so `user-detail`
# links in your other serializers resolve without extra wiring.
# Move this to entitlements/serializers.py later if you prefer.
# -------------------------------------------------------------------
class UserHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=False)

    class Meta:
        model = User
        fields = [
            "url", "id", "username", "email",
            "first_name", "last_name",
            "is_active", "is_staff", "is_superuser",
            "last_login", "date_joined",
            "password",
        ]
        extra_kwargs = {
            "url": {"view_name": "user-detail"},
            "email": {"required": True},
            "username": {"required": False},
        }

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        if not validated_data.get("username"):
            validated_data["username"] = validated_data.get("email")
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            # generate unusable password if none provided
            user.set_unusable_password()
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for k, v in validated_data.items():
            setattr(instance, k, v)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


# -------------------------------------------------------------------
# ViewSets
# -------------------------------------------------------------------
class TenantViewSet(viewsets.ModelViewSet):
    """
    /api/admin/v1/tenants
    """
    queryset: QuerySet[Tenant] = Tenant.objects.all().order_by("id")
    serializer_class = TenantSerializer
    permission_classes = [IsAuthenticated & IsEntitlementsAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["code", "active", "status"]
    search_fields = ["name", "code", "contact_email", "unique_reference_id"]
    ordering_fields = ["id", "name", "code", "created_on", "updated_on"]


class RoleViewSet(viewsets.ModelViewSet):
    """
    /api/admin/v1/roles
    """
    queryset: QuerySet[Role] = Role.objects.all().order_by("id")
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated & IsEntitlementsAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["tenant_code", "status"]
    search_fields = ["id", "label", "tenant_code", "unique_reference_id"]
    ordering_fields = ["id", "label", "created_on", "updated_on"]


class UserTenantViewSet(viewsets.ModelViewSet):
    """
    /api/admin/v1/user-tenants
    """
    queryset: QuerySet[UserTenant] = (
        UserTenant.objects.select_related("user", "tenant").all().order_by("id")
    )
    serializer_class = UserTenantSerializer
    permission_classes = [IsAuthenticated & IsEntitlementsAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["tenant", "user", "status"]
    search_fields = [
        "tenant__code", "tenant__name",
        "user__username", "user__email",
        "unique_reference_id",
    ]
    ordering_fields = ["id", "tenant", "created_on", "updated_on"]


class UserRoleViewSet(viewsets.ModelViewSet):
    """
    /api/admin/v1/user-roles
    """
    queryset: QuerySet[UserRole] = (
        UserRole.objects.select_related("user", "role").all().order_by("id")
    )
    serializer_class = UserRoleSerializer
    permission_classes = [IsAuthenticated & IsEntitlementsAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["tenant_code", "role", "user", "status"]
    search_fields = [
        "tenant_code", "role__id", "role__label",
        "user__username", "user__email",
        "unique_reference_id",
    ]
    ordering_fields = ["id", "role", "user", "created_on", "updated_on"]


class UserViewSet(viewsets.ModelViewSet):
    """
    /api/admin/v1/users
    Hyperlinked endpoint for Django auth users (for admin ops).
    """
    queryset: QuerySet[User] = User.objects.all().order_by("id")
    serializer_class = UserHyperlinkedSerializer
    permission_classes = [IsAuthenticated & IsEntitlementsAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["is_active", "is_staff", "is_superuser"]
    search_fields = ["username", "email", "first_name", "last_name"]
    ordering_fields = ["id", "email", "username", "date_joined", "last_login"]


def jwks(request):
    key = serialization.load_pem_private_key(
        settings.SIMPLE_JWT["SIGNING_KEY"].encode(), password=None
    )
    public_key = key.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo
    )
    pub_numbers = key.public_key().public_numbers()
    jwk = {
        "kty": "RSA",
        "alg": "RS256",
        "use": "sig",
        "n": base64url_encode(pub_numbers.n.to_bytes((pub_numbers.n.bit_length() + 7) // 8, "big")).decode(),
        "e": base64url_encode(pub_numbers.e.to_bytes((pub_numbers.e.bit_length() + 7) // 8, "big")).decode(),
        "kid": "agri-rs256-key",
    }
    return JsonResponse({"keys": [jwk]})


import jwt
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def whoami(request):
    """
    Diagnostic endpoint: show authenticated user and decoded JWT claims.
    Works no matter what request.auth contains.
    """
    auth_header = request.headers.get("Authorization", "")
    token_value = auth_header.replace("Bearer ", "").strip()
    claims = {}

    if token_value:
        try:
            claims = jwt.decode(
                token_value,
                settings.SIMPLE_JWT["VERIFYING_KEY"],
                algorithms=[settings.SIMPLE_JWT["ALGORITHM"]],
            )
        except jwt.ExpiredSignatureError:
            claims = {"error": "Token expired"}
        except jwt.InvalidTokenError as e:
            claims = {"error": f"Invalid token: {str(e)}"}

    return Response(
        {
            "user": str(request.user),
            "claims": claims,
        }
    )
