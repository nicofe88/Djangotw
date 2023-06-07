from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Profile
import re

class UserRegisterForm(UserCreationForm):

	class Meta:
		model = User
		fields = ['first_name', 'username', 'email', 'password1', 'password2']

class PostForm(forms.ModelForm):
	content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control w-100',
								'id':'contentsBox', 'rows':'3',
								'placeholder':'¿Qué está pasando?'}))

	class Meta:
		model = Post
		fields = ['content']

	def extrae_hashtag(self):
		content = self.cleaned_data.get('content', '')
		#extraigo del txtarea los comandos hashtags creados a partir del comando +#ejemplo
		hashtags = re.findall(r'\#(\w+)', content)
		return hashtags

class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'username']

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image', 'bio']















