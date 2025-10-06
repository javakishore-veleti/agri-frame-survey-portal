from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class AgrTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # add enterprise claims
        token["email"] = user.email
        token["username"] = user.username
        token["roles"] = list(
            user.userrole_set.values_list("role__id", flat=True)
        ) if hasattr(user, "userrole_set") else []
        token["tenant_code"] = getattr(
            user, "tenant_code", None
        ) or "FPAC"

        return token
