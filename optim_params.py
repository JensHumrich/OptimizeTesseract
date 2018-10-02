#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 17:17:29 2018

@author: jh186076

A simple grid search over the parameters of the script 'textcleaner.sh'

Evaluate different parameteres and their influence on the recognized letters.

Evaluate by giving points depending on the distance between the target and the produced solution.

"""
from fuzzywuzzy import fuzz
import subprocess
from subprocess import PIPE
import os

my_env = {**os.environ, 'TESSDATA_PREFIX': '/Users/jh186076/Documents/07_Abanca/1_text_recognition/tessdata'}

target = 'ESPAÑA DOCUMENTO NATIONAL IDENTIDAD ESPAÑOLA ESPAÑOLA CARMEN F ESP BAA000589 01 01 2025 99999999R 987654'
home_path = '/Users/jh186076/Documents/07_Abanca/1_text_recognition/improve_raw_images/'
    

"""
-f .... filtersize ...... size of filter used to clean background;
......................... integer>0; default=15
-o .... offset .......... offset of filter in percent used to reduce noise;
......................... integer>=0; default=5
-t .... threshold ....... text smoothing threshold; 0<=threshold<=100;
......................... nominal value is about 50; default is no smoothing
-s .... sharpamt ........ sharpening amount in pixels; float>=0;
......................... nominal about 1; default=0

-g ...................... convert document to grayscale before enhancing
-e .... enhance ......... enhance image brightness before cleaning;
......................... choices are: none, stretch or normalize;
......................... default=none
-S .... saturation ...... color saturation expressed as percent; integer>=0;
......................... only applicable if -g not set; a value of 100 is
......................... no change; default=200 (double saturation)
-a .... adaptblur ....... alternate text smoothing using adaptive blur;
......................... floats>=0; default=0 (no smoothing)
-F .... fuzzval ......... fuzz value for determining bgcolor when bgcolor=image;
......................... integer>=0; default=10
-i .... invert .......... invert colors; choices are: 1 or 2 for one-way or two-ways
......................... (input or input and output); default is no inversion 
"""

tess_call  = ' tesseract -l spa --oem 1 o.jpg o'

import numpy as np
from skopt import gp_minimize


def f(params):
    print(params)
    #clean_call = './textcleaner.sh -t {} -s {} -f {} -o {} ./../dni_samples/2.png o.jpg'.format(*params)
    clean_call = './textcleaner.sh -t 40 -s 0.6 -f 80 -o 12 -S {} -a {} -F {} ./../dni_samples/2.png o.jpg'.format(*params)
    # Run textcleaner
    t2 = subprocess.call(clean_call, shell=True, cwd=home_path)
    
    # Run tesseract
    t1 = subprocess.call(tess_call, 
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             shell=True,
                             env=my_env, 
                             cwd=home_path)
    
    tess_out = open(home_path+'o.txt').read()
    ratio = fuzz.ratio(target, tess_out)
    print (ratio)
    #print(tess_out)
    return -1.*ratio

res = gp_minimize(f, [(0, 400) , (0.,2.), (0,100) ] )
print(res)
#./textcleaner.sh -t 40 -s 0.600000 -f 80 -o 12  ./../dni_samples/2.png o.jpg