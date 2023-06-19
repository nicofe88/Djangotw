from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save


class Hashtag(models.Model):
	nombre_hashtag = models.CharField(max_length=20, unique=True)

	def __str__(self):
		return f'#{self.nombre_hashtag}'

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	bio = models.CharField(default='Hola, twitter', max_length=100)
	image = models.ImageField(default='default.png')
	following = models.ManyToManyField('self', related_name='followers', blank=True, symmetrical=False)
	
	def __str__(self):
		return f'Perfil de {self.user.username}'
	
	def getFollowing(self):
		user_ids = self.following.values_list('user', flat=True)
		return User.objects.filter(id__in=user_ids)

	def getFollowers(self):
		user_ids = Profile.objects.filter(following=self).values_list('user', flat=True)
		return User.objects.filter(id__in=user_ids)
	
	def create_user_profile(sender,instance,created, **kwargs):
		if created:
			Profile.objects.create(user=instance)

	def save_user_profile(sender,instance, **kwargs):
		instance.profile.save()
	post_save.connect(create_user_profile,sender=User)
	post_save.connect(save_user_profile, sender=User)

class Post(models.Model):
	timestamp = models.DateTimeField(default=timezone.now)
	content = models.TextField()
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
	hashtags = models.ManyToManyField(Hashtag)

	

	class Meta:
		ordering = ['-timestamp']

	def __str__(self):
		return self.content
	


















