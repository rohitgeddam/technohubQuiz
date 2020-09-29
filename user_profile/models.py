from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Profile(models.Model):

    COLLEGE_CHOICES = (
        ("Bhilai Institute Of Technology, Durg", "Bhilai Institute Of Technology, Durg"),
        ( "National Institute of Technology, Raipur", "National Institute of Technology, Raipur"),
        ("Sankracharya Institute of Technology, Bhilai", "Sankracharya Institute of Technology, Bhilai"),
        ("other", "other"),
    )

    BRANCH = (
        ("IT","IT"),
        ("CSE", "CSE"),
        ("MECH", "MECH"),
        ("ETC", "ETC"),
        ("EE", "EE"),
        ("CHE", "CHE"),
        ("CIVIL", "CIVIL"),
        ("MCA", "MCA"),
        ("OTHER","OTHER")
    )

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    firstname = models.CharField(max_length=255, default="")
    lastname = models.CharField(max_length=255, default="")
    college_name = models.CharField(max_length=512,choices=COLLEGE_CHOICES, default="other")
    branch = models.CharField(max_length=5, choices=BRANCH, default="OTHER")

    last_modified = models.DateTimeField(auto_now=True)
    
    completed_profile = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance,)
    
@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()