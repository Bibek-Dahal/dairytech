from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from .models import User
from user.models import Profile

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    print("create user profile running")
    if created:
        print("inside if")
        Profile.objects.create(user=instance)
    
    
@receiver(pre_save, sender=Profile)
def delete_old_profile_image(sender, instance, **kwargs):
    # Initialize old_profile as None
    old_profile = None

    try:
        # Get the current user's profile
        old_profile = Profile.objects.get(pk=instance.pk)
    except Profile.DoesNotExist:
        return

    if old_profile.profile_pic != instance.profile_pic:
        # The profile image has changed; delete the old image
        old_profile.profile_pic.delete(save=False)


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