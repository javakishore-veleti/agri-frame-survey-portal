# apps/django-identity-access/entitlements/models_base.py

from __future__ import annotations

import threading
from uuid import uuid4

from django.conf import settings
from django.db import models


# -----------------------------------------------------------------------------
# Thread-local current user helpers (used by AppBaseDomainAudited.save)
# -----------------------------------------------------------------------------
_current = threading.local()


def set_current_user(user) -> None:
    """Set the current request user in thread-local storage (see middleware)."""
    _current.user = user


def get_current_user_id(default=None):
    """Return current user's id if available, else default."""
    try:
        u = getattr(_current, "user", None)
        return getattr(u, "id", default)
    except Exception:
        return default


# -----------------------------------------------------------------------------
# Common enums / defaults
# -----------------------------------------------------------------------------
class AppStatusChoices(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"
    IN_ACTIVE = "IN_ACTIVE", "Inactive"  # alias for compatibility with prior naming
    SUSPENDED = "SUSPENDED", "Suspended"


def default_unique_ref() -> str:
    """Generate a short, uppercase unique reference (25 chars)."""
    return uuid4().hex[:25].upper()


# -----------------------------------------------------------------------------
# Base domains
# -----------------------------------------------------------------------------
class AppBaseDomain(models.Model):
    """
    Minimal base: status + unique_reference_id with sane defaults and ordering.
    """

    status = models.CharField(
        choices=AppStatusChoices.choices,
        default=AppStatusChoices.INACTIVE,
        db_column="status",
        max_length=25,
        db_index=True,
    )
    unique_reference_id = models.CharField(
        db_column="unique_reference_id",
        max_length=25,
        null=True,
        blank=True,
        default=default_unique_ref,
        unique=True,
    )

    class Meta:
        abstract = True
        ordering = ("-id",)  # replace with your AppConstants.DEFAULT_ORDER_BY_FIELDS if desired


class AppBaseDomainAudited(AppBaseDomain):
    """
    Audited base: adds created/updated timestamps and by-whom (FK to User).

    Note: created_by/updated_by are auto-populated from thread-local current user.
    See `entitlements/middleware.py` (CurrentUserMiddleware) and add it after
    AuthenticationMiddleware so `request.user` is available per request.
    """

    created_on = models.DateTimeField(db_column="created_on", auto_now_add=True, null=True, db_index=True)
    updated_on = models.DateTimeField(db_column="updated_on", auto_now=True, null=True, db_index=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        db_column="created_by",
        related_name="created_%(class)s_set",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        db_column="updated_by",
        related_name="updated_%(class)s_set",
    )

    class Meta(AppBaseDomain.Meta):
        abstract = True

    def save(self, *args, **kwargs):
        uid = get_current_user_id()
        # Set created_by once; always bump updated_by
        if not self.pk and not self.created_by_id:
            self.created_by_id = uid
        self.updated_by_id = uid
        super().save(*args, **kwargs)


class AppBaseDomainNameDesc(AppBaseDomainAudited):
    """
    Optional convenience base adding name/description to the audited base.
    """

    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(null=True, blank=True)

    class Meta(AppBaseDomainAudited.Meta):
        abstract = True
