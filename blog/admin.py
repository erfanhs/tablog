from django.contrib import admin
from .models import Post, Like, Following, Profile

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Following)
