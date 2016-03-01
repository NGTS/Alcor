# script to push the alcor images to staging 
# and the monitor page image directory every 5 mins
import os
import glob as g
os.chdir('/cygdrive/c/Users/ops/Documents/skywatch/')
current_dir=sorted(g.glob('*-*-*'))[-1]
print('Moving to %s' % current_dir)
os.chdir(current_dir)
t=g.glob('*.jpg')
print("Archiving image %s" % (t[-1]))
os.system('scp %s ops@10.2.5.32:/ngts/staging/archive/allskycam/' % (t[-1]))
print("Passing image %s to monitor page" % (t[-1]))
os.system('scp %s ops@10.2.5.32:/home/ops/ngts/prism/monitor/img/allsky.jpg' % (t[-1]))