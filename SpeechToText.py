import speech_recognition as sr
import sys
import json
import os
import cv2
import string
import numpy as np                # linear algebra
import pandas as pd               # data processing
import tensorflow as tf
import keras
import matplotlib.pyplot as plt
import skimage
import sklearn
import nltk
import string
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer


def SpeechToText_Run():

	score = 0

	TestingSentence = "Today is a beautiful day and I am amazing"

	r = sr.Recognizer()

	print("Starting the microphone for SpeechToText....")

	with sr.Microphone() as source:
		print("Please repeat this line once: Today is a beautiful day and I am amazing")                 
		audio_data = r.record(source, duration=10)     # read the audio data from the default microphone
		# convert speech to text
		try:
			text = r.recognize_google(audio_data, language = 'en-IN')
			response = json.dumps(text, ensure_ascii=False).encode('utf8')
			print(response)
		except:
			text = "Try again"
			print("Oops!", sys.exc_info(), "occured.")
	 
	print("Running the cosine similarity....")

	count_vect = CountVectorizer()
	 
	DocumentList = [TestingSentence,text]
	 
	X_train_counts = count_vect.fit_transform(DocumentList)

	vectorizer = TfidfVectorizer()
	trsfm  =  vectorizer.fit_transform(DocumentList)

	result = cosine_similarity(trsfm[0], trsfm[1])[0]

	if result == 0:
		score = 0
	elif result >= 0.5:
		score = 0
	else:
		score = 1    # only triggers if the similarity is more than 0 and less than 0.5

	return score