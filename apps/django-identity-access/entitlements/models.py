# apps/django-identity-access/entitlements/models.py

from __future__ import annotations

from django.conf import settings
from django.contrib.auth.models import Permission
from django.db import models

from .models_base import AppBaseDomainAudited


class Tenant(AppBaseDomainAudited):
    """
    A top-level organization (e.g., USDA FPAC, NRCS, Partner org).
    """
    name = models.CharField(max_length=255, db_index=True)
    code = models.CharField(max_length=64, unique=True, db_index=True)
    active = models.BooleanField(default=True)
    contact_email = models.EmailField(null=True, blank=True)
    settings = models.JSONField(null=True, blank=True)

    class Meta(AppBaseDomainAudited.Meta):
        db_table = "tenant"
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["active"]),
        ]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.name} ({self.code})"


class Role(AppBaseDomainAudited):
    """
    Permission bundle.
    If tenant_code is NULL => global role; otherwise role is scoped to that tenant.
    Examples: SYSTEM_ADMIN, TENANT_ADMIN, SURVEY_MANAGER, SURVEYOR, DATA_STEWARD, FARMER, VIEWER.
    """
    id = models.CharField(primary_key=True, max_length=64)
    label = models.CharField(max_length=128)
    tenant_code = models.CharField(max_length=64, null=True, blank=True, db_index=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    class Meta(AppBaseDomainAudited.Meta):
        db_table = "role"
        indexes = [
            models.Index(fields=["tenant_code"]),
            models.Index(fields=["label"]),
        ]

    def __str__(self) -> str:  # pragma: no cover
        return self.id


class UserTenant(AppBaseDomainAudited):
    """
    Optional 'primary tenant' mapping for a user.
    Keep this if you want a single canonical tenant per user (for UX/routing),
    while still allowing multi-tenant access via UserRole.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tenant_link",
        db_index=True,
    )
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.PROTECT,
        related_name="users",
        db_index=True,
    )

    class Meta(AppBaseDomainAudited.Meta):
        db_table = "user_tenant"
        indexes = [
            models.Index(fields=["tenant"]),
        ]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.user_id} -> {self.tenant.code}"


class UserRole(AppBaseDomainAudited):
    """
    User ↔ Role assignment (optionally tenant-scoped).
    Unique per (user, role, tenant_code).
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="role_links",
        db_index=True,
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name="user_links",
        db_index=True,
    )
    tenant_code = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        db_index=True,
        help_text="When set, this role assignment applies only within that tenant.",
    )

    class Meta(AppBaseDomainAudited.Meta):
        db_table = "user_role"
        unique_together = ("user", "role", "tenant_code")
        indexes = [
            models.Index(fields=["tenant_code"]),
            models.Index(fields=["user", "tenant_code"]),
        ]

    def __str__(self) -> str:  # pragma: no cover
        scope = self.tenant_code or "GLOBAL"
        return f"{self.user_id} -> {self.role_id} [{scope}]"
