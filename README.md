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

Install the dependencies above, clone this repo and edit the observatory setup section at the beginning of the alcor.py script, 

```python
# edit here
image_dir="/home/ops/allskycam"
# observatory set up
olat=-24.-(37./60.)-(38./3600.)
olon=-70.-(24./60.)-(15./3600.)
elev=2418.
obsloc=EarthLocation(lat=olat*u.deg,lon=olon*u.deg,height=elev*u.m)
```

adjust the configuration parameters in the .conf files and voila, you are ready to take some images

## API Reference

N/A

## Tests

_Update - add example images and output shots from terminal_

## Contributors

James McCormac

## License

_Update_