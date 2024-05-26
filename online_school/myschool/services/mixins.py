from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from users.models import Profile


class UserIsAuthenticated(UserPassesTestMixin):
    def test_func(self):
        try:
            if self.request.user.is_authenticated:
                raise PermissionDenied
            return True
        except PermissionDenied:
            return False

    def handle_no_permission(self):
        return redirect('main')


class UserAuthAccess(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        try:
            if not user.is_authenticated or profile.email_confirmed:
                raise PermissionDenied
            return True
        except PermissionDenied:
            return False

    def handle_no_permission(self):
        return redirect('main')