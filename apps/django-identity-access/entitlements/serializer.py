# apps/django-identity-access/entitlements/serializers.py

from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Tenant, Role, UserTenant, UserRole

User = get_user_model()


class TenantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tenant
        fields = "__all__"
        extra_kwargs = {
            "url": {"view_name": "tenant-detail"},
        }


class RoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"
        extra_kwargs = {
            "url": {"view_name": "role-detail"},
        }


class UserTenantSerializer(serializers.HyperlinkedModelSerializer):
    # Link related resources as hyperlinks (writeable via queryset)
    user = serializers.HyperlinkedRelatedField(
        queryset=User.objects.all(),
        view_name="user-detail",
    )
    tenant = serializers.HyperlinkedRelatedField(
        queryset=Tenant.objects.all(),
        view_name="tenant-detail",
    )

    class Meta:
        model = UserTenant
        fields = "__all__"
        extra_kwargs = {
            "url": {"view_name": "usertenant-detail"},
        }


class UserRoleSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        queryset=User.objects.all(),
        view_name="user-detail",
    )
    role = serializers.HyperlinkedRelatedField(
        queryset=Role.objects.all(),
        view_name="role-detail",
    )
    # tenant_code is a simple CharField on the model → included automatically

    class Meta:
        model = UserRole
        fields = "__all__"
        extra_kwargs = {
            "url": {"view_name": "userrole-detail"},
        }
