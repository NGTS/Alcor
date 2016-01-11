#!/usr/local/python/bin/python
# Script to observe with the all-sky camera
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
flags='-i 0 --gmt --no-banner' # try using --read to see if that helps

def adjustExptime(av,texp):
	
	# don't bother if already good	
	if av < 200 and av > 150:
		adjust=False
		print "Current texp is fine, not adjusting"
		return adjust,texp

	texp_min=1
	texp_max=120000
	target_adu=175
	diff=target_adu/av
	
	# some sanity checks on low/high counts
	if av < 10:
		diff=1.5
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
	adjust=True
	return adjust,new_texp

def getImgAverage(image_id):
	img=Image.open(image_id)
	x,y=img.size
	# get a 400 pixel box in the middle for exposure control
	# left, upper, right, lower - from top left
	box=((x/2)-200,(y/2)-200,(x/2)+200,(y/2)+200)
	region=img.crop(box)
	data=np.asarray(region)
	av=np.average(data)
	print "Image average: %.2f" % (av)
	return av

def main():
	texp=100
	adjust=True
	while(1):
		if adjust:
			os.system('fswebcam -c %s -s "exposure (absolute)"="%d" %s' % (config,texp,flags))
		else:
			os.system('fswebcam -c %s %s' % (config,flags))
		time.sleep(5)
		av=getImgAverage(live_image)
		adjust,texp=adjustExptime(av,texp)
		

if __name__ == '__main__':
	main()