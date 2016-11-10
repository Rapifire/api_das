from django.shortcuts import render
from django.views import Views
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import urllib
import json
import cv2
# Create your views here.


class FaceDetect(View):

	@csrf_exempt
	def post(self,request):

		output = dict()

		url = request.POST.get("url")

		response = urllib.urlopen(url)
		data = response.read()
		image = np.asarray(bytearray(data),dtype="uint8")
		image = cv2.imdecode(image,cv2.IMREAD_COLOR)





		return JsonResponse(output)