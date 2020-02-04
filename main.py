#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import os
#import pandas as pd
#import datetime as dt
#import matplotlib.pyplot as plt
import pdb
from scr.read_lgr import read_lgrdata
from conf_exp import *
from scr.processing_BC import processing_BC

#plt.style.use('presentation')

def main():
    data = read_lgrdata(path, meta)
    results, data_r = processing_BC(data, meta)


if __name__ == '__main__':
    main()


