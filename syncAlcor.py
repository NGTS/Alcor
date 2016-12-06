#!/usr/bin/python
# script to push the alcor images to staging
# and the monitor page image directory every X minutes
# on a cronjob
import os, Pyro4
import glob as g

top_dir = '/cygdrive/c/Users/ops/Documents'
skywatch_dir = '{}/skywatch'.format(top_dir)
exclude_file = '/home/ops/Alcor/syncAlcorExcludeFiles.txt'

def getLastImage():
    return open('{}/lastimg.txt'.format(skywatch_dir)).readline().rstrip()

def setLastImage(image_id):
    f = open('{}/lastimg.txt'.format(skywatch_dir),'w')
    f.write("{}\n".format(image_id))
    f.close()

if __name__ == "__main__":
    os.chdir(skywatch_dir)
    lastimg = getLastImage()
    current_dir = sorted(g.glob('*-*-*'))[-1]
    print('Moving to %s' % current_dir)
    os.chdir(current_dir)
    t = g.glob('*.jpg')
    if t[-1] != lastimg:
        print("Checking in with centralHub")
        hub = Pyro4.Proxy('PYRONAME:central.hub')
        hub.report_in('alcor')
        print("Rsycning data folder")
        os.system("rsync -avzHPn --stats --exclude-from {} {}/skywatch/ ops@10.2.5.32:/ngts/staging/archive/allskycam".format(exclude_file, top_dir))
        #os.system('scp {} ops@10.2.5.32:/ngts/staging/archive/allskycam/'.format(t[-1]))
        print("Passing image {} to monitor page".format(t[-1]))
        os.system('scp {} ops@10.2.5.32:/home/ops/ngts/prism/monitor/img/allsky.jpg'.format(t[-1]))
        print('Updating last image to {}'.format(t[-1]))
        setLastImage(t[-1])
        print("Done!")
    else:
        print('{} has not updated, skipping...'.format(t[-1]))
        print("Skipping check in with centralHub...")

