"""
Script to make daily movies of the all sky images
from NGTS using ffmpeg
"""
import os
import glob as g
import multiprocessing as mp

# pylint: disable=invalid-name

if __name__ == "__main__":
    n_cpu = mp.cpu_count()
    data_dir = '/ngts/staging/archive/allskycam'
    movie_dir = '{}/movies'.format(data_dir)
    os.chdir(data_dir)
    templist = sorted(g.glob('2016*'))
    for i in templist:
        print('\nMaking all-sky movie for {}\n'.format(i))
        output_file = "{}/{}.mp4".format(movie_dir, i)
        if not os.path.exists(output_file):
            os.chdir(i)
            # get the file extension
            l1 = g.glob('*.jpeg')
            l2 = g.glob('*.jpg')
            if len(l1) > len(l2):
                cmd = "ffmpeg -y -i '%*.jpeg' -r 30 -q:v 2 -threads {} {}".format(n_cpu, output_file)
            else:
                cmd = "ffmpeg -y -i '%*.jpg' -r 30 -q:v 2 -threads {} {}".format(n_cpu, output_file)
            os.system(cmd)
            os.chdir('../')
