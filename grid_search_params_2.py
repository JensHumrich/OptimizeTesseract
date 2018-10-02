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

paramlist1 = ['-t %d' % (30 + (4*i)) for i in range(5)]
paramlist2 = ['-s %f' % (0.4 + (i*0.1)) for i in range(5)]
paramlist5 = ['-S %d' % (i*40) for i in range(5)]
paramlist6 = ['-a %f' % (i*0.2) for i in range(5)]

paramlist = ['%s %s %s %s' % (p1, p2, p5, p6) for p1 in paramlist1 for p2 in paramlist2 for p5 in paramlist5 for p6 in paramlist6]

best_params = ''
best_ratio = 0
for params in paramlist:
    clean_call = './textcleaner.sh -f 80 -o 12 %s ./../dni_samples/2.png o.jpg' % params
    tess_call  = ' tesseract -l spa --oem 1 o.jpg o'
    
    home_path = '/Users/jh186076/Documents/07_Abanca/1_text_recognition/improve_raw_images/'
    
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
    if ratio >= best_ratio:
        print(params)
        print('Ratio %f ' % ratio )
        best_ratio = ratio
        best_params = params


print ("./textcleaner.sh -f 80 -o 12 -t 42 -s 0.800000 -S 160 -a 0.800000 ./../dni_samples/2.png o.jpg")