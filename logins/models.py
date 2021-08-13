from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from logins.permissions import CannotManage


class CustomUser(AbstractUser):

    def __str__(self):
        return "{}".format(self.email)

    def user_can_manage_me(self, user):
        return user == self or user.is_staff

    @classmethod
    def get_manageable_object_or_404(cls, user, *args, **kwds):
        item = get_object_or_404(cls, *args, **kwds)
        if not item.user_can_manage_me(user):
            raise CannotManage
        return item
