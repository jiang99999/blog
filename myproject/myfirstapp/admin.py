from django.contrib import admin

# Register your models here.
from myfirstapp.models import Account,Article,Tag,Comment,Attention,CourseOrg

class AccountAdmin(admin.ModelAdmin):
    list_display = ('username','email','signature')
    search_fields = ('username','email')
    list_filter = ('email',)
    list_per_page = 10
    list_display_links = ('username','email','signature')


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','account','pub_date')
    search_fields = ('title','account','pub_date')
    list_filter = ('account','pub_date',)
    list_per_page = 10
    list_display_links = ('title','account','pub_date')

    fieldsets = (
        ('文章内容',{
            'fields':['title','content','tags'],
            'classes':('wide', 'extrapretty'),
        }),(
            '发布相关',{
                #'classes': ('collapse',),
                'fields': ('account','pub_date','read_count')
        })
    )
    autocomplete_fields = ['account']
    readonly_fields = ('read_count',)


admin.site.register(Account,AccountAdmin)
admin.site.register(Article)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(CourseOrg)
admin.site.register(Attention)