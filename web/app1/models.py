from django.db import models, connection
from tinymce.models import HTMLField

class Person(models.Model):   # 用户
    name = models.CharField(max_length=16, unique=True)
    password = models.CharField(max_length=256)
    mail = models.CharField(max_length=32, null=True)
    add_time = models.DateTimeField(auto_now_add=True)
    icon = models.ImageField(upload_to='icons/%Y/%m', null=True, default='icons/2020/03/default.jpg')
    sex = models.IntegerField(default=0)  # 0-unknown  1-boy  2-girl
    motto = models.CharField(max_length=128, null=True)
    fans_num = models.IntegerField(default=0)

class ArticleTag(models.Model):
    name = models.CharField(max_length=32)
    owner = models.ForeignKey(Person)
    add_time = models.DateTimeField(auto_now_add=True)

class Article(models.Model):  # 博客文章 #时间-梯度 访问人数/10 作者粉丝数/10 点赞数 评论数 收藏数
    title = models.CharField(max_length=16)
    content = HTMLField()
    add_time = models.DateTimeField(auto_now_add=True)
    likes_num = models.IntegerField(default=0)
    comments_num = models.IntegerField(null=True, default=0)
    collects_num = models.IntegerField(default=0)
    read_num = models.IntegerField(null=True, default=0)
    author = models.ForeignKey(Person, null=True)
    tag = models.ForeignKey(ArticleTag, null=True)
    tag2 = models.CharField(max_length=64, blank=True)  # 标签 用于搜索
    hot = models.DecimalField(decimal_places=4, max_digits=10, null=True, default=0)

class ReadArticle(models.Model):
    article_id = models.IntegerField(default=0, null=True)
    reader_id = models.IntegerField(default=0, null=True)

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
    comments_num = models.IntegerField(null=True, default=0)
    last_comment_time = models.DateTimeField(auto_now_add=True, null=True)

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

# class BlogLabel(models.Model):
#     article_id = models.IntegerField()
#     label_1 = models.CharField(max_length=8, null=True, default="")
#     label_2 = models.CharField(max_length=8, null=True, default="")
#     label_3 = models.CharField(max_length=8, null=True, default="")

class BlogLabel(models.Model):
    article_id = models.IntegerField()
    have_label = models.IntegerField(null=True, default=0)

# class DiscussionLabel(models.Model):
#     discussion_id = models.IntegerField()
#     label_1 = models.IntegerField(null=True, default=0) # 0-无 1-习题求解 2-寻物启事 3-学习疑惑 4-情感问题 5-留学咨询
#     label_2 = models.IntegerField(null=True, default=0)
#     label_3 = models.IntegerField(null=True, default=0)

class DiscussionLabel(models.Model):
    discussion_id = models.IntegerField()
    have_label = models.IntegerField(null=True, default=0)

class UserLabel(models.Model):   # 维护标签内容与标签所属的用户
    owner = models.ForeignKey(Person)
    name = models.CharField(max_length=32)

class UserBlogLabel(models.Model):    # 维护标签与其对应的文章
    article_id = models.IntegerField()
    label_id = models.IntegerField()

class UserDiscussionLabel(models.Model):   # 维护标签与讨论的
    discussion_id = models.IntegerField()
    label_id = models.IntegerField()

class ChatRoom(models.Model):
    sender_id = models.IntegerField()
    receiver_id = models.IntegerField()
    sender_unread_num = models.IntegerField(default=0, null=True)
    receiver_unread_num = models.IntegerField(default=0, null=True)

class ChatContent(models.Model):
    message = models.CharField(max_length=256)
    message_time = models.DateTimeField(auto_now_add=True)
    message_room = models.ForeignKey(ChatRoom)
    message_type = models.IntegerField() #send=1  receive=0
    have_read = models.IntegerField(default=0, null=True)
