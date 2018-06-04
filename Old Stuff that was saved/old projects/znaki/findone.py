import os
import re
from os import listdir
from os.path import isfile, join
import numpy as np
import cv2

#cap = cv2.VideoCapture(0)

mypath='d:/znaki'
onlyfiles = [ f for f in listdir(mypath) if (isfile(join(mypath,f))and(re.findall(r'\d',f))) ]
images = np.empty(len(onlyfiles), dtype=object)
for n in range(0, len(onlyfiles)):
  images[n] = cv2.cvtColor(cv2.resize(cv2.imread( join(mypath,onlyfiles[n]) ),(32,32)), cv2.COLOR_BGR2GRAY)

frame = cv2.resize(cv2.imread('d:/znaki/img.jpg'),(640,360))  
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# take first frame of the video
roiret, roi = cv2.threshold(images[4],128,255,0)


thresh = cv2.Canny(frame,100,200)

res = thresh.copy()

im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

if len(contours) > 0:

	areaArray = []
	cont = []
	roiArray = []
	roiDiffArray = []

	k = 0
	
	for n, c in enumerate(contours):
	  if (cv2.contourArea(c) > 400) and (cv2.contourArea(c) < 640*480/4):
		areaArray.append(0)
		cont.append(c)
		x, y, w, h = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x+w, y+h), (255,255,255), 2)
		roi2 = cv2.resize(frame[y:y+h,x:x+w],(32,32))
		roi2ret,roi2 = cv2.threshold(roi2,128,255,0)
		roiArray.append(roi2)
		diff = cv2.absdiff(roi, roi2)
		dret,dt = cv2.threshold(diff, 128, 255, 0)
		roiDiffArray.append(dt)
		dh, dw = dt.shape[:2]
		for x in range(0, dw):
		  for y in range(0, dh):
			if dt[y,x]==255:
			  areaArray[k]=areaArray[k]+1
		print areaArray[k]
		k = k+1
		  
	sorteddata = sorted(zip(areaArray, contours), key=lambda x: x[0], reverse=False)
	c = sorteddata[0][1]
	x, y, w, h = cv2.boundingRect(c)
	cv2.rectangle(frame, (x, y), (x+w, y+h), 127, 2)


while(1):

    #ret2,thresh = cv2.threshold(frame,128,255,0)
    
	
	for n, c in enumerate(roiArray):
		cv2.imshow(str(n),c)
	
	
	cv2.imshow('camera',frame)
	cv2.imshow('result',res)
	#cv2.imshow('znak',images[4])

	k = cv2.waitKey(60) & 0xff
	if k == 27:
	  break

cv2.destroyAllWindows()
#cap.release()
