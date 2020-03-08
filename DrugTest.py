# Real-Time Intoxication Identification using Computer Vision

"""
Basics: 

Eye detection algorithm:
1) Exract the eye regions from the facial landmark detection algorithm
2) Calculate the eye aspect ratio to determine if the eyes are closed:
	=> If the eye is closed, the eye aspect ratio will remain approximately constant,
	=> If the eye is closed, the eye aspect ratio will drastically decrease
3) If the eye aspect ratio indicates that the eyes have been closed for a sufficiently long enough amount of time we will activate DrunkMode

Jawline detection algorithm:


"""

from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2

def DrugTest_Run():

	Score = 0

	def eye_aspect_ratio(eye):
		# compute the euclidean distances between the two sets of vertical eye landmarks (x, y)-coordinates
		A = dist.euclidean(eye[1], eye[5])
		B = dist.euclidean(eye[2], eye[4])

		# compute the euclidean distance between the horizontal eye landmark (x, y)-coordinates
		C = dist.euclidean(eye[0], eye[3])

		ear = (A + B) / (2.0 * C)                  # compute the eye aspect ratio

		return ear                                 # return the eye aspect ratio


	def jawline_speed_detection(jawline):
		return "testing"

	 
	# construct the argument parse and parse the arguments
	app = argparse.ArgumentParser()
	app.add_argument("-w", "--webcam", type=int, default=0)
	args = vars(app.parse_args())
	 
	# define two constants, one for the eye aspect ratio to indicate
	# blink and then a second constant for the number of consecutive
	# frames the eye must be below the threshold for to trigger the alarm
	EYE_AR_THRESH = 0.3
	EYE_AR_CONSEC_FRAMES = 60

	# initialize the frame counter as well as a boolean used to indicate if the DrunkMode is off.
	COUNTER = 0
	DrunkMode = False

	# initialize dlib's face detector (HOG-based) and then create the facial landmark predictor
	path = "shape_predictor_68_face_landmarks.dat"
	print("loading facial landmark predictor...")
	detector = dlib.get_frontal_face_detector()
	predictor = dlib.shape_predictor(path)

	# grab the indexes of the facial landmarks for the left and
	# right eye, respectively
	(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
	(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
	jawlineIndex   = face_utils.FACIAL_LANDMARKS_IDXS["jaw"]

	# start the video stream thread
	print("starting video stream thread...")
	vs = VideoStream(src=args["webcam"]).start()
	time.sleep(1.0)


	# Record the frame for 1 mins

	FramerCounter_Treshold = 2400
	FramerCounter_Initial = 0

	# loop over frames from the video stream
	while DrunkMode != True and FramerCounter_Initial < FramerCounter_Treshold:   #  Change the True for continues loop
		FramerCounter_Initial += 1  						#  Increment the counter for every frame

		# grab the frame from the threaded video file stream, resize it, and convert it to grayscale
		frame = vs.read()
		frame = imutils.resize(frame, width=450)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		# detect faces in the grayscale frame
		GrayScale_frames = detector(gray, 0)

		# loop over the face detections
		for GrayScale_frame in GrayScale_frames:
			# determine the facial landmarks for the face region, then
			# convert the facial landmark (x, y)-coordinates to a NumPy array
			shape = predictor(gray, GrayScale_frame)
			shape = face_utils.shape_to_np(shape)

			# extract the left and right eye coordinates, then use the
			# coordinates to compute the eye aspect ratio for both eyes
			leftEye = shape[lStart:lEnd]
			rightEye = shape[rStart:rEnd]
			leftEAR = eye_aspect_ratio(leftEye)
			rightEAR = eye_aspect_ratio(rightEye)

			# average the eye aspect ratio together for both eyes
			ear = (leftEAR + rightEAR) / 2.0

			# compute the convex hull for the left and right eye, then
			# visualize each of the eyes
			leftEyeHull = cv2.convexHull(leftEye)
			rightEyeHull = cv2.convexHull(rightEye)

			cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
			cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

			pts = shape[0:17]           # geometric coordinates for the Jaw line

			# manually plotting the jawline coordinates

			for l in range(1, len(pts)):
				ptA = tuple(pts[l - 1])
				ptB = tuple(pts[l])
				cv2.line(frame, ptA, ptB, (79, 76, 240), 2)

			# check to see if the eye aspect ratio is below the blink
			# threshold, and if so, increment the blink frame counter
			if ear < EYE_AR_THRESH:
				COUNTER += 1

				# if the eyes were closed for a sufficient number of then trigger the DrunkMode
				if COUNTER >= EYE_AR_CONSEC_FRAMES:
					# if the alarm is not on, turn it on
					if DrunkMode != True:
						DrunkMode = True
						score = 1

					# draw an alarm on the frame
					cv2.putText(frame, "[Eye] Drunk Detected!", (10, 30),
						cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

			# otherwise, the eye aspect ratio is not below the blink
			# threshold, so reset the counter and alarm
			else:
				COUNTER = 0
				DrunkMode = False

			# draw the computed eye aspect ratio on the frame to help
			# with debugging and setting the correct eye aspect ratio
			# thresholds and frame counters
			cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
				cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
	 
		# show the frame
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
	 
		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break

	# do a bit of cleanup
	cv2.destroyAllWindows()
	vs.stop()

	return score