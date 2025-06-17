from django.db import models
from django.core.validators import MaxValueValidator,MaxLengthValidator,MinLengthValidator
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
# Create your models here.
class Testimonials(models.Model):
    name = models.CharField(max_length = 150)
    comments = models.TextField()
    profile=models.ImageField(upload_to='media/')


    def __str__(self):
        return self.name
    
class Course(models.Model):
    cimage=models.ImageField(upload_to='media/',null=True,blank=True)
    name=models.CharField(max_length=100)
    duration=models.CharField(max_length=100)
    fee=models.IntegerField(
        validators=[MaxValueValidator(10000)]
    )

    def __str__(self):
        return self.name

class Join(models.Model):
    simage=models.ImageField(upload_to='media/')



class Team(models.Model):
    profile=models.ImageField(upload_to='media/',blank=True,null=True)
    name=models.CharField(max_length=20)
    position=models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name=models.CharField(max_length=30)
    contact = models.CharField(max_length=10,validators=[MinLengthValidator(10),MaxLengthValidator(10)])
    email=models.EmailField(unique=True,null=True,blank=True)
    message=models.TextField()


    def __str__(self):
        return self.name


class AboutCourse(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    about=RichTextField()
    learn=RichTextField()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile=models.ImageField(upload_to='media/')

   
class Transaction(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    transaction_uuid = models.CharField(max_length=100,unique=True)
    transaction_amount=models.DecimalField(max_digits=10,decimal_places=2)
    transaction_date=models.DateTimeField(auto_now_add=True)
    transaction_status=models.CharField(max_length=50,choices=[
        ('pending','Pending'),
        ('completed','Completed'),
        ('failed','Failed'),
    ],default='pending')

