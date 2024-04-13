from django.db import models
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
# Create your models here.

class CourseOrg(models.Model):
    name = models.CharField(default='',verbose_name='用户名', max_length=32)
    avatar = models.ImageField(default='',verbose_name='头像', upload_to='picture/')
    def __str__(self):
        return self.name

class Account(models.Model):
    """用户表"""
    username = models.CharField(max_length=64,unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    register_data = models.DateTimeField(auto_now_add=True)
    signature = models.CharField(max_length=255,null=True,blank=True)
    avatar = models.ForeignKey("CourseOrg",related_name="account",on_delete=models.CASCADE)
    def __str__(self):
        return self.username

class Article(models.Model):
    """文章表"""
    title = models.CharField(max_length=64,unique=True)
    content = models.TextField()
    account = models.ForeignKey("Account",related_name="article",on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag",null=True,blank=True)
    pub_date = models.DateTimeField(verbose_name="更新时间",editable=True,null=True)
    read_count =models.IntegerField(default=0)
    like_count =models.IntegerField(default=0)
    def __str__(self):
        return "%s - %s" % (self.title,self.account)


class Tag(models.Model):
    """标签表"""
    name = models.CharField(max_length=64,unique=True)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Comment(models.Model):
    "评论表"
    content = models.TextField()
    account = models.ForeignKey("Account",related_name="comment", on_delete=models.CASCADE)
    article = models.ForeignKey("Article",related_name="comment", on_delete=models.CASCADE)
    avatar = models.ForeignKey("CourseOrg",related_name="comment",on_delete=models.CASCADE)
    pub_date = models.DateTimeField()

class Attention(models.Model):
    """标签表"""
    name = models.CharField(max_length=64)#关注人名字
    accounts = models.ManyToManyField("Account",related_name="attend",null=True,blank=True)#关注此人的用户
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name