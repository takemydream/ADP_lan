# django 原装
from django.contrib import admin

# 导入各个模型
'''
from ADP.models import Contact
from ADP.models import Tag
from ADP.models import Test
'''
from ADP.models import Star
from ADP.models import Series
from ADP.models import Film
from ADP.models import Table_film_with_series
from ADP.models import Table_film_with_star


# Register your models here.

'''
class TagInLine(admin.TabularInline):
    model = Tag

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'email')
    inlines = [TagInLine]
    fieldsets = (
        ['Main',{
            'fields':('name','email'),
        }],
        ['Advance',{
            'classes': ('collapse',),  # CSS
            'fields': ('age',),
        }]
    );
    search_fields = ('name', 'email', 'age',)
'''


class Films_with_Stars_InLine(admin.TabularInline):
    model = Table_film_with_star
    def get_extra(self, request, obj=None, **kwargs):
        extra = 1
        return extra


class Films_with_Series_InLine(admin.TabularInline):
    model = Table_film_with_series
    def get_extra(self, request, obj=None, **kwargs):
        extra = 1
        return extra



class StarAdmin(admin.ModelAdmin):
    list_display = ('star_name_1', 'time_created', 'time_last_update')
    inlines = [Films_with_Stars_InLine]
    fieldsets = (
        ['Main', {
            'fields':('star_name_1', 'age_group', 'star_rank',),
        }],
        ['Advance',{
            'classes': ('collapse',),  # CSS
            'fields': ('star_name_2', 'star_name_3', 'star_name_4', 'star_English_Name', ),
        }]
    )
    search_fields = ['star_name_1', 'age_group', 'star_rank',]


class SeriesAdmin(admin.ModelAdmin):
    list_display = ('series_name', 'time_created', 'time_last_update')
    inlines = [Films_with_Series_InLine]
    fieldsets = (
        ['Main', {
            'fields': ('series_name', ),
        }],
        ['Advance', {
            'classes': ('collapse',),  # CSS
            'fields': ('series_belong_to',),
        }]
    )
    search_fields = ['series_name', 'series_belong_to', ]


class FilmsAdmin(admin.ModelAdmin):
    list_display = ('films_name', 'time_created', 'time_last_update')
    inlines = [Films_with_Series_InLine, Films_with_Stars_InLine]
    fieldsets = (
        ['Main', {
            'fields': ('films_name', 'is_censored', 'designation'),
        }],
    )



# 激活各个模块

# admin.site.register(Contact, ContactAdmin)
# admin.site.register(Test)

admin.site.register(Star, StarAdmin)
admin.site.register(Series, SeriesAdmin)
admin.site.register(Film, FilmsAdmin)
