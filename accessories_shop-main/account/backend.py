from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

User = get_user_model()


class UsernameOrEmail(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        login_value = username or kwargs.get(User.USERNAME_FIELD)
        if not login_value or not password:
            return None

        user = (
            User.objects.filter(Q(user_name__iexact=login_value) | Q(email__iexact=login_value))
            .order_by("id")
            .first()
        )
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
