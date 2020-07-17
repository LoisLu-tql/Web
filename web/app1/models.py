from django.db import models
from tinymce.models import HTMLField

class Person(models.Model):   # 用户
    name = models.CharField(max_length=16, unique=True)
    password = models.CharField(max_length=256)
    mail = models.CharField(max_length=32, null=True)
    add_time = models.DateTimeField(auto_now_add=True)
    icon = models.ImageField(upload_to='icons/%Y/%m', null=True, default='icons/2020/03/default.jpg')
    sex = models.IntegerField(default=0)  # 0-unknown  1-boy  2-girl
    motto = models.CharField(max_length=128, null=True)


class ArticleTag(models.Model):
    name = models.CharField(max_length=32)
    owner = models.ForeignKey(Person)
    add_time = models.DateTimeField(auto_now_add=True)

class Article(models.Model):  # 博客文章
    title = models.CharField(max_length=16)
    content = HTMLField()
    add_time = models.DateTimeField(auto_now_add=True)
    likes_num = models.IntegerField(default=0)
    author = models.ForeignKey(Person, null=True)
    tag = models.ForeignKey(ArticleTag, null=True)

class ArticleComment(models.Model):  # 博客评论
    content = models.CharField(max_length=100)
    article = models.ForeignKey(Article)
    owner = models.ForeignKey(Person)
    add_time = models.DateTimeField(auto_now_add=True, null=True)

class LikeArticle(models.Model):   # 博客-点赞/推荐
    article_id = models.IntegerField()
    fan_id = models.IntegerField()

class MarkArticle(models.Model):   # 博客-收藏
    article_id = models.IntegerField()
    fan_id = models.IntegerField()

class Likes(models.Model):  # 维护关注/粉丝关系
    star_id = models.IntegerField()
    fan_id = models.IntegerField()

class DiscussionTag(models.Model):
    name = models.CharField(max_length=32)
    owner = models.ForeignKey(Person)
    add_time = models.DateTimeField(auto_now_add=True)

class Discussion(models.Model):  # 论坛帖子
    title = models.CharField(max_length=32)
    content = HTMLField()
    owner = models.ForeignKey(Person)
    add_time = models.DateTimeField(auto_now_add=True, null=True)
    tag = models.ForeignKey(DiscussionTag, null=True)

class DiscussionResponse(models.Model):   # 帖子回复
    discussion = models.ForeignKey(Discussion)
    content = HTMLField()
    likes_num = models.IntegerField(default=0)
    owner = models.ForeignKey(Person)
    add_time = models.DateTimeField(auto_now_add=True)

class LikeDiscussionResponse(models.Model):
    comment_id = models.IntegerField()
    fan_id = models.IntegerField()
    add_time = models.DateTimeField(auto_now_add=True)

class LikeDiscussion(models.Model):   # 帖子-点赞/推荐
    discussion_id = models.IntegerField()
    fan_id = models.IntegerField()

class MarkDiscussion(models.Model):   # 帖子-收藏
    discussion_id = models.IntegerField()
    fan_id = models.IntegerField()

class Notice(models.Model):
    receiver_id = models.IntegerField()
    sender = models.ForeignKey(Person, null=True)
    message_type = models.IntegerField() #0-博客点赞 1-博客评论 2-问题回答 3-赞同答案 4-关注
    article = models.ForeignKey(Article, null=True)
    article_comment = models.ForeignKey(ArticleComment, null=True)
    discussion = models.ForeignKey(Discussion, null=True)
    discussion_response = models.ForeignKey(DiscussionResponse, null=True)
    have_read = models.IntegerField(default=0)

class BlogLabel(models.Model):
    article_id = models.IntegerField()
    label_1 = models.CharField(max_length=8, null=True, default="")
    label_2 = models.CharField(max_length=8, null=True, default="")
    label_3 = models.CharField(max_length=8, null=True, default="")

class DiscussionLabel(models.Model):
    discussion_id = models.IntegerField()
    label_1 = models.IntegerField(null=True, default=0) #0-无 1-习题求解 2-寻物启事 3-学习疑惑 4-情感问题 5-留学咨询
    label_2 = models.IntegerField(null=True, default=0)
    label_3 = models.IntegerField(null=True, default=0)