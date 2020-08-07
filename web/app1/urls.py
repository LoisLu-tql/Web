from django.conf.urls import url

from app1 import views

urlpatterns = [
    url(r'^helloworld/', views.helloworld, name='helloworld'),

    #url(r'^addarticle/', views.addarticle, name='addarticle'),

    url(r'^register/', views.register, name = 'register'),

    url(r'^get_verify_code/', views.get_verify_code, name = 'get_verify_code'),

    url(r'^checkusername/', views.check_username, name = 'check_username'),

    url(r'^login/', views.login, name = 'login'),

    url(r'^home/', views.home, name = 'home'),

    url(r'^logout/', views.logout, name = 'logout'),

    url(r'^addarticle/', views.add_article, name = 'add_article'),

    url(r'^article/(?P<article_id>\d+)', views.show_article, name = 'show_article'),

    url(r'^addlikerelationship/', views.add_like_relationship, name='add_like_relationship'),

    url(r'^recommendarticle/', views.recommend_article, name='recommend_article'),

    url(r'^markarticle/', views.mark_article, name='mark_article'),

    url(r'^addicon/', views.add_icon, name = 'add_icon'),

    url(r'^myblog/', views.my_blog, name = 'my_blog'),

    url(r'^changepassword/', views.change_password, name='change_password'),

    url(r'^changepasswordcheck/', views.change_password_check, name='change_password_check'),

    url(r'^deletearticle/(?P<article_id>\d+)/', views.delete_article, name = 'delete_article'),

    url(r'^personalinformation/', views.personal_information, name = 'personal_information'),

    url(r'^blogs/(?P<order_type>\d+)/', views.blogs, name = 'blogs'),

    url(r'^adddiscussion/', views.add_discussion, name = 'add_discussion'),

    url(r'^mydiscussion/', views.my_discussion, name='my_discussion'),

    url(r'^show_discussion/(?P<discussion_id>\d+)/(?P<order_type>\d+)/', views.show_discussion, name='show_discussion'),

    url(r'^discussions/', views.discussions, name = 'discussions'),

    url(r'^addarticlecomment/(?P<article_id>\d+)/', views.add_article_comment, name = 'add_article_comment'),

    url(r'^deletediscussion/(?P<discussion_id>\d+)/', views.delete_discussion, name = 'delete_discussion'),

    url(r'^recommenddiscussion/', views.recommend_discussion, name='recommend_discussion'),

    url(r'^markdiscussion/', views.mark_discussion, name='mark_discussion'),

    url(r'^adddiscussioncomment/(?P<discussion_id>\d+)/', views.add_discussion_comment, name = 'add_discussion_comment'),

    url(r'^recommenddiscussionresponse/(?P<comment_id>\d+)/(?P<fan_id>\d+)/', views.recommend_discussion_response, name = 'recommend_discussion_response'),

    url(r'^explore/', views.explore, name = 'explore'),

    url(r'^mycollectedarticles/', views.my_collected_articles, name = 'my_collected_articles'),

    url(r'^myfans/', views.my_fans, name = 'my_fans'),

    url(r'^myidols/', views.my_idols, name = 'my_idols'),
    #add functions
    url(r'^editblog/(?P<article_id>\d+)/', views.edit_blog, name='edit_blog'),

    url(r'^searchblog/', views.search_blog, name='search_blog'),

    url(r'^searchdiscussion/', views.search_discussion, name='search_discussion'),

    url(r'^searchuser/', views.search_user, name='search_user'),

    url(r'^hishome/(?P<person_id>\d+)/', views.his_home, name='his_home'),

    url(r'^hisblog/(?P<person_id>\d+)/', views.his_blog, name='his_blog'),

    url(r'^hisdiscussion/(?P<person_id>\d+)/', views.his_discussion, name='his_discussion'),

    url(r'^hisidols/(?P<person_id>\d+)/', views.his_idols, name='his_idols'),

    url(r'^hisfans/(?P<person_id>\d+)/', views.his_fans, name='his_fans'),

    url(r'^mycollecteddiscussions/', views.my_collected_discussions, name='my_collected_discussions'),

    url(r'^deletecomment/(?P<comment_id>\d+)/', views.delete_comment, name='delete_comment'),

    url(r'^deleteblogcomment/(?P<comment_id>\d+)/', views.delete_blog_comment, name='delete_blog_comment'),

    url(r'^unlikerelationship/', views.unlike_relationship, name='unlike_relationship'),

    url(r'^messagebox/', views.message_box, name='message_box'),

    url(r'^getlabel/(?P<label_type>\d+)/', views.get_label, name='get_label'),

    url(r'^getdlabel/(?P<label_type>\d+)/', views.get_d_label, name='get_d_label'),

    url(r'^addlabel/', views.add_label, name = 'add_label'),

    url(r'^randomdiscussion/', views.random_discussion, name='random_discussion'),

    url(r'^randomblog/', views.random_blog, name='random_blog'),

    url(r'^calculatehot/', views.calculate_hot, name='calculate_hot'),#刷新博客热度排名

    url(r'^chat/(?P<receiver_id>\d+)/(?P<sender_id>\d+)/', views.chat, name='chat'),

    url(r'^chatrooms/', views.chatrooms, name='chatrooms'),

    url(r'^deletechat/(?P<room_id>\d+)/', views.delete_chat, name='delete_chat'),

    url(r'^uncollectblog/(?P<article_id>\d+)/', views.uncollect_blog, name='uncollect_blog'),

    url(r'^uncollectdiscussion/(?P<discussion_id>\d+)/', views.uncollect_discussion, name='uncollect_discussion'),

    url(r'^resdisres/(?P<comment_id>\d+)/(?P<type>\d+)/(?P<discussion_id>\d+)/', views.res_dis_res, name='res_dis_res'),

    # url(r'^refreshlabel/', views.refresh_label, name = 'refresh_label'),

    url(r'^$', views.index, name='index'),

]
