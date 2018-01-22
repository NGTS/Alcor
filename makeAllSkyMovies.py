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
        cmd = "ffmpeg -i '%*.jpg' -r 30 -q:v 2 {}/{}.mp4".format(movie_dir, i)
        os.system(cmd)
        os.chdir('../')
