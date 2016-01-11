#!/usr/local/python/bin/python
#
# Description:
# Script to observe with the Alcor all-sky camera
# This script applies one exptime during the day
# and another for night time. 
#
# The main day/night settings are set in the 
# config files in the Git repo. Check there for 
# device and image settings.
#
# To do:	
#	add Pyro support
#	add long term archiving
#	run some image analysis in another subprocess?
#	add logging
#

import os, time
import signal, subprocess
from astropy.time import Time
from astropy.coordinates import EarthLocation, AltAz
from astropy.coordinates import get_sun
from datetime import datetime as dt
import astropy.units as u
import argparse as ap
import warnings
warnings.filterwarnings('ignore')

# edit here
live_image="/home/ops/webcam/allsky.jpeg"
sun_alt_limit = -5

# observatory set up
olat=-24.-(37./60.)-(38./3600.)
olon=-70.-(24./60.)-(15./3600.)
elev=2418.
paranal=EarthLocation(lat=olat*u.deg,lon=olon*u.deg,height=elev*u.m)
die=False

# parse command line
def argParse():
	description="""
		Alcor all-sky camera control script.\n 
		--------------------------------------\n
		Camera control is done using fswebcam. Edit camera\'s day/night 
		settings using the fswebcam .conf files in the Git repo. 
		"""
	parser=ap.ArgumentParser(description=description)
	parser.add_argument("--debug",help="run in deugging mode",action="store_true")
	parser.add_argument("--v",help="increased verbosity",action="store_true")
	return parser.parse_args()

args=argParse()

# work out if it is day or night time
# based on the current Sun altitude
def dayOrNight():
	tnow=Time(dt.utcnow(),scale='utc')
	altazframe = AltAz(obstime=tnow, location=paranal)
	sunaltaz = get_sun(tnow).transform_to(altazframe)
	sunalt=sunaltaz.alt.deg
	if sunalt <= sun_alt_limit:
		result='night'
	else:
		result='day'
	if args.v:
		print "%s - Sun altitude: %.2f - %s" % (dt.utcnow(),sunalt,result)
	return result

# set up Ctrl+C handling
def signalHandler(signal,frame):
	global die
	print "Ctrl+C caught, exiting..."
	die=True
signal.signal(signal.SIGINT,signalHandler)

# main function
def main():
	global die
	don=dayOrNight()
	comm='fswebcam -c paranal_%s.conf' % (don)
	if args.v:
		print "%s - %s" % (dt.utcnow(),comm)
	if not args.debug:
		pro=subprocess.Popen(comm,subprocess.PIPE,shell=True,preexec_fn=os.setsid)
	while(1):
		don_new=dayOrNight()
		# change from day to night, and vice versa
		if don_new != don:
			if args.v:
				print "%s - Changing the settings to %s" % (dt.utcnow(),don)
			if not args.debug:
				os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
			time.sleep(30)
			comm='fswebcam -c paranal_%s.conf' % (don_new)
			if args.v:
				print "%s - %s" % (dt.utcnow(),comm)
			if not args.debug:
				pro=subprocess.Popen(comm,subprocess.PIPE,shell=True,preexec_fn=os.setsid)
			don=don_new
		# wait for 5 mins between checks for change in day/night
		time.sleep(300)
		# if ctrl+c, die correctly
		if die == True:
			print "Killing fswebcam"
			if not args.debug:
				os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
			print "Exiting..."
			break

if __name__ == '__main__':
	main()