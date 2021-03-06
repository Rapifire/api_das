# -*- coding: utf-8 -*-
# import matplotlib.pyplot as plt
import cv2
import os
import sys
import numpy as np
import urllib
import requests
from StringIO import StringIO
from detector.ImagesUtil import ImageUtil

#loading caffe 
caffe_root = os.path.join('/home/sabings/glog/caffe/')	
sys.path.insert(0,os.path.join('/home/sabings/glog/caffe/python'))
	
import caffe

class ImageClassifier(ImageUtil):


	@classmethod
	def image_from_url(cls,url):

		caffe.set_mode_cpu()

		model_def = os.path.join(caffe_root, 'models', 'bvlc_reference_caffenet','deploy.prototxt')
		model_weights = os.path.join(caffe_root, 'models','bvlc_reference_caffenet','bvlc_reference_caffenet.caffemodel')

		net = caffe.Net(model_def,model_weights,caffe.TEST)     

		# load the mean ImageNet image (as distributed with Caffe) for subtraction
		mu = np.load(os.path.join(caffe_root, 'python','caffe','imagenet','ilsvrc_2012_mean.npy'))
		mu = mu.mean(1).mean(1)  # average over pixels to obtain the mean (BGR) pixel values

		transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})

		transformer.set_transpose('data', (2,0,1))  # move image channels to outermost dimension
		transformer.set_mean('data', mu)            # subtract the dataset-mean value in each channel
		transformer.set_raw_scale('data', 255)      # rescale from [0, 1] to [0, 255]
		transformer.set_channel_swap('data', (2,1,0))  # swap channels from RGB to BGR

		# set the size of the input (we can skip this if we're happy
		#  with the default; we can also change it later, e.g., for different batch sizes)
		net.blobs['data'].reshape(50,        # batch size
		                          3,         # 3-channel (BGR) images
		                          227, 227)  # image size is 227x227

		resp = requests.get(url)

		image_caffe = caffe.io.load_image(StringIO(resp.content))

		transformed_image = transformer.preprocess('data', image_caffe)

		# copy the image data into the memory allocated for the net
		net.blobs['data'].data[...] = transformed_image
		### perform classification
		output = net.forward()

		output_prob = output['prob'][0]  # the output probability vector for the first image in the batch
			# load ImageNet labels
		labels_file = os.path.join(caffe_root, 'data','ilsvrc12','synset_words.txt')
		#if not os.path.exists(labels_file):
		    #!~/caffe/data/ilsvrc12/get_ilsvrc_aux.sh

		labels = np.loadtxt(labels_file, str, delimiter='\t')

		probability_response = zip(labels[output_prob.argsort()[::-1][:5]])

		top_inds = output_prob.argsort()[::-1][:5]

		lista = zip(output_prob[top_inds], labels[top_inds])
	
		output.pop('prob')
		for probability,values in lista:
			temp = values.split(' ')
			output[temp[0]] = list()
			output[temp[0]].append(' '.join(temp[1:]))
			output[temp[0]].append(str(probability))

		return output

	@classmethod
	def image_from_file(cls,file):
		pass

