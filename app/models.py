from django.db import models

from django.db.models.signals import post_save

from django.contrib.auth.models import User

from django.dispatch import receiver

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField 

from imagekit.models import ImageSpecField
from imagekit.models import ProcessedImageField

from imagekit.processors import ResizeToFill

from datetime import datetime

# All Models or Tables are [7] and "update_user_profile" is not a models or table ==> this is just a connector to "User" Django Table (hastesh!)!
# profile is connect to update_user_profile and this connect to User TABLE!

class profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    address = models.CharField(max_length=1000)
    code_posti = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
      
@receiver(post_save, sender = User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        profile.objects.create(user = instance)
    instance.profile.save()

class Category(models.Model):

    name = models.CharField(max_length = 600)

    def __str__(self):
        return self.name
    class Meta: 
        verbose_name_plural = "Categorys"

class Grouping(models.Model):
    title = models.CharField(max_length=500, verbose_name="دسته بندی اصلی این پست را وارد نمائید.") 
    category = models.ManyToManyField(Category, verbose_name="دسته بندی های این دسته را وارد کنید.")

    def __str__(self):
        return self.title
    class Meta: 
        verbose_name_plural = "Groupings"
 
class POSTS(models.Model):
    product_status = (('unavailable', 'ناموجود'), ('available', 'موجود'),)
    post_status = (("published", "پست شده"), ("draft", "پیش نویس"))
    title = models.CharField(max_length=500)
    content = RichTextField()
    photo_post = models.ImageField(upload_to = f'posts/%Y/%D', help_text='Upload your photo')
    
    photo_post1 = models.ImageField(upload_to = f'posts/%Y/%D', help_text='Upload your photo', blank=True,null=True)
    photo_post2 = models.ImageField(upload_to = f'posts/%Y/%D', help_text='Upload your photo', blank=True,null=True)
    photo_post3 = models.ImageField(upload_to = f'posts/%Y/%D', help_text='Upload your photo', blank=True,null=True)
    photo_post4 = models.ImageField(upload_to = f'posts/%Y/%D', help_text='Upload your photo', blank=True,null=True)
      
    price = models.IntegerField(blank=True, null=True)
    Discount = models.IntegerField(blank=True, null=True)
    
    count = models.IntegerField(blank=True, null=True)
    views = models.IntegerField(blank=True, null=True, default=0)
    
    category =  models.ManyToManyField(Category) 

    status = models.CharField(max_length=500, choices=product_status)
    published = models.CharField(max_length=500, choices=post_status)
    create_date = models.DateTimeField(auto_now_add = True)
    update_date = models.DateTimeField(auto_now = True, help_text = "Post insertion date")#default = timezone.now

    tags = models.CharField(max_length=1000)

     

    def __str__(self):
        return self.title  

    class Meta:
        verbose_name_plural = 'Posts'

class Comments(models.Model):
    name = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    comment = models.CharField(max_length=500)
    post = models.ForeignKey('POSTS', on_delete = models.CASCADE, related_name='comments')
    create_date = models.DateTimeField(auto_now_add = True)
    status = models.BooleanField(default=False, verbose_name="submit")

    answer = models.TextField(blank = True, null = True, help_text = "Your Answer To This Comment!")
    update_date = models.DateTimeField(auto_now = True) 
 

    class Meta:
        verbose_name_plural = "Comments"

class buys(models.Model):
    user = models.IntegerField()
    price = models.IntegerField()
    POST = models.IntegerField()
    count = models.IntegerField()
    class Meta:
        verbose_name_plural = "Buys"

class SabadKharid(models.Model):
    user = models.IntegerField()
    product = models.IntegerField()
    count = models.IntegerField()

    class Meta:
        verbose_name_plural = "سبد خرید"
        
    def __str__(self):
        return f"{self.product}, {self.user}"

 