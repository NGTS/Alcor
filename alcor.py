#!/usr/local/python/bin/python
# code to generate the exposure time for 
# the alcor all sky camera
# 
# to do:	
#	add basic camera control	
#	add Pyro support
#	add archiving
# 	
# The main settings are set in the config file
# given below. Check here for device and image
# settings
#

import Image
import sys, os, time
import numpy as np

config="/home/ops/fswebcam/paranal.conf"
live_image="/home/ops/webcam/allsky-large.jpeg"
flags='-s "exposure"="aperture priority mode"'

def adjustExptime(av,texp):
	texp_min=1
	texp_max=120000
	target_adu=150
	diff=target_adu/av
	
	# some sanity checks on low/high counts
	if av < 10:
		diff=2
	elif av >240:
		diff=0.5

	# more sanity checks on runaway scaling
	# max of +/- 50% 
	if diff > 1.5:
		diff=1.5
	elif diff < 0.5:
		diff=0.5

	new_texp=int(texp*(diff))
	if new_texp>texp_max:
		new_texp=texp_max
	elif new_texp<texp_min:
		new_texp=texp_min
	print "New exptime: %d" % (new_texp)
	return new_texp

def getImgAverage(image_id):
	img=Image.open(image_id)
	x,y=img.size
	# get a 200 pixel box in the middle for exposure control
	# left, upper, right, lower - from top left
	box=((x/2)-100,(y/2)-100,(x/2)+100,(y/2)+100)
	region=img.crop(box)
	data=np.asarray(region)
	av=np.average(data)
	print "Image average: %.2f" % (av)
	return av

def main():
	while(1):
		os.system('fswebcam -c %s %s' % (config,flags))
		time.sleep(5)
		av=getImgAverage(live_image)
		#texp=adjustExptime(live_image,texp)
		

if __name__ == '__main__':
	main()