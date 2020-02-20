"""
Script to make daily movies of the all sky images
from NGTS using ffmpeg
"""
import os
import argparse as ap
import glob as g
import multiprocessing as mp

# pylint: disable=invalid-name

def arg_parse():
    """
    parse command line arguments
    """
    p = ap.ArgumentParser()
    p.add_argument('datestr',
                   help='Date string, e.g. 2019-01-*')
    return p.parse_args()

if __name__ == "__main__":
    args = arg_parse()
    n_cpu = mp.cpu_count()
    data_dir = '/ngts/staging/archive/allskycam'
    movie_dir = '{}/movies'.format(data_dir)
    os.chdir(data_dir)
    templist = sorted(g.glob(args.datestr))
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
