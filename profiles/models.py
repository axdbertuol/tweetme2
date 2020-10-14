from django.db import models
from django.db.models.signals import post_save
from django.conf import settings

# Create your models here.
User = settings.AUTH_USER_MODEL
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	location = models.CharField(max_length=220, null=True, blank=True)
	bio = models.TextField(blank=True, null=True)

	def __str__(self):
		return self.user.username + " Profile"


def user_did_save(sender, instance, created, *args, **kwargs):

	if created:
		Profile.objects.get_or_create(user=instance)

post_save.connect(user_did_save, sender=User)

# Make signal function to verify if user has a Profile when he logs in