#!/usr/bin/python

"""
Image converter for 'Uncanny Eyes' project.  Generates tables for
eyeData.h file.  Requires Python Imaging Library.  Expects six image
files: sclera, iris, upper and lower eyelid map (symmetrical), upper
and lower eyelid map (asymmetrical L/R) -- defaults will be used for
each if not specified.  Also generates polar coordinate map for iris
rendering (pass diameter -- must be an even value -- as 7th argument),
pupil is assumed round unless pupilMap.png image is present.
Output is to stdout; should be redirected to file for use.
"""

# This is kinda some horrible copy-and-paste code right now for each of
# the images...could be improved, but basically does the thing.

import sys
import math
from PIL import Image
from hextable import HexTable

# OPEN AND VALIDATE SCLERA IMAGE FILE --------------------------------------

try:
    FILENAME = sys.argv[1]
except IndexError:
    FILENAME = 'sclera.png' # Default filename if argv 1 not provided
IMAGE = Image.open(FILENAME)
IMAGE = IMAGE.convert('RGB')
PIXELS = IMAGE.load()

# GENERATE SCLERA ARRAY ----------------------------------------------------

print('#define SCLERA_WIDTH  ' + str(IMAGE.size[0]))
print('#define SCLERA_HEIGHT ' + str(IMAGE.size[1]))
print('')

sys.stdout.write('const uint16_t sclera[SCLERA_HEIGHT][SCLERA_WIDTH] = {')
HEX = HexTable(IMAGE.size[0] * IMAGE.size[1], 8, 4)

# Convert 24-bit image to 16 bits:
for y in range(IMAGE.size[1]):
    for x in range(IMAGE.size[0]):
        p = PIXELS[x, y] # Pixel data (tuple)
        HEX.write(
            ((p[0] & 0b11111000) << 8) | # Convert 24-bit RGB
            ((p[1] & 0b11111100) << 3) | # to 16-bit value w/
            (p[2] >> 3))                 # 5/6/5-bit packing

# OPEN AND VALIDATE IRIS IMAGE FILE ----------------------------------------

try:
    FILENAME = sys.argv[2]
except IndexError:
    FILENAME = 'iris.png' # Default filename if argv 2 not provided
IMAGE = Image.open(FILENAME)
if (IMAGE.size[0] > 512) or (IMAGE.size[1] > 128):
    sys.stderr.write('Image can\'t exceed 512 pixels wide or 128 pixels tall')
    exit(1)
IMAGE = IMAGE.convert('RGB')
PIXELS = IMAGE.load()

# GENERATE IRIS ARRAY ------------------------------------------------------

print('')
print('#define IRIS_MAP_WIDTH  ' + str(IMAGE.size[0]))
print('#define IRIS_MAP_HEIGHT ' + str(IMAGE.size[1]))
print('')

sys.stdout.write('const uint16_t iris[IRIS_MAP_HEIGHT][IRIS_MAP_WIDTH] = {')
HEX.reset(IMAGE.size[0] * IMAGE.size[1])

for y in range(IMAGE.size[1]):
    for x in range(IMAGE.size[0]):
        p = PIXELS[x, y] # Pixel data (tuple)
        HEX.write(
            ((p[0] & 0b11111000) << 8) | # Convert 24-bit RGB
            ((p[1] & 0b11111100) << 3) | # to 16-bit value w/
            (p[2] >> 3))                 # 5/6/5-bit packing

# OPEN AND VALIDATE UPPER EYELID THRESHOLD MAP (symmetrical) ---------------

try:
    FILENAME = sys.argv[3]
except IndexError:
    FILENAME = 'lid-upper-symmetrical.png' # Default if argv 3 not provided
IMAGE = Image.open(FILENAME)
if (IMAGE.size[0] != 128) or (IMAGE.size[1] != 128):
    sys.stderr.write('Image size must match screen size')
    exit(1)
IMAGE = IMAGE.convert('L')
PIXELS = IMAGE.load()

# GENERATE UPPER LID ARRAY (symmetrical) -----------------------------------

print('')
print('#define SCREEN_WIDTH  ' + str(IMAGE.size[0]))
print('#define SCREEN_HEIGHT ' + str(IMAGE.size[1]))
print('')
print('#ifdef SYMMETRICAL_EYELID')
print('')

sys.stdout.write('const uint8_t upper[SCREEN_HEIGHT][SCREEN_WIDTH] = {')
HEX = HexTable(IMAGE.size[0] * IMAGE.size[1], 12, 2)

for y in range(IMAGE.size[1]):
    for x in range(IMAGE.size[0]):
        HEX.write(PIXELS[x, y]) # 8-bit value per pixel

# OPEN AND VALIDATE LOWER EYELID THRESHOLD MAP (symmetrical) ---------------

try:
    FILENAME = sys.argv[4]
except IndexError:
    FILENAME = 'lid-lower-symmetrical.png' # Default if argv 4 not provided
IMAGE = Image.open(FILENAME)
if (IMAGE.size[0] != 128) or (IMAGE.size[1] != 128):
    sys.stderr.write('Image size must match screen size')
    exit(1)
IMAGE = IMAGE.convert('L')
PIXELS = IMAGE.load()

# GENERATE LOWER LID ARRAY (symmetrical) -----------------------------------

print('')
sys.stdout.write('const uint8_t lower[SCREEN_HEIGHT][SCREEN_WIDTH] = {')
HEX.reset(IMAGE.size[0] * IMAGE.size[1])

for y in range(IMAGE.size[1]):
    for x in range(IMAGE.size[0]):
        HEX.write(PIXELS[x, y]) # 8-bit value per pixel

# OPEN AND VALIDATE UPPER EYELID THRESHOLD MAP (asymmetrical) --------------

try:
    FILENAME = sys.argv[5]
except IndexError:
    FILENAME = 'lid-upper.png' # Default filename if argv 5 not provided
IMAGE = Image.open(FILENAME)
if (IMAGE.size[0] != 128) or (IMAGE.size[1] != 128):
    sys.stderr.write('Image size must match screen size')
    exit(1)
IMAGE = IMAGE.convert('L')
PIXELS = IMAGE.load()

# GENERATE UPPER LID ARRAY (asymmetrical) ----------------------------------

print('')
print('#else')
print('')

sys.stdout.write('const uint8_t upper[SCREEN_HEIGHT][SCREEN_WIDTH] = {')
HEX.reset(IMAGE.size[0] * IMAGE.size[1])

for y in range(IMAGE.size[1]):
    for x in range(IMAGE.size[0]):
        HEX.write(PIXELS[x, y]) # 8-bit value per pixel

# OPEN AND VALIDATE LOWER EYELID THRESHOLD MAP (asymmetrical) --------------

try:
    FILENAME = sys.argv[6]
except IndexError:
    FILENAME = 'lid-lower.png' # Default filename if argv 6 not provided
IMAGE = Image.open(FILENAME)
if (IMAGE.size[0] != 128) or (IMAGE.size[1] != 128):
    sys.stderr.write('Image size must match screen size')
    exit(1)
IMAGE = IMAGE.convert('L')
PIXELS = IMAGE.load()

# GENERATE LOWER LID ARRAY (asymmetrical) ----------------------------------

print('')
sys.stdout.write('const uint8_t lower[SCREEN_HEIGHT][SCREEN_WIDTH] = {')
HEX.reset(IMAGE.size[0] * IMAGE.size[1])

for y in range(IMAGE.size[1]):
    for x in range(IMAGE.size[0]):
        HEX.write(PIXELS[x, y]) # 8-bit value per pixel

# GENERATE POLAR COORDINATE TABLE ------------------------------------------

try:
    IRIS_SIZE = int(sys.argv[7])
except IndexError:
    IRIS_SIZE = 80 # Default size if argv 7 not provided
if IRIS_SIZE % 2 != 0:
    sys.stderr.write('Iris diameter must be even value')
    exit(1)
RADIUS = IRIS_SIZE / 2
# For unusual-shaped pupils (dragon, goat, etc.), a precomputed image
# provides polar distances.  Optional 8th argument is filename (or file
# 'pupilMap.png' in the local directory) is what's used, otherwise a
# regular round iris is calculated.
try:
    FILENAME = sys.argv[8]
except IndexError:
    FILENAME = 'pupilMap.png' # Default filename if argv 8 not provided
USE_PUPIL_MAP = True
try:
    IMAGE = Image.open(FILENAME)
    if (IMAGE.size[0] != IRIS_SIZE) or (IMAGE.size[1] != IRIS_SIZE):
        sys.stderr.write('Image size must match iris size')
        exit(1)
    IMAGE = IMAGE.convert('L')
    PIXELS = IMAGE.load()
except IOError:
    USE_PUPIL_MAP = False

print('')
print('#endif // SYMMETRICAL_EYELID')
print('')
print('#define IRIS_WIDTH  ' + str(IRIS_SIZE))
print('#define IRIS_HEIGHT ' + str(IRIS_SIZE))

# One element per screen pixel, 16 bits per element -- high 9 bits are
# angle relative to center point (fixed point, 0-511) low 7 bits are
# distance from circle perimeter (fixed point, 0-127, pixels outsize circle
# are set to 127).

sys.stdout.write('\nconst uint16_t polar[%s][%s] = {' % (IRIS_SIZE, IRIS_SIZE))
HEX = HexTable(IRIS_SIZE * IRIS_SIZE, 8, 4)

for y in range(IRIS_SIZE):
    dy = y - RADIUS + 0.5
    for x in range(IRIS_SIZE):
        dx = x - RADIUS + 0.5
        distance = math.sqrt(dx * dx + dy * dy)
        if distance >= RADIUS: # Outside circle
            HEX.write(127) # angle = 0, dist = 127
        else:
            if USE_PUPIL_MAP:
                # Look up polar coordinates in pupil map image
                angle = math.atan2(dy, dx) # -pi to +pi
                angle += math.pi           # 0.0 to 2pi
                angle /= (math.pi * 2.0)   # 0.0 to <1.0
                distance = PIXELS[x, y] / 255.0
            else:
                angle = math.atan2(dy, dx) # -pi to +pi
                angle += math.pi           # 0.0 to 2pi
                angle /= (math.pi * 2.0)   # 0.0 to <1.0
                distance /= RADIUS         # 0.0 to <1.0
            distance *= 128.0              # 0.0 to <128.0
            if distance > 127:
                distance = 127 # Clip
            a = int(angle * 512.0)    # 0 to 511
            d = 127 - int(distance)   # 127 to 0
            HEX.write((a << 7) | d)
