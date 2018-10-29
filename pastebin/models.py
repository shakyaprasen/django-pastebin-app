from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class POST(models.Model):
    post_info = models.TextField(max_length=2000)
    file_path = models.CharField(max_length=500)
    entry_date = models.DateTimeField('post entry date')
    last_updated = models.BooleanField(default=False)
    post_update = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    title = models.CharField(default = 'Untitled', max_length=30)
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)

    def __str__(self): 
        return self.post_info


class URL(models.Model):
    post = models.ForeignKey(POST, on_delete=models.CASCADE)
    length = models.IntegerField(default=0)
    short_url = models.CharField(max_length=15)
    last_updated = models.BooleanField(default=False)
    url_update = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    def __str__(self): 
        return self.short_url