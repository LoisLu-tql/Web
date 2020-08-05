from django.db.models import Q
from django.http import HttpResponse
from lxml import etree

from app1.models import Article
from search_engine.models import InvertedIndex

from search_engine.tools import is_cde, sort_by_hot, clone_list

from search_engine.tools import is_chinese, is_english, is_digit, is_cde, make_subsection

import jieba

def add_to_inverted_index(str, article_id):
    ii = InvertedIndex.objects.filter(str=str).filter(article_id=article_id)
    if not ii.exists() :
        ii = InvertedIndex()
        ii.str = str
        ii.article_id = article_id
        ii.save()
    else :
        ii = ii.first()
        ii.time += 1
    return None

# 这里可直接按显示逐一取出字符,故应该不用考虑字符编码集的转换问题
def add_document(article_id):
    article = Article.objects.get(id=article_id)
    text = article.title + article.content

    # 去除html标签
    response = etree.HTML(text=text)
    text = response.xpath('string(.)')

    # 用标点符号和空格为文段分段,分段之间以' '连接
    text = make_subsection(text)
    sen_list = text.split(' ')

    # 根据jieba分词为语段分词
    jieba.enable_paddle()
    for sen in sen_list :
        seg_list = jieba.cut_for_search(sen, HMM=True)
        for str in seg_list :
            add_to_inverted_index(str, article_id)

    tags = article.tag2
    tag_list = tags.split('#')
    for tag in tag_list :
        tag = tag.strip()
        add_to_inverted_index(tag, article_id)

    return None

# 根据搜索输入的关键字检索文章
def search_blog_by_str(sstring):

    # 根据空格将关键字分开
    sen_list = sstring.split(' ')

    # 提取所有词元
    seg_list = []
    # jieba.enable_paddle()
    for sen in sen_list :
        segs = jieba.cut_for_search(sen, HMM=True)
        for seg in segs :
            seg_list.append(seg)

    article_list1 = Article.objects.all()  # 标题或标签中出现全部关键词
    # article_list2 = Article.objects.all()  # 文章内容中出现全部关键词
    for sen in sen_list :
        article_list1 = article_list1.filter(Q(title__contains=sen) | Q(tag2__contains=sen))
        # article_list2 = article_list2.filter(content__contains=sen)
        if not article_list1.exists() :
            break
    article_list1 = article_list1.order_by('-hot')
    # article_list2 = article_list2.order_by('-hot')

    print(len(article_list1))
    # print(len(article_list2))
    articles = []
    for article in article_list1:
        if not article in articles:
            articles.append(article)

    # for article in article_list2:
    #     if not article in articles:
    #         articles.append(article)
    # for seg in seg_list :
    #     print("seg:")
    #     print(seg)

    if len(seg_list) > 3 :
        article_list = set()
        for i in range(3) :
            artis = Article.objects.filter(Q(title__contains=seg_list[i]) | Q(content__contains=seg_list[i]))
            for article in artis :
                article_list.add(article)
        article_list = list(article_list)

        tim = [0 for i in range(len(article_list))]  # time 记录每个文章中出现的词元个数
        for seg in seg_list :
            iis = InvertedIndex.objects.filter(str=seg)
            for i in range(len(article_list)) :
                ii = iis.filter(article_id=article_list[i].id)
                if ii.exists() :
                    tim[i] += 1

        # for i in range(len(tim)) :
        #     print("tim" + str(i) + ":")
        #     print(tim[i])

        article_list3 = set()
        for i in range(len(tim)) :
            if tim[i] >= len(seg_list)*0.8 :
                article_list3.add(article_list[i])
        article_list3 = list(article_list3)
        sort_by_hot(article_list3, 0, len(article_list3)-1)

        for article in article_list3 :
            if not article in articles :
                articles.append(article)
    else :
        iis = InvertedIndex.objects.filter(str=seg_list[0])
        article_list3 = set()
        for ii in iis :
            article = Article.objects.get(id=ii.article_id)
            article_list3.add(article)
        for seg in seg_list :
            iis = InvertedIndex.objects.filter(str=seg)
            a_l = set()
            for ii in iis :
                article = Article.objects.get(id=ii.article_id)
                a_l.add(article)
            a_l3s = article_list3.copy()
            for article in a_l3s :
                if not article in a_l :
                    article_list3.discard(article)
        article_list3 = list(article_list3)
        sort_by_hot(article_list3, 0, len(article_list3)-1)

        # print(len(article_list3))
        # print(type(articles))

        for article in article_list3 :
            if not article in articles :
                articles.append(article)

    return articles

