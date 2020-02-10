#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fpdf import FPDF
from PIL import Image
import matplotlib.image as mpimg
import glob
import os
import pdb

lakes = ('Baldegg', 'Soppen', 'Noir', 'Lioson', 'Chavonnes', 'Bretaye')
path = '/home/cesar/Dropbox/Cesar/PhD/Data/Fieldwork/MultiLakeSurvey/Lakes'

pdf = FPDF()
new = False
for lake in lakes:
    pathfig = os.path.join(path, lake, 'Results','Benthic_Chamber')
    os.chdir(pathfig)
    if not new:
        pdf.add_page()
    i = 0
    x = 10
    b = 10
    files = glob.glob("*_CH4*")
    files.sort()
    for file in files:
        print(file)
        img = Image.open(file)
        pdf.image(file, x, b, 100, 100)
        if (i % 2) == 0:
            x+=100
        else:
            x-=100
            b+=100
        i+=1
        if i == 4:
            i = 0
            x = 10
            b = 10
            pdf.add_page()
            new = True
        else:
            new = False
os.chdir(path)
pdf.output('allfigures.pdf','F')



