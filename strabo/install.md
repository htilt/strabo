## Purpose

This file is here to deal with all the problems of installing and setting up strabo. Place anything here that you had to change in your system in order to get strabo up and running


## Basic installation:

### Virtualenv

set up virtualenv using python 3

This can be done by:

    mkvirtualenv --python=python3 strabo

### Python packages

pip install -r requirements.txt

#### OSError: cannot decode filename

If you ever get an error that looks like the above, this means you do not have the system library that decodes images set up on your computer. You will have to uninstall Pillow, install the system library and reinstall Pillow. For jpeg files on OSX, this can be done with brew by:

    pip uninstall Pillow
    brew install libjpeg
    pip install  --no-cache-dir -I Pillow

On other systems, the process should be very similar, but the specific package and package system will be different.

Other image formats (png?) might also have a similar problem.

#### geojson module has no attribute error

This most likely means you are using python2. Use python 3 as shown above. The easiest way to do this is by removing the old virtualenv and making a new one using python 3:

    deactivate
    rmvirtualenv strabo

Then set up new virtualenv as show above.
