from django.contrib.auth.models import User
from django.db import models

from pagetools.subscribe.base_models import BaseSubscriberMixin
class CustomSubscriber(BaseSubscriberMixin):
    user = models.OneToOneField(User)
    email = models.EmailField()
