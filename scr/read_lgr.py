#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scr.functions import foot_pos
import pandas as pd
import os

def read_lgrdata(path, lake, meta):
    date = meta[2]
    filename = 'gga_' + date + '_' + meta[3] + '.txt'
    lgrfile = os.path.join(path, lake, 'Data', 'LGR', date, filename)
    ifoot = foot_pos(lgrfile)
    rfile = pd.read_csv(lgrfile, sep=',', header=1, skipfooter=ifoot,
                        squeeze=True, infer_datetime_format=True,
                        parse_dates=[0], usecols=[0,7,9], engine='python',
                        index_col=[0], names=['Time','CH4d_ppm','CO2d_ppm'])
    return rfile


