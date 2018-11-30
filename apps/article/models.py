from django.db import models
from datetime import datetime
# from django.template.defaultfilters import slugify
from uuslug import slugify
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.validators import UnicodeUsernameValidator
from mdeditor.fields import MDTextField

class UserProfile(AbstractUser):
    """
    自定义扩展用户
    """
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=20,
        unique=True,
        help_text=_('Required. 20 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(blank=True, null=True,verbose_name="电子邮箱",help_text="电子邮箱")
    avatar = models.ImageField(blank=True, null=True,upload_to="avatar/",default="avatar/default.png",verbose_name="头像",help_text="头像")
    age = models.IntegerField(blank=True, null=True,verbose_name="年龄",help_text="年龄")
    website = models.URLField(blank=True, null=True,verbose_name="个人网站",help_text="个人网站")
    hometown = models.CharField(max_length=64, blank=True, null=True,verbose_name="家乡",help_text="家乡")
    introduction = models.CharField(max_length=128, blank=True, null=True,verbose_name="个人简介",help_text="个人简介")

    class Meta:
        verbose_name="用户"
        verbose_name_plural="用户"

    def get_avatar_url(self):
        if self.socialaccount_set.count():
            return self.socialaccount_set.all()[0].get_avatar_url()
        return None

    def __str__(self):
        return "用户:{0}".format(self.username)


class Article(models.Model):
    """
    文章
    """
    title=models.CharField(max_length=128,verbose_name="标题",help_text="标题")
    post_time=models.DateTimeField(default=datetime.now,verbose_name="发布时间",help_text="发布时间")
    author=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='articles',on_delete=models.CASCADE,verbose_name="作者",help_text="作者")
    content=MDTextField(max_length=1024*20,verbose_name="内容",help_text="内容")
    summary=models.TextField(max_length=514,verbose_name="摘要",help_text="摘要")
    picture=models.ImageField(blank=True,null=True,upload_to='article_images',verbose_name="封面图",help_text="封面图")
    #Tag的实例可以使用t.articles查询相应tag下所有的article
    tags = models.ManyToManyField('Tag',blank=True,related_name='articles',verbose_name="标签",help_text="标签")
    category = models.ManyToManyField('Category',verbose_name="博客分类")
    likes=models.IntegerField(default=0,verbose_name="点赞数",help_text="点赞数")
    views=models.IntegerField(default=0,verbose_name="阅读数",help_text="阅读数")

    class Meta:
        verbose_name="文章"
        verbose_name_plural=verbose_name

    def get_comment_count(self):
        return self.comments.count()+self.sub_comments.count()

    def __str__(self):
        return "文章:%s"%self.title

# 标签
class Tag(models.Model):
    name=models.CharField(max_length=32,unique=True,verbose_name="标签名",help_text="标签名")
    chinese_name=models.CharField(blank=True,null=True,max_length=32,verbose_name="标签中文名",help_text="标签中文名")
    slug=models.SlugField(blank=True,unique=True,verbose_name="标签slug",help_text="标签slug")
    desc=models.CharField(max_length=128,blank=True,null=True,verbose_name="标签描述",help_text="标签描述")

    def save(self, *args, **kw):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kw)

    class Meta:
        verbose_name="标签"
        verbose_name_plural=verbose_name

    def __str__(self):
        return "标签:%s"%self.name

class Comment(models.Model):
    """
    一级评论
    """
    author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name="评论人",help_text="评论人",related_name='comments')
    content=models.TextField(max_length=256,verbose_name="评论内容",help_text="评论内容")
    post_time=models.DateTimeField(default=datetime.now,verbose_name="评论时间",help_text="评论时间")
    article=models.ForeignKey('Article',related_name='comments',on_delete=models.CASCADE,verbose_name="从属文章",help_text="从属文章")

    class Meta:
        verbose_name="一级评论"
        verbose_name_plural=verbose_name

    def __str__(self):
        return '%s关于%s的一级评论(#%s)'%(self.author,self.article,self.id)

class Subcomment(models.Model):
    """
    二级评论
    """
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,verbose_name="评论人",help_text="评论人",related_name='sub_comments')
    content = models.TextField(max_length=256,verbose_name="评论内容",help_text="评论内容")
    post_time = models.DateTimeField(default=datetime.now,verbose_name="评论时间",help_text="评论时间")
    article = models.ForeignKey('Article',on_delete=models.CASCADE,verbose_name="从属文章",help_text="从属文章",related_name='sub_comments')
    parent_comment=models.ForeignKey(Comment,related_name='sub_comments',on_delete=models.CASCADE,verbose_name="父评论",help_text="父评论")
    reply_to=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name="回复给",help_text="回复给")

    class Meta:
        verbose_name="二级评论"
        verbose_name_plural=verbose_name

    def __str__(self):
        return '%s关于%s的二级评论(#%s)回复给%s'%(self.author,self.article,self.id,self.reply_to)

#　博客分类
class Category(models.Model):
    name = models.CharField(max_length=128,verbose_name='博客分类')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '博客分类'
        verbose_name_plural = '博客分类'

#　轮播图
class Carousel(models.Model):
    number = models.IntegerField(verbose_name='编号', help_text='编号决定图片播放的顺序，图片不要多于5张')
    title = models.CharField(verbose_name='标题', max_length=20, blank=True, null=True, help_text='标题可以为空')
    content = models.CharField(verbose_name='描述', max_length=80)
    img_url = models.CharField(verbose_name='图片地址', max_length=200)
    url = models.CharField(verbose_name='跳转链接', max_length=200, default='#', help_text='图片跳转的超链接，默认#表示不跳转')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name
        # 编号越小越靠前，添加的时间约晚约靠前
        ordering = ['number', '-id']

    def __str__(self):
        return self.content[:25]
