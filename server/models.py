from django.db import models
class admin(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=8)
    email = models.CharField(max_length=50)
    lasttime=models.DateTimeField()
class menu(models.Model):
    name = models.CharField(max_length=30)
class news(models.Model):
    catid = models.IntegerField(max_length=10)
    title = models.CharField(max_length=30)
    title_font_color = models.CharField(max_length=8,null=True)
    thumb = models.CharField(max_length=255)
    num=models.IntegerField(max_length=10)
    lasttime=models.DateTimeField()
class news_content(models.Model):
    newid = models.IntegerField(max_length=10)
    content=models.TextField()
class position(models.Model):
    name = models.CharField(max_length=30)
class position_content(models.Model):
    positionid =models.IntegerField(max_length=10)
    newsid = models.IntegerField(max_length=10)
