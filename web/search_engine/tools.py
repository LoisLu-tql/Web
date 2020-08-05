from app1.models import Article
from lxml import etree


def is_chinese(ch):
    if u'\u4e00' <= ch <= u'\u9fff' :
        return True
    return False

def is_english(ch):
    if ch.isalpha():
        return True
    return False

def is_digit(ch):
    if ch.isdigit():
        return True
    return False

# 判断是否为中文,英文,数字,连接词
def is_cde(ch):
    if is_chinese(ch) or is_digit(ch) or is_english(ch) :
        return True
    conjuction_list = ['-','_']    # 连接词列表,需手动添加
    if ch in conjuction_list :
        return True
    return False

# 用标点符号和空格为文段分段,分段之间以' '连接
def make_subsection(text):
    text = text.replace('&nbsp;',' ')
    print(len(text))
    print(text)
    res = ''
    for i in range(len(text)):
        if is_cde(text[i]):
            res += text[i]
            continue
        res += ' '
        i += 1
        while i < len(text) and (not is_cde(text[i]) ):
            i += 1
    res = ' '.join(res.split())
    print(len(res))
    print(res)

    return res

# 排序功能已经过小样本测试 可正常使用
def sort_by_hot(list, l, r):
    if l >= r :
        return None
    ll = l
    rr = r
    sdd = list[ll].hot
    while ll < rr :
        while list[ll].hot < sdd and ll < r :
            ll += 1
        while list[rr].hot >= sdd and rr > l :
            rr -= 1
        if ll >= rr :
            break
        tt = Article()
        tt = list[ll]
        list[ll] = list[rr]
        list[rr] = tt
    mm = rr
    sort_by_hot(list, l, mm)
    sort_by_hot(list, mm+1, r)
    return None

def clone_list(list):
    res = list[:]
    return res

def delete_htmltag(text):
    response = etree.HTML(text=text)
    text = response.xpath('string(.)')
    return text










