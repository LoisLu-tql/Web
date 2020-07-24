import re
import time
import uuid
from io import BytesIO
import random

from django.db import connection
from PIL import Image, ImageFont
from PIL.ImageDraw import ImageDraw
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db import connection
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.utils import timezone

from app1.models import Article, Person, Likes, Discussion, LikeArticle, MarkArticle, ArticleComment, LikeDiscussion, \
    MarkDiscussion, DiscussionResponse, LikeDiscussionResponse, Notice, BlogLabel, DiscussionLabel, UserLabel, \
    UserBlogLabel, ReadArticle
from app1.tools import get_color, generate_code
from web1 import settings


def helloworld(request):
    return HttpResponse('Hello world !')


# def addarticle(request):
#     if request.method == 'GET':
#         context = {
#             'title': 'Add Article',
#         }
#         return render(request, 'Blog/addarticle.html', context=context)
#     elif request.method == 'post':
#         return HttpResponse("add success")

def index(request):
    try:
        username = request.session['username']  # 没有session的话这一行代码会报错
        user = Person.objects.get(name=username)
        context = {
            'title': 'index',
            'user': user,
            'have_user': True,
        }
    except Exception as e:
        context = {
            'title': 'Index',
            'have_user': False
        }
    return render(request, 'index.html', context)


def home(request):
    try:
        username = request.session['username']
        user = Person.objects.filter(name=username).first()
    except Exception as e:
        return HttpResponse("Please Login first")

    page_now = int(request.GET.get('page', 1))
    per_page = 10

    articles = user.article_set.all().order_by('-id')  # 新发表的(id值大的)排在前面
    paginator = Paginator(articles, per_page)
    page_objects = paginator.page(page_now)

    context = {
        'title': username + '\'s home',
        'user': user,
        'icon_url': '/static/uploadfiles/' + user.icon.url,
        'page_objects': page_objects,
        'page_range': paginator.page_range,  # paginator.page_range用于获取一共有多少页
        'page_now': page_now,
    }
    return render(request, 'UserManager/home.html', context=context)


def register(request):
    if request.method == 'GET':
        return render(request, 'UserManager/register.html', context={'title': 'Register'})
    elif request.method == 'POST':
        username = request.POST.get('username')
        if Person.objects.filter(name=username).exists():
            return HttpResponse("用户名已存在")
        if request.POST.get('verify_code') != request.session['verify_code']:
            return HttpResponse("验证码错误")
        password = request.POST.get('password')
        user = Person()
        user.name = username
        user.password = password
        user.save()
        response = render(request, 'Page Jump/register_to_login.html')
        return response


def get_verify_code(request):
    mode = "RGB"
    size = (100, 40)

    red = get_color()
    green = get_color()
    blue = get_color()
    color_bg = (red, green, blue)

    image = Image.new(mode=mode, size=size, color=color_bg)
    imagedraw = ImageDraw(image, mode=mode)
    imagefont = ImageFont.truetype(settings.FONT_PATH, 40)

    verify_code = generate_code()
    request.session['verify_code'] = verify_code  # 存到session中用于用户登录

    for i in range(4):
        fill = (get_color(), get_color(), get_color())
        imagedraw.text(xy=(25 * i, 0), text=verify_code[i], font=imagefont, fill=fill)

    for i in range(700):
        fill = (get_color(), get_color(), get_color())
        xy = (random.randrange(100), random.randrange(40))
        imagedraw.point(xy=xy, fill=fill)

    fp = BytesIO()
    image.save(fp, "png")

    return HttpResponse(fp.getvalue(), content_type="image/png")


def check_username(request):
    data = {
        'status': 200,
        'msg': 'username is allowed',
    }
    username = request.GET.get('username')
    user = Person.objects.filter(name=username)
    if user.exists():
        data['status'] = 901
        data['msg'] = 'username already exists'
    return JsonResponse(data=data)


def login(request):
    if request.method == 'GET':
        return render(request, 'UserManager/login.html', context={'title': 'login'})
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        users = Person.objects.filter(Q(name=username) & Q(password=password))
        if users.exists():
            user = users.first()
            request.session['username'] = user.name
            response = redirect(reverse('app1:home'))
        else:
            response = redirect(reverse('app1:login'))
        return response


# def forget_password(request):
#     if request.method == 'GET':
#         return render(request, 'User Manage/forget_password.html')
#     elif request.method == 'POST':
#         u_token = uuid.uuid4().hex
#         email = request.POST.get('email')
#         user = Person.objects.filter(email=email)
#         if not user.exists():
#             return HttpResponse("请检查您输入的邮箱是否有误！")
#         user = user.first()
#         cache.set(u_token, user.id, timeout = 60*60*24 )
#         send_email_change_password(user.name, email, u_token)
#         return HttpResponse("已向您发送密码重置邮件，请注意查收")


def logout(request):
    request.session.flush()
    response = redirect(reverse('app1:index'))
    return response


def add_article(request):
    try:
        user = Person.objects.get(name=request.session['username'])
        if request.method == "GET":

            userlabels = UserLabel.objects.filter(owner=user)

            context = {
                'title': 'Add article',
                'userlabels': userlabels,
            }
            return render(request, 'Blog/add_article.html', context)

        elif request.method == "POST":

            article = Article()
            article.title = request.POST.get('title')
            article.content = request.POST.get('content')
            article.author = user
            article.save()

            blog_label = BlogLabel()
            blog_label.article_id = article.id
            labels = request.POST.getlist("item")
            for label in labels:
                blog_label.have_label += pow(2, int(label) - 1)
            s = []
            binstring = ''
            while blog_label.have_label > 0:
                rem = blog_label.have_label % 2
                s.append(rem)
                blog_label.have_label = blog_label.have_label // 2
            while len(s) > 0:
                binstring = binstring + str(s.pop())
            blog_label.have_label = int(binstring)
            blog_label.save()

            tot = request.POST.get("tot_label")
            tot = int(tot)
            for i in range(1, tot+1):
                lid = 'ulabel'+str(i)
                ulabel_name = request.POST.get(lid)
                ulabel_name = ulabel_name.strip()
                ulabel = UserLabel.objects.filter(name=ulabel_name).filter(owner=user).first()
                ubl = UserBlogLabel()
                ubl.article_id = article.id
                ubl.label_id = ulabel.id
                ubl.save()

            response = redirect(reverse('app1:home'))
            return response
    except Exception as e:
        response = render(request, 'Page Jump/notlogin_to_login.html')
        return response


# def add_article(request):
#      user = Person.objects.get(name=request.session['username'])
#      if request.method == "GET":
#          context = {
#             'title': 'Add article',
#          }
#          return render(request, 'Blog/add_article.html', context)

def show_article(request, article_id):
    username = request.session.get('username')
    is_login = False
    is_author = False
    article = Article.objects.get(id=article_id)
    comments = ArticleComment.objects.filter(article=article)
    ulbs = UserBlogLabel.objects.filter(article_id=article.id)
    ulabels = []
    for ubl in ulbs:
        ulabel = UserLabel.objects.get(id=ubl.label_id)
        ulabels.append(ulabel)
    data = {
        'title': article.title,
        'article': article,
        'comments': comments,
        'ulabels': ulabels,
    }
    try:
        blog_label = BlogLabel.objects.get(article_id=article.id)
        labels = []
        if blog_label.have_label % 10 == 1:
            labels.append('高等数学')
        if blog_label.have_label // 10 % 10 == 1:
            labels.append('线性代数')
        if blog_label.have_label // 100 % 10 == 1:
            labels.append('数据结构与算法')
        if blog_label.have_label // 1000 % 10 == 1:
            labels.append('大学物理')
        if blog_label.have_label // 10000 % 10 == 1:
            labels.append('概率论')
        if blog_label.have_label // 100000 % 10 == 1:
            labels.append('计算机科学与技术')
        if blog_label.have_label // 1000000 % 10 == 1:
            labels.append('机电工程与自动化')
        if blog_label.have_label // 10000000 % 10 == 1:
            labels.append('电子与信息工程')
        if blog_label.have_label // 100000000 % 10 == 1:
            labels.append('经济管理')
        if blog_label.have_label // 1000000000 % 10 == 1:
            labels.append('材料与环境')
        data['labels'] = labels
        is_label = True
    except Exception as e:
        is_label = False
    if username:
        is_login = True
        user = Person.objects.get(name=username)
        data['user'] = user
        if username == article.author.name:
            is_author = True
    data['is_login'] = is_login
    data['is_author'] = is_author
    data['is_label'] = is_label
    try:
        read = ReadArticle.objects.get(Q(article_id=article_id) & Q(reader_id=user.id))
    except Exception as e:
        read = ReadArticle()
        read.article_id = article_id
        read.reader_id = user.id
        read.save()
        article.read_num += 1
        article.save()
    return render(request, 'Blog/show_article.html', context=data)


def add_like_relationship(request):  # 关注
    star_id = request.GET.get('star_id')
    fan_id = request.GET.get('fan_id')
    relations = Likes.objects.filter(fan_id=fan_id).filter(star_id=star_id)
    if relations.exists():
        data = {
            'status': 400,
            'msg': 'already exists',
        }
    else:
        Relation = Likes()
        Relation.star_id = star_id
        Relation.fan_id = fan_id
        Relation.save()
        star = Person.objects.get(id=star_id)
        star.fans_num += 1
        star.save()
        message = Notice()
        message.message_type = 4
        message.sender_id = fan_id
        message.receiver_id = star_id
        message.save()
        data = {
            'status': 200,
            'msg': 'add success',
        }
    return JsonResponse(data=data)


def recommend_article(request):  # 给博客点赞
    article_id = request.GET.get('article_id')
    fan_id = request.GET.get('fan_id')
    relations = LikeArticle.objects.filter(fan_id=fan_id).filter(article_id=article_id)
    if relations.exists():
        data = {
            'status': 400,
            'msg': 'already exists',
        }
    else:
        Relation = LikeArticle()
        Relation.article_id = article_id
        Relation.fan_id = fan_id
        Relation.save()
        article = Article.objects.get(id=article_id)
        article.likes_num += 1
        article.save()

        message = Notice()
        message.message_type = 0
        message.sender = Person.objects.get(id=fan_id)
        message.receiver_id = article.author.id
        message.article = article
        message.save()

        data = {
            'status': 200,
            'msg': 'add success',
        }
    return JsonResponse(data=data)


def mark_article(request):  # 给博客点赞
    article_id = request.GET.get('article_id')
    fan_id = request.GET.get('fan_id')
    relations = MarkArticle.objects.filter(fan_id=fan_id).filter(article_id=article_id)
    if relations.exists():
        data = {
            'status': 400,
            'msg': 'already exists',
        }
    else:
        Relation = MarkArticle()
        Relation.article_id = article_id
        Relation.fan_id = fan_id
        Relation.save()
        data = {
            'status': 200,
            'msg': 'add success',
        }
    return JsonResponse(data=data)


def add_icon(request):
    if request.method == 'GET':
        return render(request, 'UserManager/add_icon.html')
    else:
        try:
            username = request.session['username']
            user = Person.objects.get(name=username)
            user.icon = request.FILES.get('icon')
            user.save()
            response = redirect(reverse('app1:home'))
            return response
        except Exception as e:
            return HttpResponse("您还没有登录！")


def my_blog(request):
    try:
        username = request.session['username']
    except Exception as e:
        return redirect(reverse('app1:login'))

    user = Person.objects.get(name=username)
    articles = Article.objects.filter(author=user).order_by('-id')

    for article in articles:
        article.content = article.content[:90]

    ulabels = UserLabel.objects.filter(owner=user)

    ulabel_now = int(request.GET.get('ulabel_now',0))
    if ulabel_now :
        ulabel = UserLabel.objects.get(id=ulabel_now)
        articles = []
        ubls = UserBlogLabel.objects.filter(label_id=ulabel.id)
        for ubl in ubls:
            article = Article.objects.get(id=ubl.article_id)
            articles.append(article)

    context = {
        'title': 'My Blogs',
        'articles': articles,
        'ulabels': ulabels,
    }

    return render(request, 'Blog/my_blog.html', context=context)


def change_password_check(request):
    if request.method == 'GET':
        return render(request, 'UserManager/change_password_check.html', {'title': 'Change Password'})
    elif request.method == 'POST':
        username = request.session['username']
        password = request.POST.get('password')
        user = Person.objects.get(name=username)
        if user.password == password:
            u_token = uuid.uuid4().hex
            cache.set(u_token, user.id, timeout=60 * 60 * 24)
            new_url = 'http://127.0.0.1:8000/changepassword/?u_token=' + u_token
            return redirect(new_url)
        else:
            return HttpResponse("密码错误！")


def change_password(request):
    u_token = request.GET.get('u_token')
    if not u_token:
        u_token = request.POST.get('u_token')
    user_id = cache.get(u_token)
    if user_id:
        user = Person.objects.get(pk=user_id)
        if request.method == 'GET':
            data = {
                'u_token': u_token,
                'title': 'Change Password',
            }
            return render(request, 'UserManager/change_password.html', context=data)
        elif request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if password1 != password2:
                return HttpResponse("LOL ! Not the same password !")

            user.password = password1
            user.save()
            return HttpResponse("密码修改成功")

    return HttpResponse("404")


def delete_article(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
        user = article.author
        if user.name != request.session['username']:
            return render(request, 'Wrong Page/noRight.html')
        article.delete()
        return redirect(reverse('app1:home'))
    except Exception as e:
        return HttpResponse("此文章不存在哟~")


def personal_information(request):
    username = request.session.get('username')
    if not username:
        return render(request, 'Page Jump/notlogin_to_login.html')

    user = Person.objects.get(name=username)
    if request.method == 'GET':
        return render(request, 'UserManager/personal_information.html', {'user': user, 'title': '个人信息'})
    elif request.method == 'POST':
        user.email = request.POST.get('email')
        user.sex = request.POST.get('sex')
        user.motto = request.POST.get('motto')
        user.save()
        return render(request, 'Page Jump/change_success.html')


def blogs(request, order_type):
    page_now = int(request.GET.get('page', 1))
    per_page = 10
    if order_type == '0':
        blogs = Article.objects.all().order_by('-hot') #热度大在前
    else:
        blogs = Article.objects.all().order_by('-id')  # 新发表的(id值大的)排在前面

    paginator = Paginator(blogs, per_page)
    page_objects = paginator.page(page_now)

    # label_now = int(request.GET.get('label_now', 0))
    # if label_now:
    #     blogs = blogs.filter()

    for blog in blogs:
        blog.content = blog.content[:50]

    random_range = len(blogs)
    aim_id = random.randint(1, random_range)

    data = {
        'blogs': blogs,
        'page_objects': page_objects,
        'page_range': paginator.page_range,  # paginator.page_range用于获取一共有多少页
        'page_now': page_now,
        'title': 'Blog',
        'aim_id': aim_id,
    }
    return render(request, 'Blog/blogs.html', context=data)


def add_discussion(request):
    username = request.session.get('username')
    if not username:
        return render(request, 'Page Jump/notlogin_to_login.html')
    user = Person.objects.get(name=username)
    if request.method == 'GET':
        data = {
            'title': 'Add discussion',
        }
        return render(request, 'Discussion/add_discussion.html', context=data)
    elif request.method == 'POST':
        discussion = Discussion()
        discussion.title = request.POST.get('title')
        discussion.content = request.POST.get('content')
        discussion.owner = user
        discussion.save()

        discussion_label = DiscussionLabel()
        discussion_label.discussion_id = discussion.id
        labels = request.POST.getlist("item")

        for label in labels:
            discussion_label.have_label += pow(2, int(label)-1)
        s = []
        binstring = ''
        while discussion_label.have_label > 0:
            rem = discussion_label.have_label % 2
            s.append(rem)
            discussion_label.have_label = discussion_label.have_label // 2
        while len(s) > 0:
            binstring = binstring + str(s.pop())
        discussion_label.have_label = int(binstring)
        discussion_label.save()

        return redirect(reverse('app1:home'))


def my_discussion(request):
    username = request.session.get('username')
    if not username:
        return render(request, 'Page Jump/notlogin_to_login.html')
    user = Person.objects.get(name=username)
    discussions = Discussion.objects.filter(owner=user).order_by('-id')
    data = {
        'discussions': discussions,
        'title': 'My discussions',
    }
    return render(request, 'Discussion/my_discussion.html', context=data)


def show_discussion(request, discussion_id, order_type):
    try:
        discussion = Discussion.objects.get(pk=discussion_id)
    except Exception as e:
        return HttpResponse('404')

    username = request.session.get('username')
    is_login = True
    is_author = False
    if not username:
        is_login = False
    if is_login:
        if username == discussion.owner.name:
            is_author = False
    #0-热度 1-最新
    if order_type == '1':
        comments = DiscussionResponse.objects.filter(discussion=discussion).order_by('-id')
    else:
        comments = DiscussionResponse.objects.filter(discussion=discussion).order_by('-likes_num')

    data = {
        'title': discussion.title,
        'discussion': discussion,
        'is_login': is_login,
        'is_author': is_author,
        'user': Person.objects.get(name=username),
        'comments': comments,
    }
    try:
        discussion_label = DiscussionLabel.objects.get(discussion_id=discussion.id)
        labels = []
        if discussion_label.have_label % 10 == 1:
            labels.append('高等数学')
        if discussion_label.have_label // 10 % 10 == 1:
            labels.append('线性代数')
        if discussion_label.have_label // 100 % 10 == 1:
            labels.append('数据结构与算法')
        if discussion_label.have_label // 1000 % 10 == 1:
            labels.append('大学物理')
        if discussion_label.have_label // 10000 % 10 == 1:
            labels.append('概率论')
        if discussion_label.have_label // 100000 % 10 == 1:
            labels.append('机械制图')
        if discussion_label.have_label // 1000000 % 10 == 1:
            labels.append('寻物启事与失物招领')
        if discussion_label.have_label // 10000000 % 10 == 1:
            labels.append('找寻组织与兴趣交流')
        if discussion_label.have_label // 100000000 % 10 == 1:
            labels.append('心理咨询')
        if discussion_label.have_label // 1000000000 % 10 == 1:
            labels.append('跳蚤市场')
        data['labels'] = labels
        is_label = True
    except Exception as e:
        is_label = False
    data['is_label'] = is_label
    return render(request, 'Discussion/show_discussion.html', context=data)


def discussions(request):
    page_now = int(request.GET.get('page', 1))
    per_page = 10

    discussions = Discussion.objects.all().order_by('-last_comment_time')  # 新发表的或最新评论的排在前面

    paginator = Paginator(discussions, per_page)
    page_objects = paginator.page(page_now)

    data = {
        'title': 'Discussions',
        'discussions': discussions,
        'page_objects': page_objects,
        'page_range': paginator.page_range,  # paginator.page_range用于获取一共有多少页
        'page_now': page_now,
    }

    return render(request, 'Discussion/discussions.html', context=data)


def add_article_comment(request, article_id):
    username = request.session.get('username')
    if not username:
        return render(request, 'Page Jump/notlogin_to_login.html')

    # print(username)
    user = Person.objects.get(name=username)
    # print("2333")

    if request.method == 'GET':
        return render(request, 'Blog/add_comment.html', {'article_id': article_id})
    elif request.method == 'POST':
        article = Article.objects.get(id=article_id)
        comment = ArticleComment()
        comment.owner = user
        comment.article = article
        article.comments_num += 1
        comment.content = request.POST.get('content')
        comment.save()
        article.save()
        message = Notice()
        message.message_type = 1
        message.receiver_id = comment.article.author.id
        message.sender = user
        message.article_comment = comment
        message.article = comment.article
        message.save()

        return redirect(reverse('app1:show_article', kwargs={'article_id': article_id}))


def delete_discussion(request, discussion_id):
    username = request.session.get('username')
    if not username:
        return render(request, 'Page Jump/notlogin_to_login.html')

    discussion = Discussion.objects.get(id=discussion_id)

    if username != discussion.owner.name:
        return render(request, 'Wrong Page/noRight.html')

    discussion.delete()
    return render(request, 'Page Jump/delete_success.html')


def recommend_discussion(request):  # 给帖子点赞
    discussion_id = request.GET.get('discussion_id')
    fan_id = request.GET.get('fan_id')
    relations = LikeDiscussion.objects.filter(fan_id=fan_id).filter(discussion_id=discussion_id)
    if relations.exists():
        data = {
            'status': 400,
            'msg': 'already exists',
        }
    else:
        Relation = LikeDiscussion()
        Relation.discussion_id = discussion_id
        Relation.fan_id = fan_id
        Relation.save()
        data = {
            'status': 200,
            'msg': 'add success',
        }
    return JsonResponse(data=data)


def mark_discussion(request):  # 给博客点赞
    discussion_id = request.GET.get('discussion_id')
    fan_id = request.GET.get('fan_id')
    relations = MarkDiscussion.objects.filter(fan_id=fan_id).filter(discussion_id=discussion_id)
    if relations.exists():
        data = {
            'status': 400,
            'msg': 'already exists',
        }
    else:
        Relation = MarkDiscussion()
        Relation.discussion_id = discussion_id
        Relation.fan_id = fan_id
        Relation.save()
        data = {
            'status': 200,
            'msg': 'add success',
        }
    return JsonResponse(data=data)


def add_discussion_comment(request, discussion_id):
    username = request.session.get('username')
    if not username:
        return render(request, 'Page Jump/notlogin_to_login.html')

    user = Person.objects.get(name=username)

    if request.method == 'GET':
        return render(request, 'Discussion/add_comment.html', {'discussion_id': discussion_id})
    elif request.method == 'POST':
        discussion = Discussion.objects.get(id=discussion_id)
        comment = DiscussionResponse()
        comment.owner = user
        comment.discussion = discussion
        discussion.comments_num += 1
        discussion.last_comment_time = timezone.now()
        comment.content = request.POST.get('content')
        comment.save()
        discussion.save()
        message = Notice()
        message.message_type = 2
        message.receiver_id = comment.discussion.owner.id
        message.sender = comment.owner
        message.discussion = comment.discussion
        message.discussion_response = comment
        message.save()

        return redirect(reverse('app1:show_discussion', kwargs={'discussion_id': discussion_id, 'order_type': '0'}))


def recommend_discussion_response(request, comment_id, fan_id):
    # comment_id = request.GET.get('comment_id')
    # fan_id = request.GET.get('fan_id')
    relations = LikeDiscussionResponse.objects.filter(fan_id=fan_id).filter(comment_id=comment_id)
    comment = DiscussionResponse.objects.get(id=comment_id)
    if relations.exists():
        pass
    #     data = {
    #         'status': 400,
    #         'msg': 'already exists',
    #     }
    else:
        Relation = LikeDiscussionResponse()
        Relation.comment_id = comment_id
        Relation.fan_id = fan_id
        Relation.save()

        comment.likes_num += 1
        comment.save()

        message = Notice()
        message.message_type = 3
        message.receiver_id = comment.owner.id
        message.sender = Person.objects.get(id=fan_id)
        message.discussion_response = comment
        message.discussion = comment.discussion
        message.save()

        # data = {
        #     'status': 200,
        #     'msg': 'add success',
        # }
    return redirect(reverse('app1:show_discussion', kwargs={'discussion_id': comment.discussion.id, 'order_type': '0'}))


def explore(request):
    data = {
        'title': 'Explore',
    }
    return render(request, 'Explore/expolre.html', context=data)


def my_collected_articles(request):
    username = request.session.get('username')
    if not username:
        return render(request, 'Page Jump/notlogin_to_login.html')

    user = Person.objects.get(name=username)
    # articles = Article.objects.filter(author=user)
    relations = MarkArticle.objects.filter(fan_id=user.id)
    articles = []
    for relation in relations:
        arti = Article.objects.filter(id=relation.article_id)
        if arti.exists():
            article = arti.first()
            articles.append(article)

    data = {
        'articles': articles,
        'title': 'My collection',
    }

    return render(request, 'Blog/my_collected_blogs.html', context=data)


def my_fans(request):
    username = request.session.get('username')
    if not username:
        return render(request, 'Page Jump/notlogin_to_login.html')

    user = Person.objects.get(name=username)
    relations = Likes.objects.filter(star_id=user.id)

    fans = []
    for relation in relations:
        fan = Person.objects.get(id=relation.fan_id)
        fans.append(fan)

    data = {
        'title': '我的粉丝',
        'fans': fans,
    }

    return render(request, 'UserManager/my_fans.html', context=data)


def my_idols(request):
    username = request.session.get('username')
    if not username:
        return render(request, 'Page Jump/notlogin_to_login.html')

    user = Person.objects.get(name=username)
    relations = Likes.objects.filter(fan_id=user.id)

    idols = []
    for relation in relations:
        idol = Person.objects.get(id=relation.star_id)
        idols.append(idol)

    data = {
        'title': '我的关注',
        'idols': idols,
    }

    return render(request, 'UserManager/my_idols.html', context=data)


def edit_blog(request, article_id):
    article = Article.objects.get(pk=article_id)
    if request.method == 'GET':
        data = {
            'title': 'Edit Blog',
            'article': article,
        }
        return render(request, 'Blog/edit_blog.html', context=data)
    elif request.method == 'POST':
        article.title = request.POST.get('title')
        article.content = request.POST.get('content')
        article.save()
        return redirect(reverse('app1:show_article', kwargs={'article_id': article.id}))


def search_blog(request):
    if request.method == 'POST':
        search_ob = request.POST.get('search_ob')
        search_ob = search_ob.replace(' ', '')
        raw_sql = "select * from app1_article where title like concat(%s,%s,%s) order by -hot"
        pattern = re.compile('.{1}')
        search_ob = '%'.join(pattern.findall(search_ob))
        print(search_ob)

        aim_blogs = Article.objects.raw(raw_sql, params=['%',search_ob,'%'])

        # aim_blogs = Article.objects.filter(title__contains=search_ob)
        data = {
            'aim_blogs': aim_blogs,
        }
        return render(request, 'Blog/search_consequences.html', context=data)


def search_discussion(request):
    if request.method == 'POST':
        search_ob = request.POST.get('search_ob')
        search_ob = search_ob.replace(' ','')
        raw_sql = "select * from app1_discussion where title like concat(%s,%s,%s) order by -comments_num"
        pattern = re.compile('.{1}')
        search_ob = '%'.join(pattern.findall(search_ob))

        aim_discussions = Discussion.objects.raw(raw_sql,params=['%',search_ob,'%'])

        data = {
            'aim_discussions': aim_discussions,
        }
        return render(request, 'Discussion/search_consequence.html', context=data)


def search_user(request):
    if request.method == 'GET':
        return render(request, 'UserManager/search_user.html', {'title': '添加关注'})
    elif request.method == 'POST':
        search_ob = request.POST.get('search_ob')
        aim_users = Person.objects.filter(Q(mail__iexact=search_ob) | Q(name__icontains=search_ob))

        data = {
            'aim_users': aim_users,
            'title': '添加关注',
        }
        return render(request, 'UserManager/search_user_consequence.html', context=data)


def his_home(request, person_id):
    user = Person.objects.get(pk=person_id)
    my_name = request.session.get('username')
    if not my_name:
        return render(request, 'Page Jump/notlogin_to_login.html')
    if my_name == user.name:
        page_now = int(request.GET.get('page', 1))
        per_page = 10
        articles = user.article_set.all().order_by('-id')  # 新发表的(id值大的)排在前面
        paginator = Paginator(articles, per_page)
        page_objects = paginator.page(page_now)
        context = {
            'title': user.name + '\'s home',
            'user': user,
            'icon_url': '/static/uploadfiles/' + user.icon.url,
            'page_objects': page_objects,
            'page_range': paginator.page_range,  # paginator.page_range用于获取一共有多少页
            'page_now': page_now,
        }
        return render(request, 'UserManager/home.html', context=context)

    me = Person.objects.get(name=my_name)
    data = {
        'title': user.name + "'s home",
        'user': user,
        'me': me,
        'icon_url': '/static/uploadfiles/' + user.icon.url,
    }
    return render(request, 'UserManager/his_home.html', context=data)


def his_blog(request, person_id):
    user = Person.objects.get(pk=person_id)
    articles = Article.objects.filter(author=user)
    for article in articles:
        article.content = article.content[:90]
    data = {
        'title': user.name + '\'s Blogs',
        'articles': articles,
    }
    return render(request, 'Blog/my_blog.html', context=data)


def his_discussion(request, person_id):
    user = Person.objects.get(pk=person_id)
    discussions = Discussion.objects.filter(owner=user)
    data = {
        'discussions': discussions,
        'title': user.name + '\'s discussions',
    }
    return render(request, 'Discussion/my_discussion.html', context=data)


def his_idols(request, person_id):
    user = Person.objects.get(pk=person_id)
    relations = Likes.objects.filter(fan_id=user.id)
    idols = []
    for relation in relations:
        idol = Person.objects.get(id=relation.star_id)
        idols.append(idol)

    data = {
        'title': user.name + '的关注',
        'idols': idols,
    }

    return render(request, 'UserManager/my_idols.html', context=data)


def his_fans(request, person_id):
    user = Person.objects.get(pk=person_id)
    relations = Likes.objects.filter(star_id=user.id)
    fans = []
    for relation in relations:
        fan = Person.objects.get(id=relation.fan_id)
        fans.append(fan)

    data = {
        'title': user.name + '的粉丝',
        'fans': fans,
    }
    return render(request, 'UserManager/my_fans.html', context=data)


def my_collected_discussions(request):
    username = request.session.get('username')
    user = Person.objects.get(name=username)
    relations = MarkDiscussion.objects.filter(fan_id=user.id)
    discussions = []
    for relation in relations:
        disc = Discussion.objects.filter(id=relation.discussion_id)
        if disc.exists():
            discussion = disc.first()
            discussions.append(discussion)

    data = {
        'discussions': discussions,
        'title': 'My collection',
    }
    return render(request, 'Discussion/my_collected_discussions.html', context=data)


def delete_comment(request, comment_id):
    try:
        comment = DiscussionResponse.objects.get(pk=comment_id)
        discussion_id = comment.discussion.id
        user = comment.owner
        if user.name != request.session['username']:
            return render(request, 'Wrong Page/noRight.html')
        comment.delete()
        return redirect(reverse('app1:show_discussion', kwargs={'discussion_id': discussion_id, 'order_type': '0'}))
    except Exception as e:
        return HttpResponse("此评论不存在哟~")


def unlike_relationship(request):
    star_id = request.GET.get('star_id')
    fan_id = request.GET.get('fan_id')
    relation = Likes.objects.filter(fan_id=fan_id).filter(star_id=star_id)
    if relation.exists():
        relation.delete()
        star = Person.objects.get(id=star_id)
        star.fans_num -= 1
        star.save()
        data = {
            'status': 200,
            'msg': 'delete success',
        }
    else:
        data = {
            'status': 400,
            'msg': 'already delete',
        }
    return JsonResponse(data=data)


def message_box(request):
    if request.method == 'GET':
        username = request.session.get('username')
        user = Person.objects.get(name=username)
        messages = Notice.objects.filter(receiver_id=user.id).order_by('-id')
        data = {
            'title': 'Message Box',
            'user': user,
            'messages': messages,
        }
        return render(request, 'UserManager/message_box.html', context=data)
    elif request.method == 'POST':
        username = request.session.get('username')
        user = Person.objects.get(name=username)
        messages = Notice.objects.filter(receiver_id=user.id).order_by('-id')
        for message in messages:
            message.have_read = 1
            message.save()
        data = {
            'title': 'Message Box',
            'user': user,
            'messages': messages,
        }
        return render(request, 'UserManager/message_box.html', context=data)


def get_label(request, label_type):
    labels = BlogLabel.objects.all().order_by('-id')
    label_type_backup = int(label_type)
    cor_articles = []
    for label in labels:
        while label_type_backup > 1:
            label.have_label = label.have_label // 10
            label_type_backup -= 1
        if label.have_label % 10 == 1:
            article = Article.objects.get(id=label.article_id)
            cor_articles.append(article)
        label_type_backup = int(label_type)
    data = {
        'articles': cor_articles,
        'label_type': label_type,
    }
    return render(request, 'Blog/blogs_with_label.html', context=data)


def get_d_label(request, label_type):
    labels = DiscussionLabel.objects.all().order_by('-id')
    label_type_backup = int(label_type)
    cor_discussions = []
    for label in labels:
        while label_type_backup > 1:
            label.have_label = label.have_label // 10
            label_type_backup -= 1
        if label.have_label % 10 == 1:
            discussion = Discussion.objects.get(id=label.discussion_id)
            cor_discussions.append(discussion)
        label_type_backup = int(label_type)
    data = {
        'discussions': cor_discussions,
        'label_type': label_type,
    }
    return render(request, 'Discussion/discussions_with_label.html', context=data)


def add_label(request):
    label_name = request.GET.get('labelname')
    label_name = label_name.strip()
    label = UserLabel.objects.filter(name=label_name)
    if label.exists() :
        data = {
            'status': 901,
            'msg': 'Label already exists',
        }
    else :
        username = request.session.get('username')
        user = Person.objects.get(name=username)
        label = UserLabel()
        label.name = label_name
        label.owner = user
        label.save()
        data = {
            'status': 200,
            'msg': 'Add success',
        }
    return JsonResponse(data=data)


# def refresh_label(request):
#     username = request.session.get('username')
#     user = Person.objects.get(name=username)
#     labels = UserLabel.objects.filter(owner=user)
#     labelnames = []
#     for label in labels :
#         labelnames.append(label.name)
#     data = {
#
#     }

def random_discussion(request):
    random_range = Discussion.objects.last().id
    aim_id = random.randint(1, random_range)
    if Discussion.objects.filter(id=aim_id).exists():
        url = reverse('app1:show_discussion', kwargs={'discussion_id': aim_id, 'order_type': 0})
        return redirect(url)
    else:
        return HttpResponse("暂时找不到问题噢,请稍后再试一次~")


def calculate_hot(request):
    articles = Article.objects.all()
    for article in articles:
        time_now = timezone.now()
        time_diff = time.mktime(time_now.timetuple()) - time.mktime(article.add_time.timetuple())
        if time_diff < 86400: #1day
            time_value = 0.10
        elif time_diff < 259200: #3days
            time_value = 0.08
        elif time_diff < 604800: #7days
            time_value = 0.05
        elif time_diff < 2592000: #1month
            time_value = 0.03
        else: #time_value随用户量作相应变化
            time_value = 0.01
        article.hot = article.comments_num + article.likes_num + (article.author.fans_num / 10)\
                      + (article.read_num / 10) + time_value
        article.save()
    return HttpResponse("Modify successfully.")


def random_blog(request):
    random_range = Article.objects.last().id
    aim_id = random.randint(1, random_range)
    if Article.objects.filter(id=aim_id).exists():
        url = reverse('app1:show_article', kwargs={'article_id': aim_id})
        return redirect(url)
    else:
        return HttpResponse("暂时找不到文章噢,请稍后再试一次~")