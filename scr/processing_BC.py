#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pdb
import numpy as np
from scipy.optimize import curve_fit
from datetime import datetime
from scr.functions import dcon_dt, sed_flux, FdPdt, Cw, Fs_massbalance
import pandas as pd
import logging
pd.set_option('mode.chained_assignment', None)

def processing_BC(data, core, meta, kbounds):
    # Selecting time frame
    if int(meta[0][:2]) > int(meta[1][:2]):
        date_end = pd.to_datetime(meta[2]) + pd.Timedelta('1days')
        date_end = str(date_end.date())
    else:
        date_end = meta[2]
    time_start = meta[2] + ' ' + meta[0]
    time_end = date_end + ' ' + meta[1]
    data = data[time_start:time_end]
    t_start = datetime.strptime(time_start, '%Y-%m-%d %H:%M')
    t_end = datetime.strptime(time_end, '%Y-%m-%d %H:%M')
    P = meta[10] # (hPa) Pressure
    T = meta[11] # (C) Temperature
    hw = meta[8] # (cm) Water height inside core
    ha = meta[9] # (cm) Air height inside core
    #print(data.iloc[0], data.iloc[-1])
    results = dict()
    data_r = dict()

    for var in data:
        logging.info('Processing variable %s', var[:3])
        # Changing ppm to partial pressure
        data.loc[:,var] = data[var]*P*1E-4 #[Pa]

        # Calculate flux: Derivative
        dtmin = 30/60. # Every dtmin min
        dPdt, dt = dcon_dt(data, var, dtmin, hw, ha, T)
        # Fluxes calculated with the last 10 min of data
        Fa, Fs, pol, time = sed_flux(data, var, 5, hw, ha, T)
        # Fit curves
        Px = data[var].values
        t = np.arange(0,len(Px))
        if var == 'CH4d_ppm':
            Cw0 = meta[4] # (umol/l) Initial CH4 concentration measured with headspace
            Cwf = meta[5] # (umol/l) Final CH4 concentration measured with headspace
            bounds = ([0, kbounds[0][0]/86400.], [1, kbounds[0][1]/86400.])
        else:
            Cw0 = meta[6] # (umol/l) Initial CO2 concentration measured with headspace
            Cwf = meta[7] # (umol/l) Final CO2 concentration measured with headspace
            bounds = ([-1, kbounds[1][0]/86400.], [1, kbounds[1][1]/86400.])
        # Fitting equation based on dPdt
        try:
            dPdt_opt, dPdt_cov = curve_fit(lambda t, Fs, k: \
                                        FdPdt(dt, var, Fs, Cw0/1000., k,
                                                Px[0], T, hw, ha), dt, dPdt,
                                        bounds=bounds)

            # Evaluation of fittig curve based on dPdt with optimum
            dPdt_f = FdPdt(dt, var, dPdt_opt[0], Cw0/1000., dPdt_opt[1], Px[0],
                        T, hw, ha)
            Cw_f = Cw(dPdt_f, Px, dPdt_opt[1], var, dtmin, hw, ha, T)
            Fs_dPdt_f = dPdt_opt[0]*1000*86400
            k_dPdt_f = dPdt_opt[1]*86400
            dPdt_f2 = FdPdt(dt, var, Fs/86400/1000., Cw0/1000., dPdt_opt[1], Px[0],
                            T, hw, ha)
            Cw_f2 = Cw(dPdt_f2, Px, dPdt_opt[1], var, dtmin, hw, ha, T)

        except RuntimeError as fnf_error:
            dPdt_f = np.NAN
            dPdt_f2 = np.NAN
            Cw_f = [np.NAN]
            Fs_dPdt_f = np.NAN
            k_dPdt_f = np.NAN
            dPdt_f2 = np.NAN
            Cw_f2 = [np.NAN]
            logging.warning(fnf_error)
        Px0 = data[var].iloc[0]
        Pxf = data[var].iloc[-1]
        Fs_MB, Cwf = Fs_massbalance(Cw0, Cwf, Px0, Pxf, hw, ha, t_start, t_end, T)
        # Evaluation of fittig curve based on dPdt with linear flux
        # Water concentration with optimus values
        results[var] = {'BC_Name': core, 'Start': t_start, 'End': t_end,
                        'Fs_lin': Fs,'Fs_dPdt': Fs_dPdt_f, 'Fs_MB': Fs_MB,
                        'k': k_dPdt_f, 'Cw0': Cw0,'Cwf': Cwf, 'Pol': pol,
                        'Cwf_dPdt': Cw_f[-1]*1000, 'Cwf_lin': Cw_f2[-1]*1000,
                        'P' : P, 'Temp': T, 'Hw': hw, 'Ha': ha,
                        'Px_start': Px0, 'Px_end': Pxf}
        data_r[var] = {'Px': Px, 'dPdt_fopt': dPdt_f, 'dPdt_flin': dPdt_f2,
                       'Cw_fopt': Cw_f, 'Cw_flin': Cw_f2, 'dPdt': dPdt,
                       'Time': data.index, 'dt': dt, 'Time_linf': time}
    return results, data_r
