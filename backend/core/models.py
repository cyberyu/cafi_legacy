from django.contrib.auth.models import User
from django.db import models
from core.helpers import format_phone_number

class UserProfile(models.Model):
    """
        Represents a user's profile
    """
    user = models.OneToOneField(User)
    title = models.CharField(max_length=128, null=True, blank=True)
    office_phone = models.CharField(max_length=32, null=True, blank=True)

    @classmethod
    def active_user_count(cls):
        return User.objects.filter(is_active=True).count()

    @property
    def full_name(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    def format_phone_numbers(self):
        self.office_phone_formatted = format_phone_number(self.office_phone)

    def save(self, *args, **kwargs):
        self.format_phone_numbers()
        super(UserProfile, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.user
