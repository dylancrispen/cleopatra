# USAGE
# python tracking(version).py -parameters

# import the necessary packages
from __future__ import division
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import Adafruit_PCA9685
import pirecord as rec

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the video file")
ap.add_argument("-hl", "--headless", type=int, default=0,
	help="run program in headless mode")
ap.add_argument("-s", "--stream",
	help="server address for streaming")
ap.add_argument("-sq","--streamquality",
	help="scale down quality of stream", type=int, default=1)
args = vars(ap.parse_args())

# camera setting
width = 1280
height = 720
framerate = 25
# Size of screen
scale = 2
Xlength = int(640/scale)
Ylength = int(360/scale)

# size of acceptable window
Xbox = int(20/scale)
Ybox = int(16/scale)

# start bonnet
pwm = Adafruit_PCA9685.PCA9685()
servo_max = 409
servo_min = 205

pwm.set_pwm_freq(50)

delay = 0.001

pulseX = 306
pulseY = 306

Xcenter = Xlength/2
Ycenter = Ylength/2

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (29, 86, 30)
greenUpper = (65, 255, 255)

# initialize video recorder object
recorder = rec.VideoRec(video=args["video"], framerate = framerate,
	width = width, height = height, useStreamer = True,
		server = args["stream"], scale = args["streamquality"])
# allow the camera or video file to warm up
# keep looping
start = time.time()
frameCount = 0

# start recording or streaming
if args.get("video",False):
	recorder.startRecord()
	print("Recording")
if args.get("stream",False):
	recorder.startStream()
	print("Streaming")	

recorder.start()

try:
	while True:
		# grab the current frame
		frame = recorder.read()
		# if we are viewing a video and we did not grab a frame,
		# then we have reached the end of the video
		if frame is None:
			break
		frameCount = frameCount+1
		# resize the frame, blur it, and convert it to the HSV
		# color space
		frame = imutils.resize(frame, height=Ylength, width=Xlength)
		blurred = cv2.GaussianBlur(frame, (11, 11), 0)
		hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

		# construct a mask for the color "green", then perform
		# a series of dilations and erosions to remove any small
		# blobs left in the mask
		mask = cv2.inRange(hsv, greenLower, greenUpper)
		mask = cv2.erode(mask, None, iterations=1)
		mask = cv2.dilate(mask, None, iterations=1)

		# find contours in the mask and initialize the current
		# (x, y) center of the ball
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = cnts[0] if imutils.is_cv2() else cnts[1]
		center = None
		radius = 0

		# only proceed if at least one contour was found
		if len(cnts) > 0:
			# find the largest contour in the mask, then use
			# it to compute the minimum enclosing circle and
			# centroid
			c = max(cnts, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(c)
			M = cv2.moments(c)
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		
		# show the frame to our screen
		if (args["headless"]==0):
			cv2.rectangle(frame, (int(Xcenter+Xbox), int(Ycenter+Ybox)),
				(int(Xcenter-Xbox), int(Ycenter-Ybox)), (0, 0, 255), 2)
			# only proceed if the radius meets a minimum size
			if radius > 10:
				# draw the circle and centroid on the frame,
				# then update the list of tracked points
				cv2.circle(frame, (int(x), int(y)), int(radius),
					(0, 255, 255), 2)
				cv2.circle(frame, center, 5, (0, 0, 255), -1)
			cv2.imshow("Frame",frame)

		# move the servos in a scaled degree
		scaleX = 10
		scaleY = 5
		if (len(cnts)>0):
			if x < (Xcenter - Xbox):
				newPulse = pulseX + (Xcenter - Xbox -x)*scaleX/Xcenter
				if (newPulse<=servo_max):
					pulseX = newPulse
			if x > (Xcenter + Xbox):
				newPulse = pulseX - (x - Xcenter - Xbox)*scaleX/Xcenter
				if (newPulse>=servo_min):
					pulseX = newPulse
			if y < (Ycenter - Ybox):
				newPulse = pulseY - (Ycenter - Ybox - y)*scaleY/Ycenter
				if (newPulse>=servo_min):
					pulseY = newPulse
			if y > (Ycenter + Ybox):
				newPulse = pulseY + (y - Ycenter - Ybox)*scaleY/Ycenter
				if (newPulse<=servo_max):
					pulseY = newPulse
		pwm.set_pwm(0, 0, int(pulseX))
		pwm.set_pwm(1, 0, int(pulseY))
		time.sleep(delay)
		if (args["headless"]==0):
			key = cv2.waitKey(1) & 0xFF
			# if the 'q' key is pressed, stop the loop
			if key == ord("q"):
				break
except KeyboardInterrupt:
	pass			
pwm.set_pwm(1, 0, 0)
pwm.set_pwm(0, 0, 0)
# if we are not using a video file, stop the camera video stream
end = time.time()
recorder.stop()

fps = frameCount/(end - start)
print(fps)
# close all windows
cv2.destroyAllWindows()
