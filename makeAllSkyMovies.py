"""
Script to make daily movies of the all sky images
from NGTS using ffmpeg
"""
import os
import glob as g

if __name__ == "__main__":
    data_dir = '/ngts/staging/archive/allskycam'
    movie_dir = '{}/movies'.format(data_dir)
    os.chdir(data_dir)
    templist = g.glob('2016-01-*')
    for i in templist:
        os.chdir(i)
        # get the file extension
        l1 = g.glob('*.jpeg')
        l2 = g.glob('*.jpg')
        if len(l1) > len(l2):
            cmd = "ffmpeg -y -i '%*.jpeg' -r 30 -q:v 2 {}/{}.mp4".format(movie_dir, i)
        else:
            cmd = "ffmpeg -y -i '%*.jpg' -r 30 -q:v 2 {}/{}.mp4".format(movie_dir, i)
        os.system(cmd)
        os.chdir('../')
