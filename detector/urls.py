# -*- coding: utf-8 -*-
from django.conf.urls import url
from views import FaceDetect,FirstPage,GetCategories
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
	url(r'^$',FirstPage.as_view(),name='first_page'),
    url(r'url/',FaceDetect.as_view(),name='face_detect'),
    url(r'categories/',GetCategories.as_view(),name='get_categories'),
]