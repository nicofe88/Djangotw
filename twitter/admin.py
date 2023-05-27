from django.contrib import admin
from .models import Profile, Post, Relationship, Hashtag

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Relationship)
admin.site.register(Hashtag)