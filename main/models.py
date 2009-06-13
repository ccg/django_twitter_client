from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    oauth_token = models.TextField(blank=True, null=False)

    def __unicode__(self):
        return "<Profile for '%s'>" % user.name
    def __str__(self):
        return self.__unicode__()
