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
from scr.plots import plot_results

#plt.style.use('presentation')

def main():
    data = read_lgrdata(path, meta)
    results, data_r = processing_BC(data, meta)
    plot_results(results, data_r, meta, path)

if __name__ == '__main__':
    main()


