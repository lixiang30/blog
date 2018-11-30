# _*_ coding: utf-8 _*_
__author__ = 'Huu'
__date__ = '2018/8/7 20:03'

import xadmin
from .models import Article,Tag,Comment,Subcomment,Category,Carousel

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True
from xadmin import views
xadmin.site.register(views.BaseAdminView,BaseSetting)

class GlobalSettings(object):
    site_title = "理想三旬"
    site_footer = "我的个人博客"
    # menu_style = "accordion"
xadmin.site.register(views.CommAdminView,GlobalSettings)

class ArticleAdmin(object):
    list_display=('title',)

class TagAdmin(object):
    list_display=('name','chinese_name')

class CommentAdmin(object):
    list_display=('content','article','author')

class SubcommentAdmin(object):
    list_display=('content','article','author','reply_to')

class CategoryAdmin(object):
    list_display=('name',)

xadmin.site.register(Article,ArticleAdmin)
xadmin.site.register(Tag,TagAdmin)
xadmin.site.register(Comment,CommentAdmin)
xadmin.site.register(Subcomment,SubcommentAdmin)
xadmin.site.register(Category,CategoryAdmin)