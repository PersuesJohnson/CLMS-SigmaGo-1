from django.db import models
from image_cropping import ImageRatioField
from django.db.models.fields.files import ImageFieldFile
from django.contrib import admin
from django import forms
import skimage.io
from skimage.transform import resize
import os
# Create your models here.

def make_thumb(path,thumb_path, size = (160,120)):
    image = skimage.io.imread(path)
    height,width = image.shape[0],image.shape[1]

    thumb=image

    if (height/width)>(size[0]/size[1]):
        new_height=width*size[0]/size[1]
        height1=(height-new_height)/2
        thumb=image[height1:height+new_height,0:width]

    if (height/width)<(size[0]/size[1]):
        new_width=height*size[1]/size[0]
        width1=(width-new_width)/2
        thumb=image[0:height,width1:width1+new_width]
    
    thumb = resize(thumb, size)
    print(thumb.shape)
    skimage.io.imsave(thumb_path,thumb)
    return thumb


class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Competition(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100,blank=True,null=True)

    # basic info
    hold_time = models.DateTimeField()
    holder = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    # text
    intro = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    method = models.TextField(blank=True, null=True)
    award = models.TextField(blank=True, null=True)
    
    # image
    image = models.ImageField(
            upload_to='./Competition/images/', null=True, blank=True)
    thumb = models.ImageField(upload_to = './Competition/thumbs', blank = True)
    cropping = ImageRatioField('image', '640x480')
    
    tag = models.ManyToManyField(Tag)
    
    # what is this?
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    
    result = models.FileField(
        upload_to='./Competition/result/', null=True, blank=True)

    date_time = models.DateTimeField(auto_now_add=True)

    def save(self):
        super(Competition,self).save()
        #base, ext = os.path.splitext(os.path.basename(self.image.path))
        thumb_path = os.path.join('./media/Competition/thumbs/', os.path.basename(self.image.path))
        thumb = make_thumb(self.image.path,thumb_path)
       
        #thumb_path = os.path.join(MEDIA_ROOT, relate_thumb_path)
        thumb_path = os.path.join('./Competition/thumbs/', os.path.basename(self.image.path))
        self.thumb = ImageFieldFile(self, self.thumb, thumb_path)
        super(Competition, self).save()
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_time']


class Lecture(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100,blank=True,null=True)

    # basic info
    hold_time = models.DateTimeField()
    holder = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    # text 
    intro = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    news = models.TextField(blank=True, null=True)
    
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    
    #image
    image = models.ImageField(
        upload_to='./Lecture/images/', null=True, blank=True)
    thumb = models.ImageField(upload_to = './Lecture/thumbs', blank = True)
    cropping = ImageRatioField('image', '640x480')
    
    tag = models.ManyToManyField(Tag)
    
    date_time = models.DateTimeField(auto_now_add=True)

    def save(self):
        super(Lecture,self).save()
        #base, ext = os.path.splitext(os.path.basename(self.image.path))
        thumb_path = os.path.join('./media/Lecture/thumbs/', os.path.basename(self.image.path))
        thumb = make_thumb(self.image.path,thumb_path)
       
        #thumb_path = os.path.join(MEDIA_ROOT, relate_thumb_path)
        thumb_path = os.path.join('./Lecture/thumbs/', os.path.basename(self.image.path))
        self.thumb = ImageFieldFile(self, self.thumb, thumb_path)
        super(Lecture, self).save()
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_time']

class User(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    def __unicode__(self):
        return self.username

class RegUserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password1 = forms.CharField(label='密码',widget=forms.PasswordInput())
    password2 = forms.CharField(label='请再输入密码',widget=forms.PasswordInput())

class LogUserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())