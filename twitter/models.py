from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Hashtag(models.Model):
	nombre_hashtag = models.CharField(max_length=20, unique=True)

	def __str__(self):
		return f'#{self.nombre_hashtag}'
	
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.CharField(default='Hola, twitter', max_length=100)
	image = models.ImageField(default='default.png')

	def __str__(self):
		return f'Perfil de {self.user}'

	def following(self):
		user_ids = Relationship.objects.filter(from_user=self.user)\
									.values_list('to_user_id', flat=True)
		return User.objects.filter(id__in=user_ids)

	def followers(self):
		user_ids = Relationship.objects.filter(to_user=self.user)\
									.values_list('from_user_id', flat=True)
		return User.objects.filter(id__in=user_ids)

class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
	hashtags = models.ManyToManyField(Hashtag)
	content = models.TextField()
	timestamp = models.DateTimeField(default=timezone.now)

	class Meta:
		ordering = ['-timestamp']

	def __str__(self):
		return self.content

class Relationship(models.Model):
	from_user = models.ForeignKey(User, related_name='relationships', on_delete=models.CASCADE)
	to_user = models.ForeignKey(User, related_name='related_to', on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.from_user} to {self.to_user}'
	