from django.db import models

class InvertedIndex(models.Model):
    str = models.CharField(max_length=16)
    article_id = models.IntegerField(default=0)
    time = models.IntegerField(default=1)   # 第一次加入的时候默认有一次

class AlreadyUpdate(models.Model):
    au = models.IntegerField(default=0)
