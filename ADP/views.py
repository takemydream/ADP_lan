from django.shortcuts import render
from ADP import models
from django.http import HttpResponse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Create your views here.
def Stars_view_fuc(request):
    star_list = models.Star.objects.all()
    return render(request, 'ADP/Stars_view.html',{'star_list': star_list})

def search_fuc(request):
    request.encoding = "utf-8"
    if "thing_to_find" in request.POST:
        thing_to_find = request.POST['thing_to_find']
        if 'type_to_search' in request.POST:
            type_to_search = request.POST['type_to_search']
            if type_to_search == "Star_name":

                # 各级段需要的中转list
                star_foreign_id_list = []
                films_name_id_queryset_list = []
                films_name_queryset_list = []
                films_designation_queryset_list = []
                series_queryset_list = []

                # 输出数据list: data_to_show_formatting
                data_to_show_formatting = []

                # 获取star表的id
                star_foreign_id = models.Star.objects.filter(star_name_1=thing_to_find)
                if len(star_foreign_id) == 0:
                    data_to_show_formatting = [["Sorry, No find this Star"]]
                else:
                    for n in star_foreign_id:
                        star_foreign_id_list.append(n.id)

                #films
                # 获取films的id
                films_name_id_queryset = models.Table_film_with_star.objects.filter(star_name_1_id__in=star_foreign_id_list)
                if len(films_name_id_queryset) == 0:
                    data_to_show_formatting = [["Sorry, No find films of this star"]]
                else:
                    for fni in films_name_id_queryset:
                        films_name_id_queryset_list.append(fni.films_name_id)

                    # 根据films的id查找films的属性
                    films_argOf_name_and_designation_list = models.Film.objects.filter(id__in=films_name_id_queryset_list)

                    # films 的番号和描述,
                    for fanadl in films_argOf_name_and_designation_list:
                        films_name_queryset_list.append(fanadl.films_name)
                        films_designation_queryset_list.append(fanadl.designation)
                    # films 的series,
                    for films_num in films_name_id_queryset_list:
                        series_queryset = models.Table_film_with_series.objects.filter(films_name_id=films_num)
                        if len(series_queryset) == 0:
                            series_queryset_list.append("No_set_Series")
                        else:
                            for kdsa in series_queryset:
                                for askldjain in models.Series.objects.filter(id=kdsa.series_name_id):
                                    series_queryset_list.append(str(askldjain.series_name))

                # 添加到输出表: data_to_show_formatting
                len_films_name_queryset_list = len(films_name_queryset_list)
                for k in range(0, len_films_name_queryset_list):
                    data_to_show_formatting.append([thing_to_find,films_name_queryset_list[k], films_designation_queryset_list[k], series_queryset_list[k]])


                dict_of_datas = {'search_label': 'Star_name', 'data_to_show_formatting': data_to_show_formatting}
                return render(request, 'ADP/Search_view.html', dict_of_datas)

            elif type_to_search == "Film_num":

                star_id_sequeryset_list = []
                star_name_mix = ""
                series_mix = ""
                film_designation = ""
                series_id_queryset_list = []

                # 获取Films的id
                films_name_id_queryset = models.Film.objects.filter(films_name=thing_to_find)
                if len(films_name_id_queryset) != 0:
                    for fniq in films_name_id_queryset:
                        film_id = fniq.id
                        # 获取Films的designation
                        film_designation = fniq.designation

                    # star
                    star_id_sequeryset = models.Table_film_with_star.objects.filter(films_name_id=film_id)
                    if len(star_id_sequeryset) != 0:
                        for sis in star_id_sequeryset:
                            star_id_sequeryset_list.append(sis.star_name_1_id)

                        for snq_kasjdj in models.Star.objects.filter(id__in=star_id_sequeryset_list):
                            if star_name_mix != "":
                                star_name_mix = star_name_mix + "," + snq_kasjdj.star_name_1
                            else:
                                star_name_mix = snq_kasjdj.star_name_1
                    else:
                        star_name_mix = "UnKnow_Star"

                    # series
                    series_id_queryset = models.Table_film_with_series.objects.filter(films_name_id=film_id)
                    if len(series_id_queryset) != 0:
                        for siq_sdaqwec in series_id_queryset:
                            series_id_queryset_list.append(siq_sdaqwec.series_name_id)
                            series_queryset_list = models.Series.objects.filter(id__in=series_id_queryset_list)
                            if series_queryset_list != 0:
                                for sql_qjcbq in series_queryset_list:
                                    series_mix = series_mix + "," + sql_qjcbq.series_name_id
                    else:
                        series_mix = "Unset_Series"

                else:
                    thing_to_find = "sorry, No find Film:" + thing_to_find
                    star_name_mix = "No_find"
                    series_mix = "No_find"
                    film_designation = "No_find"

                data_to_show_formatting = [[thing_to_find, star_name_mix, film_designation, series_mix]]
                dict_of_datas = {'search_label': 'Film_num', 'data_to_show_formatting': data_to_show_formatting}
                return render(request, 'ADP/Search_view.html', dict_of_datas)


            elif type_to_search == "Series":
                # 获取series的id
                series_id_queryset = models.Series.objects.filter(series_name=thing_to_find)
                if series_id_queryset.count() != 0:
                    for siq in series_id_queryset:
                        series_id = siq.id

                    #films
                    # 获取films的id
                    films_name_id_queryset = models.Table_film_with_series.objects.filter(series_name_id=series_id)
                    if films_name_id_queryset.count() != 0:
                        films_name_id_queryset_list = []
                        for fniq in films_name_id_queryset:
                            films_name_id_queryset_list.append(fniq.films_name_id)
                        #获取films_number以及films的designation
                        films_number_queryset_list=[]
                        films_designation_queryset_list=[]
                        films_queryset = models.Film.objects.filter(id__in=films_name_id_queryset_list)
                        for fq in films_queryset:
                            films_number_queryset_list.append(fq.films_name)
                            films_designation_queryset_list.append(fq.designation)


                        #star
                        #根据films获取star信息
                        star_id_queryset_list = []
                        star_id_queryset = models.Table_film_with_star.objects.filter(films_name_id__in=films_name_id_queryset_list)
                        if star_id_queryset.count() != 0:
                            for siq in star_id_queryset:
                                star_id_queryset_list.append(siq.star_name_1_id)
                            star_name_queryset = models.Star.objects.filter(id__in=star_id_queryset_list)
                            star_name_queryset_list = []
                            for snql in star_name_queryset:
                                star_name_queryset_list.append(snql.star_name_1)

                            data_to_show_formatting = []
                            for num in range(0, len(films_name_id_queryset)):
                                data_to_show_formatting.append([thing_to_find, films_number_queryset_list[num], films_designation_queryset_list[num], star_name_queryset_list[num]])
                        else:
                            data_to_show_formatting = []
                            for num in range(0, len(films_name_id_queryset)):
                                data_to_show_formatting.append([thing_to_find, films_number_queryset_list[num], films_designation_queryset_list[num], 'No_info_about_Stars'])
                    else:
                        data_to_show_formatting=[[str(thing_to_find)+'   (matched_in_Database)', 'NO_films_matched']]
                else:
                    data_to_show_formatting=[['NO_Find_Series']]

                dict_of_datas = {'search_label': 'Series', 'data_to_show_formatting': data_to_show_formatting }
                return render(request, 'ADP/Search_view.html', dict_of_datas)


            elif type_to_search == "Film_Designation":
                pass# TODO


            else:
                message = "here was some problems in data_search part"
        else:
            message = "no 'type_to_search' argument posted?"
    else:
        message = '你提交了空表单'

    return HttpResponse(message)

def return_index(request):
    return render(request, "ADP/index.html")