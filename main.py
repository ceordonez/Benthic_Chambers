#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import pdb
from scipy.optimize import curve_fit
from funtions import sed_flux, pC_sol, pCsol, dcon_dt, foot_pos,dPdt, Cw
from scr.read_lgr import read_lgrdata
from conf_exp import *

plt.style.use('presentation')

def main():
    data = read_lgrdata(path, meta)
    varname_CH4 = data.keys()[0]
    varname_CO2 = data.keys()[1]

    CwCH4_0 = meta[4]  # (umol/l) initial CH4 concentration measured with headspace
    CwCO2_0 = meta[6]  # (umol/l) initial CH4 concentration measured with headspace

    T = meta[11] # (C) Temperature
    P = meta[10] # (hPa) Pressure
    hw = meta[8] # (cm) Water height inside core
    ha = meta[9] # (cm) Air height inside core
    pdb.set_trace()

if __name__ == '__main__':
    main()


