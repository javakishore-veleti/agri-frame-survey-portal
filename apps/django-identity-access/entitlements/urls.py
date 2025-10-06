from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .auth_tokens import AgrTokenObtainPairSerializer

from .views import (
    TenantViewSet,
    RoleViewSet,
    UserTenantViewSet,
    UserRoleViewSet,
    UserViewSet, jwks, whoami,
)

app_name = "entitlements"

class AgrTokenObtainPairView(TokenObtainPairView):
    serializer_class = AgrTokenObtainPairSerializer

router = DefaultRouter()
router.register(r"tenants", TenantViewSet, basename="tenant")
router.register(r"roles", RoleViewSet, basename="role")
router.register(r"user-tenants", UserTenantViewSet, basename="usertenant")
router.register(r"user-roles", UserRoleViewSet, basename="userrole")
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    # CRUD endpoints
    path("", include(router.urls)),

    # JWT auth
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("jwks/", jwks, name="jwks"),
    path("whoami/", whoami, name="whoami"),
]
