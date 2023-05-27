from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Post, Relationship, Hashtag
from .forms import UserRegisterForm, PostForm, ProfileUpdateForm, UserUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import re

@login_required
def home(request):
	posts = Post.objects.all()
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.user = request.user
			post.save()
			#Obtengo los hashtags del post
			hashtags = extract_hashtags(post.content)
			#Asocia los hashtags al post
			for hashtag in hashtags:
				tag, _ = Hashtag.objects.get_or_create(nombre_hashtag=hashtag)
				post.hashtags.add(tag)

			return redirect('home')
	else:
		form = PostForm()

	context = {'posts':posts, 'form' : form }
	return render(request, 'twitter/newsfeed.html', context)

def extract_hashtags(content):
	hashtags = re.findall(r'#(\w+)', content)
	return hashtags


def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('home')
	else:
		form = UserRegisterForm()

	context = {'form' : form}
	return render(request, 'twitter/register.html', context)


def delete(request, post_id):
	post = Post.objects.get(id=post_id)
	post.delete()
	return redirect('home')

def profile(request, username):
	user = User.objects.get(username=username)
	posts = user.posts.all()
	hashtags = Hashtag.objects.filter(post__user=user).distinct().order_by('nombre')
	context = {'user':user, 'posts':posts, 'hashtags': hashtags}
	return render(request, 'twitter/profile.html', context)

@login_required
def editar(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			return redirect('home')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm()

	context = {'u_form' : u_form, 'p_form' : p_form}
	return render(request, 'twitter/editar.html', context)

@login_required
def follow(request, username):
	current_user = request.user
	to_user = User.objects.get(username=username)
	to_user_id = to_user
	rel = Relationship(from_user=current_user, to_user=to_user_id)
	rel.save()
	return redirect('home')

@login_required
def unfollow(request, username):
	current_user = request.user
	to_user = User.objects.get(username=username)
	to_user_id = to_user.id
	rel = Relationship.objects.get(from_user=current_user.id, to_user=to_user_id)
	rel.delete()
	return redirect('home')

@login_required
def hashtags_en_posts(request, hashtag_id):
	hashtag = Hashtag.objects.get(id=hashtag_id)
	posts = Post.objects.filter(hashtags = hashtag).order_by('-fecha_publicacion')
	context = {'hashtags': hashtags, 'posts': posts}
	return render(request, 'twitter/hashtag_en_posts.html', context)