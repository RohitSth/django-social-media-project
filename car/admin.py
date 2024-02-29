from django.contrib import admin
from .models import Post, Comment

# registering models so that they show up in admin page
admin.site.register(Post)
admin.site.register(Comment)