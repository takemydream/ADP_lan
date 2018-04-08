from django.db import models

# Create your models here.
class Test(models.Model):
    name = models.CharField(max_length=20)

class Contact(models.Model):
    name  = models.CharField(max_length=200)
    age = models.IntegerField(default=0)
    email = models.EmailField()
    def __str__(self):
        return self.name

class Tag(models.Model):
    contact = models.ForeignKey(Contact)
    name = models.CharField(max_length=50)


    def __str__(self):
        return self.name

class Star(models.Model):
    '''
        name_1 女星名称 ;	string
        级别地位: normal/perfect;	string
        创建时间;
        更新时间;
        name_2;	string
        name_3; string
        name_4;	string
        英文名;	string
        年龄段;  string
    '''

    star_name_1 = models.CharField(max_length=200)
    star_name_2 = models.CharField(max_length=200, default="Unknow")
    star_name_3 = models.CharField(max_length=200, default="Unknow")
    star_name_4 = models.CharField(max_length=200, default="Unknow")
    star_English_Name = models.CharField(max_length=200, default="Unknow")
    age_group = models.CharField(max_length=200, default="NoSet")  # TODO age_group 表
    star_rank = models.CharField(max_length=100, default="NoSet")

    time_created = models.DateTimeField(auto_now_add=True)
    time_last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.star_name_1


class Series(models.Model):
    '''
        系列 表 ;
            名称; 	string
            primary_key
            系列传承大统;	string
            创建时间;
            更新时间;
    '''
    series_name = models.CharField(max_length=200)
    series_belong_to = models.CharField(max_length=200, default="UnKnow")
    time_created = models.DateTimeField(auto_now_add=True)
    time_last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.series_name



class Film(models.Model):
    '''
         影片名称;   string
         有码/无码; 	string
         番号; 	string
         创建时间;
         更新时间;
    '''
    films_name = models.CharField(max_length=200, unique=True)
    is_censored = models.NullBooleanField()
    designation = models.CharField(max_length=100, default='UnKnow')

    # 时间
    time_created = models.DateTimeField(auto_now_add=True)
    time_last_update = models.DateTimeField(auto_now=True)

    # ManyToMany 维系
    # 维系 Films 和 Stars 表
    stars_connect = models.ManyToManyField(Star, through='Table_film_with_star', through_fields=('films_name', "star_name_1" ))
    # 维系 Films 和 Series
    Series_connect = models.ManyToManyField(Series, through='Table_film_with_series', through_fields=('films_name', 'series_name' ))

    def __str__(self):
        return self.films_name

class Table_film_with_star(models.Model):
    films_name = models.ForeignKey(Film)
    star_name_1 = models.ForeignKey(Star)


class Table_film_with_series(models.Model):
    films_name = models.ForeignKey(Film)
    series_name = models.ForeignKey(Series)