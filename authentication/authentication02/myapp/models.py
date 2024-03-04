from django.db import models

from django.contrib.auth.models import AbstractUser



class Custom_user(AbstractUser):
    USER =[
        ('admin','Admin'),
        ('user','User'),
        
    ]
    first_name=models.CharField(max_length=50, null=True, blank=True)
    last_name=models.CharField(max_length=50, null=True, blank=True)
    username=models.CharField(null=True, blank=True, max_length=50, unique=True)
    display_name=models.CharField(max_length=50, null=True, blank=True)
    email=models.EmailField(unique=True, max_length=100)
    user_type=models.CharField(choices=USER, max_length=50)
    password=models.CharField(max_length=50)
    confirm_password=models.CharField(max_length=50)
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']
    
    GENDER=[
        ('Male','male'),
        ('Female','female'),
    ]
    
    profile_pic=models.ImageField(upload_to='media/profile pic', null=True, blank=True)
    age=models.FloatField( null=True, blank=True)
    gender=models.CharField(max_length=100, choices=GENDER,null=True, blank=True)
    phone=models.CharField(max_length=10, null=True, blank=True)
    Present_address=models.CharField(max_length=100, null=True, blank=True)
    permanent_address=models.CharField(max_length=100, null=True, blank=True)
    
    otp_token = models.CharField(max_length = 6, blank = True, null = True)

    
    
    def __str__(self):
        return self.username
    




    
    
    
    
    