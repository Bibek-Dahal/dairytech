from django.db import models
from django.contrib.auth import get_user_model
from django.utils.html import mark_safe
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(get_user_model(),related_name='profile',on_delete=models.CASCADE)
    profile_pic = models.ImageField("Profile",upload_to='profile')
    created_at = models.DateTimeField("Created At",auto_now_add=True)
    updated_at = models.DateTimeField("Created At",auto_now=True)

    
    def image(self): #new
        return mark_safe(f'<img src = "{self.profile_pic.url}" width="50" border-radius = "50%"/>')
    