from django.shortcuts import render,redirect,reverse
from django.shortcuts import HttpResponse
from myfirstapp import models
import json
from django.core.paginator import Paginator
from django.template import loader
from django.http import JsonResponse
from django.utils import timezone

# Create your views here.
#显示热点博客
def hot(request):
    article_id_list=[]
    article_content_list = []
    article_len =len(models.Tag.objects.all())
    for i in range(article_len):
        # 获得标签
        tag = models.Tag.objects.filter(id=(i+1)).first()
        # 获得最新的文章
        article= tag.article_set.all().order_by('-id')[0]
        #传id（json）
        article_id_list.append(json.dumps(article.id))
        #传内容（json）
        article_content_list.append(json.dumps(article.content))
    article = models.Article.objects.all()
    list_= article.order_by('-read_count')[:10]
    titlelist = []  # 存放标题
    readlist = []  # 存放阅读数
    if list_:
        for i in range(10 if len(list_)>=10 else len(list_)):
            titlelist.append(list_[i].title)
            readlist.append(list_[i].read_count)

    return render(request,'hot.html',{'article_id_list':article_id_list,
                                      'article_content_list':article_content_list,
                                      'titlelist':titlelist,
                                      'readlist':readlist,
                                      })
#显示我的博客
def article(request):
    cookie_dict = request.COOKIES
    context = {}
    status = "notlogined"  # 判断是否在线
    user_id = "none"
    find = 'user_id' in cookie_dict.keys()  # 判断是否有用户登录
    if find:
        status = "logined"
        user_id = request.COOKIES['user_id']
        #--------------------------------------
        #实现分页功能
        user = models.Account.objects.filter(id=user_id)[0]
        data = user.article.all()
        # 得到get请求中的页码参数
        page_num = request.GET.get('page', 1)
        # 实例化一个分页器
        paginator = Paginator(data, 8)
        # 通过页码获得对应的文章，可以使用paginator.page， 但是这个方法不能对get获得的数据进行筛选，所以使用get_page
        article_list = paginator.get_page(page_num)
        # 前端页面参数字典
        context['status'] = json.dumps(status)
        context['data'] = article_list.object_list
        context['obj'] = article_list
        # context['user'] = request.user
        # 判断是否当前页是否是第一页
        if int(article_list.number) == 1:
            # 总页数超过3页
            if (int(article_list.number) + 2) <= paginator.num_pages:
                context["page_num"] = range(int(article_list.number), int(article_list.number) + 3)
            else:
                context["page_num"] = range(int(article_list.number), int(paginator.num_pages) + 1)
        # 判断是否是最后一页
        elif not article_list.has_next():
            if (int(article_list.number) - 2) > 0:
                context["page_num"] = range(int(article_list.number) - 2, int(article_list.number) + 1)
            else:
                context["page_num"] = range(1, int(article_list.number) + 1)
        else:
            if (int(article_list.number) - 1) > 0 and (int(article_list.number) + 1) <= paginator.num_pages:
                context['page_num'] = range(int(article_list.number) - 1, int(article_list.number) + 2)
            elif (int(article_list.number) - 1) <= 0 and (int(article_list.number) + 1) <= paginator.num_pages:
                context['page_num'] = range(1, int(article_list.number) + 2)
            else:
                context['page_num'] = range(1, int(article_list.number) + 1)

    #--------------------------------------
        article_list = []
        for i in data:
            article_list.append(i.title)

        context['json'] = json.dumps(article_list)  # 传回一个json类型，供jquery使用
    else:
        context['status'] = json.dumps(status)
        context['data'] = None
        context['obj'] = None
        context['json'] = None
    return render(request, 'article.html', context)
#用于登录后用户信息获取
def home(request):
    cookie_dict = request.COOKIES
    context = {}
    status = "notlogined"  # 判断是否在线
    user_id = "none"
    find = 'user_id' in cookie_dict.keys()  # 判断是否有用户登录
    follower_list = []
    follower_list_json = []
    if find:
        status = "logined"
        user_id = request.COOKIES['user_id']
        user = models.Account.objects.filter(id=user_id)[0]
        context['user']=user
        # --------------------------------------
        # 实现分页功能
        data = models.Article.objects.all()
        # 得到get请求中的页码参数
        page_num = request.GET.get('page', 1)
        # 实例化一个分页器
        paginator = Paginator(data, 8)
        # 通过页码获得对应的文章，可以使用paginator.page， 但是这个方法不能对get获得的数据进行筛选，所以使用get_page
        article_list = paginator.get_page(page_num)
        # 前端页面参数字典
        context['status'] = json.dumps(status)
        context['data'] = article_list.object_list
        context['obj'] = article_list
        # context['user'] = request.user
        # 判断是否当前页是否是第一页
        if int(article_list.number) == 1:
            # 总页数超过3页
            if (int(article_list.number) + 2) <= paginator.num_pages:
                context["page_num"] = range(int(article_list.number), int(article_list.number) + 3)
            else:
                context["page_num"] = range(int(article_list.number), int(paginator.num_pages) + 1)
        # 判断是否是最后一页
        elif not article_list.has_next():
            if (int(article_list.number) - 2) > 0:
                context["page_num"] = range(int(article_list.number) - 2, int(article_list.number) + 1)
            else:
                context["page_num"] = range(1, int(article_list.number) + 1)
        else:
            if (int(article_list.number) - 1) > 0 and (int(article_list.number) + 1) <= paginator.num_pages:
                context['page_num'] = range(int(article_list.number) - 1, int(article_list.number) + 2)
            elif (int(article_list.number) - 1) <= 0 and (int(article_list.number) + 1) <= paginator.num_pages:
                context['page_num'] = range(1, int(article_list.number) + 2)
            else:
                context['page_num'] = range(1, int(article_list.number) + 1)

        # --------------------------------------
        article_list = []
        for i in data:
            article_list.append(i.title)

        context['json'] = json.dumps(article_list)  # 传回一个json类型，供jquery使用
    else:
        context['status'] = json.dumps(status)
        context['data'] = None
        context['obj'] = None
        context['json'] = None

    return render(request, 'home.html',context)

def follow(request):
    cookie_dict = request.COOKIES
    status = "notlogined"  # 判断是否在线
    user = "none"
    find = 'user_id' in cookie_dict.keys()  # 判断是否有用户登录
    follower_list = []
    follower_list_json = []
    if find:
        status = "logined"
        user_id = request.COOKIES['user_id']
        user = models.Account.objects.filter(id=user_id)[0]
        attender = models.Attention.objects.filter(name=user.username)
        if (attender):
            follower_list = attender[0].accounts.all()
            for i in range(len(follower_list)):
                follower_list_json.append(follower_list[i].username)
        myidol_list = user.attend.all()


    return render(request, 'follow.html',{'status': json.dumps(status),
                                         'user': user,
                                         'follower_list': follower_list,
                                         'follower_list_json': follower_list_json,
                                         'myidol_list': myidol_list
                                         })
#根据id获得用户名
def getusername(request):
    user_id = request.GET.get('user_id')
    user = models.Account.objects.filter(id=user_id)[0]
    username = user.username
    return JsonResponse(username, safe=False)
#读博客
def read(request):
    article_id = request.GET.get('article_id')#读取文章信息
    status ='notread'#判断是否读入
    comment_account_list=[]#每个评论人的对象列表
    tags_list=[]
    cookie_dict = request.COOKIES
    if (article_id):#读入文章
        status ='read'
        article = models.Article.objects.filter(id=article_id)[0]
        tags = article.tags.all()
        for tag in tags:
            tags_list.append(tag)  # tag的数组形式
        # 获取评论内容
        # 传入文章id，标签给jquery
        article_id_json = json.dumps(article.id)
        comment_list = article.comment.all()  # 所有评论
        comment_count = len(comment_list)#统计评论数
        # 写入评论人列表
        for comment in comment_list:
            username = comment.account.username
            user = models.Account.objects.filter(username=username)[0]
            comment_account_list.append(user)
        data = request.GET.get('content')
        data_json = json.dumps(data)
        #---------------------------------
        # 如果作者和访问者一样不增加阅读数，否则阅读数加一
        # 判断是否有用户登录
        user_id = request.GET.get('user_id')  # 获取访问者id(返回str)
        Author_id = str(article.account.id)
        author = models.Account.objects.filter(id=Author_id)[0]#获取作者对象显示图片
        print("user_id:",user_id,"article.account.id:",article.account.id)
        if Author_id != user_id:
            article.read_count=add(article.read_count)
        article.save()#完成阅读量增加
        #-------------------------------
        #实现分页功能
        data = article.comment.all()
        # 得到get请求中的页码参数
        page_num = request.GET.get('page', 1)
        # 实例化一个分页器
        paginator = Paginator(data, 8)
        # 通过页码获得对应的文章，可以使用paginator.page， 但是这个方法不能对get获得的数据进行筛选，所以使用get_page
        comment_list = paginator.get_page(page_num)
        # 前端页面参数字典
        # context['user'] = request.user
        # 判断是否当前页是否是第一页
        if int(comment_list.number) == 1:
            # 总页数超过3页
            if (int(comment_list.number) + 2) <= paginator.num_pages:
                page_num = range(int(comment_list.number), int(comment_list.number) + 3)
            else:
                page_num = range(int(comment_list.number), int(paginator.num_pages) + 1)
        # 判断是否是最后一页
        elif not comment_list.has_next():
            if (int(comment_list.number) - 2) > 0:
                page_num = range(int(comment_list.number) - 2, int(comment_list.number) + 1)
            else:
                page_num = range(1, int(comment_list.number) + 1)
        else:
            if (int(comment_list.number) - 1) > 0 and (int(comment_list.number) + 1) <= paginator.num_pages:
                page_num = range(int(comment_list.number) - 1, int(comment_list.number) + 2)
            elif (int(comment_list.number) - 1) <= 0 and (int(comment_list.number) + 1) <= paginator.num_pages:
                page_num = range(1, int(comment_list.number) + 2)
            else:
                page_num = range(1, int(comment_list.number) + 1)
        #print(comment_list[0].avatar.url)
        return render(request, 'read.html', {'status': json.dumps(status),
                                             'article': article,
                                             'tags_list': tags_list,
                                             'data_json': data_json,
                                             'article_id_json': article_id_json,
                                             'comment_list': comment_list,
                                             'comment_count': comment_count,
                                             'comment_account_list':comment_account_list,
                                             'data': comment_list.object_list,
                                             'obj': comment_list,
                                             'page_num': page_num,
                                             'author':author
                                             })
    return render(request, 'read.html',{'status': json.dumps(status)})

#增加阅读量
def add(count):
    count = count+1
    return count
#写博客
def write(request):
    status = "notlogined"  # 判断是否在线
    user_id = "none"
    cookie_dict = request.COOKIES
    find = 'user_id' in cookie_dict.keys()  # 判断是否有用户登录
    if find:
        status = "logined"
    error = '发布成功'
    if request.method == "POST":
        user_id = request.COOKIES['user_id']
        print(user_id)
        title = request.POST.get('title')
        content = request.POST.get('content')
        tags = request.POST.getlist('tags')
        pub_date = timezone.now()
        tags_list=[]
        #获取标签列表
        for i in tags:
            tags = models.Tag.objects.filter(name=i)[0]
            tags_list.append(tags.id)

        title_same = models.Article.objects.filter(title=title).count()
        if title_same==1:
            error= '标题名重复'
            return render(request, 'write.html',{'error':json.dumps(error),'status':json.dumps(status)})
        article = models.Article.objects.create(title=title,
                                                content=content,
                                                account_id =user_id,
                                                pub_date= pub_date)
        article.save()
        article.tags.set(tags_list)#插入标签数据
    return render(request, 'write.html',{'error':json.dumps(error),'status':json.dumps(status)})

def test(request):
    cookie_dict = request.COOKIES
    context = {}
    status = "notlogined"  # 判断是否在线
    user_id = "none"
    find = 'user_id' in cookie_dict.keys()  # 判断是否有用户登录
    if find:
        status = "logined"
        user_id = request.COOKIES['user_id']
        # --------------------------------------
        # 实现分页功能
        data = models.Article.objects.all()
        # 得到get请求中的页码参数
        page_num = request.GET.get('page', 1)
        # 实例化一个分页器
        paginator = Paginator(data, 8)
        # 通过页码获得对应的文章，可以使用paginator.page， 但是这个方法不能对get获得的数据进行筛选，所以使用get_page
        article_list = paginator.get_page(page_num)
        # 前端页面参数字典
        context['status'] = json.dumps(status)
        context['data'] = article_list.object_list
        context['obj'] = article_list
        # context['user'] = request.user
        # 判断是否当前页是否是第一页
        if int(article_list.number) == 1:
            # 总页数超过3页
            if (int(article_list.number) + 2) <= paginator.num_pages:
                context["page_num"] = range(int(article_list.number), int(article_list.number) + 3)
            else:
                context["page_num"] = range(int(article_list.number), int(paginator.num_pages) + 1)
        # 判断是否是最后一页
        elif not article_list.has_next():
            if (int(article_list.number) - 2) > 0:
                context["page_num"] = range(int(article_list.number) - 2, int(article_list.number) + 1)
            else:
                context["page_num"] = range(1, int(article_list.number) + 1)
        else:
            if (int(article_list.number) - 1) > 0 and (int(article_list.number) + 1) <= paginator.num_pages:
                context['page_num'] = range(int(article_list.number) - 1, int(article_list.number) + 2)
            elif (int(article_list.number) - 1) <= 0 and (int(article_list.number) + 1) <= paginator.num_pages:
                context['page_num'] = range(1, int(article_list.number) + 2)
            else:
                context['page_num'] = range(1, int(article_list.number) + 1)

        # --------------------------------------
        article_list = []
        for i in data:
            article_list.append(i.title)

        context['json'] = json.dumps(article_list)  # 传回一个json类型，供jquery使用
    else:
        context['status'] = json.dumps(status)
        context['data'] = None
        context['obj'] = None
        context['json'] = None

    return render(request, 'test.html',context)

def get_photo(request):
    img = request.FILES.get('img')
    user_id = request.POST.get('user_id')
    user = models.Account.objects.filter(id=user_id)[0]
    find = models.CourseOrg.objects.filter(name=img.name)#查看是否已有此图片
    print(find)
    if find:
        user.avatar_id = find[0].id
    else:
        avatar = models.CourseOrg.objects.create(name=img.name, avatar=img)
        user.avatar_id = avatar.id
    user.save()
    return JsonResponse('', safe=False)

def test2(request):
    return render(request, 'test2.html')





#注册
def register(request):
    if request.method == 'POST':
        user = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        sign = request.POST.get('signature')
        user_list = models.Account.objects.filter(username=user)
        email_list = models.Account.objects.filter(email=email)
        if user_list:
            # 注册失败
            error = '用户名已存在！'
            # 返回到注册页面，并且把错误信息报出来
            return render(request, 'register.html',{'message':json.dumps(error)})

        elif email_list:
            # 注册失败
            error = '邮箱地址已存在！'
            # 返回到注册页面，并且把错误信息报出来
            return render(request, 'register.html',{'message':json.dumps(error)})

        else:
            # 数据保存在数据库中，并返回到登录页面
            
            avatar_id = models.CourseOrg.objects.filter(name='初始头像.jpg')[0].id#设置初始头像
            #models.CourseOrg.objects.count()可以记录所有模型数
            user = models.Account.objects.create(username=user,
                                              password=password,
                                              email=email,
                                              avatar_id=avatar_id,
                                              signature=sign)
            user.save()
            success = '注册成功！'
            return render(request, 'register.html', {'message': json.dumps(success)})

    return render(request, 'register.html')


def base(request):
    return render(request, 'base.html')
#登陆
def getlogin(request):
    data=[]
    data.append('0')
    #########################
    username = request.GET.get('username')
    password = request.GET.get('password')

    user = models.Account.objects.filter(username=username).first()

    if user == None:
        message = '用户名错误'
        data.append(message)
        return JsonResponse(data, safe=False)
    if (user.password == password):
        user_id = user.id
        message = 'logined'
        data[0]=user_id
        data.append(message)
        return JsonResponse(data, safe=False)
    else:
        message = '密码错误'
        data.append(message)
        return JsonResponse(data, safe=False)


def login(request):
    return render(request, 'login.html')
#ajax通信
def ajax(request):
    data=[]
    user_id = request.GET.get('user_id')
    content = request.GET.get('content')
    article_id = request.GET.get('id')#读文章id
    user =models.Account.objects.filter(id=user_id)[0]
    avatar_id = user.avatar.id
    comment = models.Comment.objects.create(content=content,
                                            account_id=user_id,
                                            article_id=article_id,
                                            avatar_id=avatar_id,
                                            pub_date=timezone.now())
    comment.save()
    username = models.Account.objects.filter(id=user_id)[0].username
    avatar = models.Account.objects.filter(id=user_id)[0].avatar.avatar.url
    # 处理data
    data.append(username)
    data.append(content)
    data.append(avatar)
    print(avatar)
    # 1.直接返回output_data
    # return output_data
    # 2.也可以返回html元素
    #return render(request,'ajax.html',{'output_data':json.dumps(output_data)})
    return JsonResponse(data, safe=False)

def ajax2(request):
    data = request.GET.get('ajax_input_data');
    output_data = [1,2,3]
    print(data)
    return render(request, 'read.html',{ 'output_data':json.dumps(output_data)})
#个人中心
def personal(request):
    cookie_dict = request.COOKIES
    message = "notlogined"  # 判断是否在线
    user = "none"
    find = 'user_id' in cookie_dict.keys()  # 判断是否有用户登录
    follower_list=[]
    follower_list_json=[]
    context= {}
    if find:
        message = "logined"
        user_id = request.COOKIES['user_id']
        user = models.Account.objects.filter(id=user_id)[0]
        attender = models.Attention.objects.filter(name=user.username)
        if (attender):
            follower_list = attender[0].accounts.all()
            print(follower_list)
            for i in range(len(follower_list)):
                follower_list_json.append(follower_list[i].username)

        #context['follower_list']=follower_list
        #context['follower_list_json'] = follower_list_json
        # --------------------------------------
        # 实现分页功能
        data = user.article.all()
        # 得到get请求中的页码参数
        page_num = request.GET.get('page', 1)
        # 实例化一个分页器
        paginator = Paginator(data, 8)
        # 通过页码获得对应的文章，可以使用paginator.page， 但是这个方法不能对get获得的数据进行筛选，所以使用get_page
        article_list = paginator.get_page(page_num)
        # 前端页面参数字典
        context['status'] = json.dumps(message)
        context['data'] = article_list.object_list
        context['obj'] = article_list
        context['user'] = user
        # context['user'] = request.user
        # 判断是否当前页是否是第一页
        if int(article_list.number) == 1:
            # 总页数超过3页
            if (int(article_list.number) + 2) <= paginator.num_pages:
                context["page_num"] = range(int(article_list.number), int(article_list.number) + 3)
            else:
                context["page_num"] = range(int(article_list.number), int(paginator.num_pages) + 1)
        # 判断是否是最后一页
        elif not article_list.has_next():
            if (int(article_list.number) - 2) > 0:
                context["page_num"] = range(int(article_list.number) - 2, int(article_list.number) + 1)
            else:
                context["page_num"] = range(1, int(article_list.number) + 1)
        else:
            if (int(article_list.number) - 1) > 0 and (int(article_list.number) + 1) <= paginator.num_pages:
                context['page_num'] = range(int(article_list.number) - 1, int(article_list.number) + 2)
            elif (int(article_list.number) - 1) <= 0 and (int(article_list.number) + 1) <= paginator.num_pages:
                context['page_num'] = range(1, int(article_list.number) + 2)
            else:
                context['page_num'] = range(1, int(article_list.number) + 1)

        # --------------------------------------
        article_list = []
        for i in data:
            article_list.append(i.title)

        context['json'] = json.dumps(article_list)  # 传回一个json类型，供jquery使用
    else:
        context['status'] = json.dumps(message)
        context['data'] = None
        context['obj'] = None
        context['json'] = None
        context['user'] = None
        context['follower_list_json'] = None
        context['follower_list_json'] = None
        context['follower_list_json']=None
    return render(request, 'personal.html', context)

#修改数据
def modify_user(request):
    user_id = request.COOKIES['user_id']#获取要修改的用户
    Attributes = request.GET.get('Attributes')#获取要修改的属性值
    print(Attributes)
    content = request.GET.get('content')#获取要修改的内容
    user = models.Account.objects.filter(id=user_id)[0]
    if Attributes=='username':
        user.username=content
    if Attributes == 'email':
        user.email = content
    if Attributes == 'signature':
        user.signature= content
    user.save()

    return JsonResponse(content, safe=False)
"""
def render(request, template_name, context=None, content_type=None, status=None, using=None):

   
    content = loader.render_to_string(template_name, context, request, using=using)
    return HttpResponse(content, content_type, status)
"""
def others_space(request):#在文章中进入别人的空间
    Visitor_id= request.GET.get('Visitor_id')#访问者id
    user_id = request.GET.get('user_id')#空间使用者id
    print(Visitor_id,user_id)
###########
    follower_list = []
    follower_list_json = []
    context = {}
    user = models.Account.objects.filter(id=user_id)[0]

    visitor = models.Account.objects.filter(id=Visitor_id)[0]
    attender = models.Attention.objects.filter(name=user.username)
    status = '0'  # 判断是否关注
    follower_list = []
    follower_list_len = 0
    context['user'] = user
    print("user:", context['user'])
    context['status'] = json.dumps(status)
    context['data'] = None
    context['obj'] = None
    context['json'] = None
    context['follower_list_json'] = None
    if attender:  # 如果此人有人关注返回关注列表
        attender = attender[0]
        follower_list = attender.accounts.all()  # 粉丝列表
        follower_list_len = len(follower_list)
        follower_list_name = []
        for follower in follower_list:  # 将所有粉丝组成数组
            follower_list_name.append(follower.username)
        for name in follower_list_name:
            if name == visitor.username:  # 判断是否已关注
                status = '1'
        context['status'] = json.dumps(status)
        context['follower_list_len'] = follower_list_len

        # --------------------------------------
        # 实现分页功能
        data = user.article.all()
        # 得到get请求中的页码参数
        page_num = request.GET.get('page', 1)
        # 实例化一个分页器
        paginator = Paginator(data, 8)
        # 通过页码获得对应的文章，可以使用paginator.page， 但是这个方法不能对get获得的数据进行筛选，所以使用get_page
        article_list = paginator.get_page(page_num)
        # 前端页面参数字典
        context['data'] = article_list.object_list
        context['obj'] = article_list

        # context['user'] = request.user
        # 判断是否当前页是否是第一页
        if int(article_list.number) == 1:
            # 总页数超过3页
            if (int(article_list.number) + 2) <= paginator.num_pages:
                context["page_num"] = range(int(article_list.number), int(article_list.number) + 3)
            else:
                context["page_num"] = range(int(article_list.number), int(paginator.num_pages) + 1)
        # 判断是否是最后一页
        elif not article_list.has_next():
            if (int(article_list.number) - 2) > 0:
                context["page_num"] = range(int(article_list.number) - 2, int(article_list.number) + 1)
            else:
                context["page_num"] = range(1, int(article_list.number) + 1)
        else:
            if (int(article_list.number) - 1) > 0 and (int(article_list.number) + 1) <= paginator.num_pages:
                context['page_num'] = range(int(article_list.number) - 1, int(article_list.number) + 2)
            elif (int(article_list.number) - 1) <= 0 and (int(article_list.number) + 1) <= paginator.num_pages:
                context['page_num'] = range(1, int(article_list.number) + 2)
            else:
                context['page_num'] = range(1, int(article_list.number) + 1)

            # --------------------------------------
        article_list = []
        for i in data:
            article_list.append(i.title)

        context['json'] = json.dumps(article_list)  # 传回一个json类型，供jquery使用
    else:
        pass
    ###########

    return render(request,'others_space.html',context)

def getid(request):#在我的关注中进入别人的空间
    username = request.GET.get('username')
    print(username)
    user_id = models.Account.objects.filter(username=username)[0].id
    return JsonResponse(user_id,safe=False)

def getmost_read(request):
    article = models.Article.objects.all()
    list = article.order_by('-read_count')[:10]
    titlelist = []#存放标题
    readlist =[]#存放阅读数
    data={}
    for i in range(10):
        titlelist.append(list[i].title)
        readlist.append(list[i].read_count)
    data['titlelist']=titlelist
    data['readlist'] = readlist
    return JsonResponse(data ,safe=False)

def get_tag(request):#根据文章获得标签
    id = request.GET.get('article_id')
    article = models.Article.objects.filter(id=id)[0]
    tags=article.tags.all()
    tag_list=[]
    for tag in tags:
        tag_list.append(tag.name)
    print(tag_list)
    return JsonResponse(tag_list,safe=False)

def attend(request):
    user_id = request.GET.get('user_id')  # 获取要修改的属性值
    follow_list=[]#粉丝列表
    attend_name = request.GET.get('attend_name')  # 获取要修改的属性值
    attend_people = models.Account.objects.filter(username=attend_name)
    #创建关注对象
    name = attend_name#关注人姓名
    find = models.Attention.objects.filter(name=name)#查看是否有此人，有则修改关注对象
    if(find):
        finder = find[0]
        followers = finder.accounts.all()
        for follower in followers:
            follow_list.append(follower.id)
        follow_list.append(user_id)
        finder.accounts.set(follow_list)
    else:
        attend = models.Attention.objects.create(name=name,date=timezone.now())
        attend.save()
        follow_list.append(user_id)
        attend.accounts.set(follow_list)
    return JsonResponse( '', safe=False)