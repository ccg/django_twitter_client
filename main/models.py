from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    oauth_token = models.TextField(blank=True, null=False)

    def can_tweet(self):
        # Kind of a hack. If there's something in the oauth_token
        # field, assume the user authorized us to tweet.
        if self.oauth_token != None and self.oauth_token != '':
            return True
        return False

    def __unicode__(self):
        return "username: '%s'" % self.user.username
    def __str__(self):
        return self.__unicode__()

def create_profile(sender, instance=None, **kwargs):
    if instance is None:
        return
    profile, created = UserProfile.objects.get_or_create(user=instance)

models.signals.post_save.connect(create_profile, sender=User)
