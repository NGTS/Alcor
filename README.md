## Synopsis

Control script for Alcor OMEA all-sky camera. This code wraps up _fswebcam_ and embraces many of its nice features for adjustment and image archiving.<br/>

alcor.py runs like a daemon, adjusting the camera settings depending on the Sun's current altitude. This enables relatively seemless day and night time imaging of the sky above NGTS. <br/>

The configuration files should be adjusted depending on the camera and installtion location etc. See Installation section below.

## Code Example

```
usage: alcor.py [-h] [--debug] [--v]

Alcor all-sky camera control script. Camera control is done using fswebcam.
Edit camera's day/night settings using the fswebcam .conf files in the Git
repo.

optional arguments:
  -h, --help  show this help message and exit
  --sunalt SUNALT Sun altitude limit for day/night transition
  --debug         Run in deugging mode
  --v             Increased verbosity
```
To start the script simply run:

```
python alcor.py [--sunalt SUNALT, --v]
```
This will run an infinite loop taking images and adjusting the camera based on the settings in the configuration files and the Sun altitude limit for the day/night transition. If no --sunalt is given alcor.py defaults to -5 degrees. 

## Motivation

We need real time images of the sky above NGTS. The best solution is an all-sky camera. 

## Installation

Depends on the following:<br/> 
_libgd2-noxpm-dev_ <br/>
[fswebcam](https://github.com/jmccormac01/fswebcam) <br/>
_ttf-dejavu_ (optional, different fonts can be used, see .conf files)<br/>
_astropy_ <br>

Install the dependencies above, clone this repo and edit the observatory setup section at the beginning of the alcor.py script: 

```python
# edit here
image_dir="/home/ops/allskycam"
# observatory set up
olat=-24.-(37./60.)-(38./3600.)
olon=-70.-(24./60.)-(15./3600.)
elev=2418.
obsloc=EarthLocation(lat=olat*u.deg,lon=olon*u.deg,height=elev*u.m)
```

Adjust the configuration parameters in the day and night .conf files, e.g.: Additional .conf files maybe included (e.g. for twilight). This would require a slight modification of alcor.py to add an additional check on the Sun altitude. I will investigate this further when our OMEA camera goes on sky in February.

```
# Paranal_day.conf - James McCormac 20160110

# Be very quiet...
quiet

# Or be very loud?
#verbose

# The image source - 
device     "/dev/video0"
input      0
palette    GREY
resolution 1600x1200
loop       30
skip       5
set        "exposure (absolute)"="1000" 
timeout    5
frames     100

# design the banner
top-banner
font          "/usr/share/fonts/truetype/ttf-dejavu/DejaVuSansMono.ttf"
title         "NGTS All Sky Camera"
subtitle      "PAO subtitle"
info          "PAO info"
banner-colour #FF000000
line-colour   #FF000000
text-colour   #FF000000
gmt

# Save it to a shared folder.
save "/home/ops/allskycam/allsky.jpeg"

# Save another copy for the archive. The archive contains a folder for each
# day of images. First we create the folder if it doesn't already exist.
exec "mkdir /home/ops/allskycam/%Y%m%d 2> /dev/null"

# Then save the image into it.
save "/home/ops/allskycam/%Y%m%d/allsky-%Y%m%d-%H%M%S.jpeg"
```
Additional .conf files maybe included (e.g. for twilight). This would require a slight modification of alcor.py to add an additional check on the Sun altitude. I will investigate this further when our OMEA camera goes on sky in February.

A full description of all the fswebcam parameters is given in the fswebcam help file. Voila, you are ready to take some images

## API Reference

N/A

## Tests

_Update - add example images and output shots from terminal_

## Contributors

James McCormac

## License

_Update_
