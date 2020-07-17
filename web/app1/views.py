import uuid
from io import BytesIO
import random

from PIL import Image, ImageFont
from PIL.ImageDraw import ImageDraw
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from app1.models import Article, Person, Likes, Discussion, LikeArticle, MarkArticle, ArticleComment, LikeDiscussion, \
    MarkDiscussion, DiscussionResponse, LikeDiscussionResponse, Notice, BlogLabel, DiscussionLabel
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
            context = {
                'title': 'Add article',
            }
            return render(request, 'Blog/add_article.html', context)
        else:
            article = Article()
            article.title = request.POST.get('title')
            article.content = request.POST.get('content')
            article.author = user
            article.save()

            blog_label = BlogLabel()
            blog_label.article_id = article.id
            labels = request.POST.getlist("item")
            if len(labels) == 1:
                blog_label.label_1 = labels[0]
            elif len(labels) == 2:
                blog_label.label_1 = labels[0]
                blog_label.label_2 = labels[1]
            elif len(labels) == 3:
                blog_label.label_1 = labels[0]
                blog_label.label_2 = labels[1]
                blog_label.label_3 = labels[2]
            blog_label.save()

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
    data = {
        'title': article.title,
        'article': article,
        'comments': comments,
    }
    try:
        blog_label = BlogLabel.objects.get(article_id=article.id)
        data['blog_label'] = blog_label
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
    articles = Article.objects.filter(author=user)

    for article in articles:
        article.content = article.content[:90]

    context = {
        'title': 'My Blogs',
        'articles': articles,
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


def blogs(request):
    page_now = int(request.GET.get('page', 1))
    per_page = 10

    blogs = Article.objects.all().order_by('-id')  # 新发表的(id值大的)排在前面
    paginator = Paginator(blogs, per_page)
    page_objects = paginator.page(page_now)

    for blog in blogs:
        blog.content = blog.content[:50]

    data = {
        'blogs': blogs,
        'page_objects': page_objects,
        'page_range': paginator.page_range,  # paginator.page_range用于获取一共有多少页
        'page_now': page_now,
        'title': 'Blog',
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
        if len(labels) == 1:
            discussion_label.label_1 = labels[0]
        elif len(labels) == 2:
            discussion_label.label_1 = labels[0]
            discussion_label.label_2 = labels[1]
        elif len(labels) == 3:
            discussion_label.label_1 = labels[0]
            discussion_label.label_2 = labels[1]
            discussion_label.label_3 = labels[2]
        discussion_label.save()

        return redirect(reverse('app1:home'))


def my_discussion(request):
    username = request.session.get('username')
    if not username:
        return render(request, 'Page Jump/notlogin_to_login.html')
    user = Person.objects.get(name=username)
    discussions = Discussion.objects.filter(owner=user)
    data = {
        'discussions': discussions,
        'title': 'My discussions',
    }
    return render(request, 'Discussion/my_discussion.html', context=data)


def show_discussion(request, discussion_id):
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

    comments = DiscussionResponse.objects.filter(discussion=discussion)

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
        data['discussion_label'] = discussion_label
        is_label = True
    except Exception as e:
        is_label = False
    data['is_label'] = is_label
    return render(request, 'Discussion/show_discussion.html', context=data)


def discussions(request):
    page_now = int(request.GET.get('page', 1))
    per_page = 10

    discussions = Discussion.objects.all().order_by('-id')  # 新发表的(id值大的)排在前面
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
        comment = ArticleComment()
        comment.owner = user
        comment.article = Article.objects.get(id=article_id)
        comment.content = request.POST.get('content')
        comment.save()

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
        comment = DiscussionResponse()
        comment.owner = user
        comment.discussion = Discussion.objects.get(id=discussion_id)
        comment.content = request.POST.get('content')
        comment.save()

        message = Notice()
        message.message_type = 2
        message.receiver_id = comment.discussion.owner.id
        message.sender = comment.owner
        message.discussion = comment.discussion
        message.discussion_response = comment
        message.save()

        return redirect(reverse('app1:show_discussion', kwargs={'discussion_id': discussion_id}))


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
    return redirect(reverse('app1:show_discussion', kwargs={'discussion_id': comment.discussion.id}))


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
        return HttpResponse('Edit successfully.')


def search_blog(request):
    if request.method == 'POST':
        search_ob = request.POST.get('search_ob')
        aim_blogs = Article.objects.filter(title__icontains=search_ob)
        data = {
            'aim_blogs': aim_blogs,
        }
        return render(request, 'Blog/search_consequences.html', context=data)


def search_discussion(request):
    if request.method == 'POST':
        search_ob = request.POST.get('search_ob')
        aim_discussions = Discussion.objects.filter(title__icontains=search_ob)
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
        return redirect(reverse('app1:show_discussion', args=[discussion_id]))
    except Exception as e:
        return HttpResponse("此评论不存在哟~")


def unlike_relationship(request):
    star_id = request.GET.get('star_id')
    fan_id = request.GET.get('fan_id')
    relation = Likes.objects.filter(fan_id=fan_id).filter(star_id=star_id)
    if relation.exists():
        relation.delete()
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
    if label_type == '1':
        labels = BlogLabel.objects.filter(Q(label_1='习题解答') | Q(label_2='习题解答') | Q(label_3='习题解答'))
        label_name = '习题解答'
    elif label_type == '2':
        labels = BlogLabel.objects.filter(Q(label_1='数学建模') | Q(label_2='数学建模') | Q(label_3='数学建模'))
        label_name = '数学建模'
    elif label_type == '3':
        labels = BlogLabel.objects.filter(Q(label_1='数据结构与算法') | Q(label_2='数据结构与算法') | Q(label_3='数据结构与算法'))
        label_name = '数据结构与算法'
    elif label_type == '4':
        labels = BlogLabel.objects.filter(Q(label_1='学习资料') | Q(label_2='学习资料') | Q(label_3='学习资料'))
        label_name = '学习资料'
    elif label_type == '5':
        labels = BlogLabel.objects.filter(Q(label_1='考研') | Q(label_2='考研') | Q(label_3='考研'))
        label_name = '考研'
    elif label_type == '6':
        labels = BlogLabel.objects.filter(Q(label_1='校园生活') | Q(label_2='校园生活') | Q(label_3='校园生活'))
        label_name = '校园生活'
    else:
        labels = BlogLabel.objects.filter(Q(label_1='经验分享') | Q(label_2='经验分享') | Q(label_3='经验分享'))
        label_name = '经验分享'

    articles = []
    for label in labels:
        article = Article.objects.get(id=label.article_id)
        articles.append(article)
    data = {
        'articles': articles,
        'label_name': label_name,
    }
    return render(request, 'Blog/blogs_with_label.html', context=data)


def get_d_label(request, label_type):
    labels = DiscussionLabel.objects.filter(Q(label_1=label_type) | Q(label_2=label_type) | Q(label_3=label_type))
    discussions = []
    for label in labels:
        discussion = Discussion.objects.get(id=label.discussion_id)
        discussions.append(discussion)
    data = {
        'discussions': discussions,
        'label_type': label_type,
    }
    return render(request, 'Discussion/discussions_with_label.html', context=data)
