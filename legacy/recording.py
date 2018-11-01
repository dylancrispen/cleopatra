from threading import Thread 
import imutils
import cv2
import numpy as np

class VideoRec:	
	def __init__(self, video=None, frame=None):
		print(video)
		self.frame = frame
		self.video = video
		self.stopped = False

	def start(self):
		Thread(target=self.record, args=()).start()
		return self
		
	def record(self):
		fourcc = cv2.VideoWriter_fourcc(*'XVID')
		rec = cv2.VideoWriter(self.video, fourcc, 20, (640,480))
		try:
			while self.stopped==False:
				rec.write(self.frame)
		except KeyboardInterrupt:
			pass
		rec.release()
		self.stop()

	def stop(self):
		print("Frames released")
		self.stopped = True
		
