#!/cygdrive/c/Users/ops/Miniconda2/python
# script to push the alcor images to staging 
# and the monitor page image directory every 5 mins
import os, Pyro4
import glob as g

skywatch_dir='/cygdrive/c/Users/ops/Documents/skywatch/'

def getLastImage():
	return open('%s/lastimg.txt' % (skywatch_dir)).readline().split('\n')[0]

def setLastImage(image_id):
	f=open('%s/lastimg.txt' % (skywatch_dir),'w')
	f.write(image_id)
	f.close()

os.chdir(skywatch_dir)
lastimg=getLastImage()
current_dir=sorted(g.glob('*-*-*'))[-1]
print('Moving to %s' % current_dir)
os.chdir(current_dir)
t=g.glob('*.jpg')
if t[-1] != lastimg:
	print("Archiving image %s" % (t[-1]))
	os.system('scp %s ops@10.2.5.32:/ngts/staging/archive/allskycam/' % (t[-1]))
	print("Passing image %s to monitor page" % (t[-1]))
	os.system('scp %s ops@10.2.5.32:/home/ops/ngts/prism/monitor/img/allsky.jpg' % (t[-1]))
	print("Checking in with centralHub")
	hub = Pyro4.Proxy('PYRONAME:central.hub')
	hub.report_in('alcor')
	print("Done!")
else:
	print('%s has not updated, skipping...' % (t[-1])) 
	print("Skipping check in with centralHub...")

