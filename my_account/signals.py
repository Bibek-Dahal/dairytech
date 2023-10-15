from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from .models import User
from user.models import Profile

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
    

@receiver(pre_save, sender=User)
def user_verification_handler(sender,instance,**kwargs):
    """
        This signal handels user if user change their email of phone number
    """
    print(kwargs)
    previous_user = User.objects.filter(id=instance.id)
    print("prev usre",previous_user)
    
    
    
    if previous_user:
        if instance.phone_number != previous_user[0].phone_number:
            print("phone num modified")
            instance.is_active = False

        if instance.email != previous_user[0].email:
            print("user email changed")
            instance.is_email_verified = False


    print("pre save called")