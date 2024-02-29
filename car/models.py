from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

class Post(models.Model):
    car_name = models.CharField(max_length = 100)
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    brand = models.CharField(max_length = 50)
    content = models.TextField(default = '', null = True, blank = True)
    date_posted = models.DateTimeField(default = timezone.now)
    car_image = models.ImageField(upload_to = 'car_images', null = True, blank = True)
    likes = models.ManyToManyField(User, related_name = "post_like", blank = True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.car_image:
            img = Image.open(self.car_image.path)

            # Resize the image to a maximum width or height of 800 pixels
            max_size = (1080, 1080)
            img.thumbnail(max_size)

            img.save(self.car_image.path)


    # keep track of likes
    def number_of_likes(self):
        return self.likes.count()
    
    def number_of_comments(self):
        return self.comments.count()

    def __str__(self):
        return self.car_name
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs = {'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name = "comments", on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add = True)    

    def __str__(self):
        return "%s - %s" % (self.post.car_name, self.user.username)
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs = {'pk': self.pk})
    