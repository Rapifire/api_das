from django.conf.urls import url
from views import FaceDetect
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    url(r'^url/',FaceDetect.as_view(),name='face_detect'),
]