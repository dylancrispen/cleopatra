from threading import Thread 
import numpy as np
import picamera
import picamera.array
import socket
import time

class VideoRec:	
	def __init__(self, video=None, width = 640, height = 480, framerate=32, 
		useStreamer=False, server='0.0.0.0', scale = 1):
	# initialize VideoRec class with different parameters
	# video: Name of the video file being recorded
	# self.camera: the picamera object used for recording
	# resolution and framerate: depended on user setting
	# self.frame: a frame extracted for reading from outside
	# self.stopped: stop the program when it's done	
	# useStreamer: whether or not to stream the service

		self.camera = picamera.PiCamera()
		self.camera.resolution = (width, height)
		self.camera.framerate = framerate
		self.video = video
		self.framerate = framerate
		self.frame = np.empty((height, width, 3), dtype=np.uint8)
		
		self.useStreamer = useStreamer
		if useStreamer==True:
			self.server = server
			self.streamresolution = (int(width/scale), int(height/scale))
		self.stopped = False
		self.streaming = False
		self.recording = False

	def start(self):
	# open a thread and run self.vision() for frames
		Thread(target=self.vision, args=()).start()
		return self
	
	def startStream(self):
	# start streaming and setup connection sockets at self.server
		self.client_socket = socket.socket()
		self.client_socket.connect((self.server, 8000))
		self.connection = self.client_socket.makefile('wb')
		self.camera.start_recording(self.connection, format='h264',
				splitter_port=2, resize=self.streamresolution)
		self.streaming = True
		return self

	def stopStream(self):
	# stop streaming and close all connection sockets
		self.camera.stop_recording(splitter_port=2)
		self.connection.close()
		self.client_socket.close()
		self.streaming = False
		return self
	
	def startRecord(self):
	# start recording video and store at self.video
		self.camera.start_recording(self.video)
		self.started = True
		self.recording = True
		return self

	def stopRecord(self):
	# stop the recording
		f = "Video saved at: " + self.video
		print(f)
		self.camera.stop_recording()
		self.recording = False
		return self

	def vision(self):
	# grab a frame every frame length (1/fps)
		if (self.streaming == False) and (self.recording == False):
			print("Please start recording or streaming first")
		framelength = 1/self.framerate
		read = 0
		start = time.time()
		while self.stopped==False:
			current = time.time()
			if (read==0):
				with picamera.array.PiRGBArray(self.camera) as stream:
					self.camera.capture(stream, format = 'bgr', 
						use_video_port = True)
					self.frame = stream.array
					read = 1
			if (current-start)>framelength:
				start = current
				read = 0
	
	def read(self):
	# return the current saved frame
		return self.frame	

	def stop(self):
	# stop everything
		if (self.recording == True):
			self.stopRecord()
		if (self.streaming == True):
			self.stopStream()
		self.stopped = True
		
