#!/usr/bin/python
"""
script to push the alcor images to staging
and copy the monitor page static image every
X minutes on a cronjob
"""
import os
import glob as g
import Pyro4

# pylint: disable = invalid-name

top_dir = '/cygdrive/c/Users/ops/Documents'
skywatch_dir = '{}/skywatch'.format(top_dir)
exclude_file = '/home/ops/Alcor/syncAlcorExcludeFiles.txt'

def getLastImage():
    """
    Return the name of most recent synced image
    """
    return open('{}/lastimg.txt'.format(skywatch_dir)).readline().rstrip()

def setLastImage(image_id):
    """
    Set the most recent synced image
    """
    f = open('{}/lastimg.txt'.format(skywatch_dir), 'w')
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
        os.system("rsync -avzHP --stats --exclude-from {} {}/skywatch/ ops@10.2.5.32:/ngts/staging/archive/allskycam".format(exclude_file, top_dir))
        #os.system('scp {} ops@10.2.5.32:/ngts/staging/archive/allskycam/'.format(t[-1]))
        print("Passing image {} to monitor page as static allsky.jpg".format(t[-1]))
        os.system('scp {} ops@10.2.5.32:/ngts/staging/archive/allskycam/allsky.jpg'.format(t[-1]))
        print('Updating last image to {}'.format(t[-1]))
        setLastImage(t[-1])
        print("Done!")
    else:
        print('{} has not updated, skipping...'.format(t[-1]))
        print("Skipping check in with centralHub...")

