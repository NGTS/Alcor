#!/usr/local/python/bin/python
# Script to observe with the all-sky camera
# 
# to do:	
#	add basic camera control	
#	add Pyro support
#	add archiving
#	work out when to jump from day to night mode using el_sun
#	run the camera in one thread 
#	run image analysis in another
# 	
# The main settings are set in the config file
# given below. Check here for device and image
# settings
#
import os, time
import signal, subprocess
from astropy.time import Time
from astropy.coordinates import EarthLocation, AltAz
from astropy.coordinates import get_sun
from datetime import datetime as dt

live_image="/home/ops/webcam/allsky.jpeg"
sun_alt_limit = -5
die=False

# observatory set up
olat=-24.-(37./60.)-(38./3600.)
olon=-70.-(24./60.)-(15./3600.)
elev=2418.
paranal=EarthLocation(lat=olat*u.deg,lon=olon*u.deg,height=elev*u.m)

# work out if it is day or night time
# based on the current Sun altitude
def dayOrNight():
	time=Time(dt.utcnow(),scale='utc')
	altazframe = AltAz(obstime=time, location=paranal)
	sunaltaz = get_sun(time).transform_to(altazframe)
	sunalt=sunaltaz.alt.deg[0]
	if sunalt <= sun_alt_limit:
		return 'night'
	else:
		return 'day'

# set up Ctrl+C handling
def signal_handler(signal,frame):
	global die
	print "Ctrl+C caught, exiting..."
	die=True
signal.signal(signal.SIGINT,signal_handler)

# main function
def main():
	global die
	don=dayOrNight()
	comm='fswebcam -c paranal_%s.conf' % (don)
	print "%s - %s" % (dt.utcnow(),comm)
	pro=subprocess.Popen(comm,subprocess.PIPE,shell=True,preexec_fn=os.setsid)
	while(1):
		don_new=dayOrNight()
		if don_new != don:
			# change settings
			print "%s - Changing the settings to %s" % (dt.utcnow(),don)
			os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
			time.sleep(30)
			comm='fswebcam -c paranal_%s.conf' % (don_new)
			print "%s - %s" % (dt.utcnow(),comm)
			pro=subprocess.Popen(comm,subprocess.PIPE,shell=True,preexec_fn=os.setsid)
			don=don_new
		time.sleep(10)
		if die == True:
			print "Killing fswebcam"
			os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
			print "Exiting..."
			break

if __name__ == '__main__':
	main()