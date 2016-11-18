from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from ImageCategory import ImageClassifier
from models import Image, Classification
import numpy as np
import urllib
import json
import cv2
import os

# Create your views here.

class FaceDetect(View):

	http_methods_names = [u'post']

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(FaceDetect, self).dispatch(request, *args, **kwargs)

	def post(self,request):

		output = dict()

		url = request.POST["url"]

		faces = list()

		response = urllib.urlopen(url)
		data = response.read()
		
		image = np.asarray(bytearray(data),dtype="uint8")
		image = cv2.imdecode(image,cv2.IMREAD_COLOR)
		image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
		detector = cv2.CascadeClassifier('/root/Opencv/data/haarcascades/haarcascade_frontalface_default.xml')


		rects = detector.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5,
			minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
		
		rects = [(int(x), int(y), int(x + w), int(y + h)) for (x, y, w, h) in rects]

		
		output['num_faces']=len(rects)
		output['faces'] = rects
		output['sucess'] = True
		output['probability_response'] = ImageClassifier.image_from_url(url)



		for key,value in output['probability_response'].items():
			if(len(Classification.objects.filter(number_id=key)) == 0):
				
				classification = Classification()
				
				classification.number_id = key
				classification.classification = value

				classification.save()

				print key,value
			else:
				pass


		if( len(Image.objects.filter(url=url)) == 0 ):

			image = Image()
			image.url = request.POST['url']
			image.save()

			for key in output['probability_response'].keys():
				
				classification = Classification.objects.get(number_id=key)
				
				image.classification_type.add(classification)


			image.save()


		faces.append(output)


		

		return JsonResponse(output)
