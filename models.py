from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Video(models.Model):
    video_id = models.AutoField(primary_key=True)
    video_name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    tags = models.CharField(max_length=200)
    img = models.FileField(upload_to="media/images", default="static/img/logo.svg")
    file = models.FileField(upload_to="media/videos")

    def __str__(self):
        return self.video_name


class MovieSeries(models.Model):
    movie_id = models.AutoField(primary_key=True)
    movie_name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    tags = models.CharField(max_length=200)
    img = models.FileField(upload_to="media/images", default="static/img/logo.svg")
    file = models.FileField(upload_to="media/videos")

    def __str__(self):
        return self.movie_name


class Ad(models.Model):
    ad_id = models.AutoField(primary_key=True)
    ad_name = models.CharField(max_length=100)
    tags = models.CharField(max_length=200)
    link = models.CharField(max_length=255)
    file = models.FileField(upload_to="media/videos", default="www.youtube.com")

    def __str__(self):
        return self.ad_name

class Watch_later(models.Model):
    watch_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_id = models.CharField(max_length=1000000000)


class History(models.Model):
    hist_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_id = models.CharField(max_length=1000000000)


class Channel(models.Model):
    channel_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    video = models.CharField(max_length=10000000000)


class Pay(models.Model):
    pay_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    movie = models.CharField(max_length=10000000000)
    img = models.FileField(upload_to="media/payment", default="static/img/logo.svg")


class BoughtVideoB(models.Model):
    bought_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.CharField(max_length=1000000000)

