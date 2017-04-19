#!/usr/local/python/bin/python
import os
if __name__ == "__main__":
    os.chdir("/ngts/staging/archive/allskycam/")
    img = "allsky.jpg"
    new_img = "allsky_s.jpg"
    os.system('/usr/local/bin/convert %s -resize 50%% %s' % (img, new_img))
