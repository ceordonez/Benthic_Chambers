#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pdb
import numpy as np
from scipy.optimize import curve_fit
from scr.functions import dcon_dt, sed_flux, FdPdt, Cw
import pandas as pd
import logging
pd.set_option('mode.chained_assignment', None)

def processing_BC(data, meta):
    # Selecting time frame
    data = data[meta[2] + ' ' + meta[0]:meta[2] + ' ' + meta[1]]
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
        Fa, Fs, pol, time = sed_flux(data, var, 10, hw, ha, T)
        # Fit curves
        Px = data[var].values
        t = np.arange(0,len(Px))
        if var == 'CH4d_ppm':
            Cw0 = meta[4] # (umol/l) initial CH4 concentration measured with headspace
            bounds = ([0, 10/86400.], [1, 30/86400.])
        else:
            Cw0 = meta[6] # (umol/l) initial CO2 concentration measured with headspace
            bounds = ([-1, 10/86400.], [1, 30/86400.])
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

        # Evaluation of fittig curve based on dPdt with linear flux
        # Water concentration with optimus values
        results[var] = {'BC_Name': meta[13], 'Date': meta[2], 'Start': meta[0],
                        'End': meta[1], 'Fs_lin': Fs, 'Pol': pol,
                        'Fs_dPdt': Fs_dPdt_f, 'k': k_dPdt_f, 'Cw0': Cw0,
                        'Cwf_dPdt': Cw_f[-1]*1000, 'Cwf_lin': Cw_f2[-1]*1000,
                        'P' : P, 'Temp': T, 'Hw': hw, 'Ha': ha}
        data_r[var] = {'Px': Px, 'dPdt_fopt': dPdt_f, 'dPdt_flin': dPdt_f2,
                       'Cw_fopt': Cw_f, 'Cw_flin': Cw_f2, 'dPdt': dPdt,
                       'Time': data.index, 'dt': dt, 'Time_linf': time}
    return results, data_r



"""
## Flux calculations

## Fittings
PCO2 = data[varname_CO2].values

# Base on partial pressure function
PCO2_opt, PCO2_cov = curve_fit(lambda t, Fs, k: \
                            pC_sol(t, varname_CO2, Fs, CwCO2_0/1000., k, PCO2[0], T, hw, ha),
                            t, PCO2, bounds=([-1, 0], [1, 1]))
PCO2_f = pC_sol(t, varname_CO2, PCO2_opt[0], CwCO2_0/1000., PCO2_opt[1], PCO2[0], T, hw, ha)

PCH4_opt, PCH4_cov = curve_fit(lambda t, Fs, k: \
                            pC_sol(t, varname_CH4, Fs, CwCH4_0/1000., k, PCH4[0], T, hw, ha)
                            t, PCH4, bounds=([0, 0], [1, 1]))
PCH4_f = pC_sol(t, varname_CH4, PCH4_opt[0], CwCH4_0/1000., PCH4_opt[1], PCH4[0], T, hw, ha)
# Base on dP/dt funtion
#dPdtCH4_opt, dPdtCH4_cov = curve_fit(lambda t, Fs, k: \
#                                    dPdt(dt, varname_CH4, Fs, CwCH4_0/1000., k,
#                                         PCH4[0], T, hw, ha), dt, dPdtCH4,
#                                     bounds=([0, 14/86400.], [1, 25/86400.]))
#dPdtCH4_opt, dPdtCH4_cov = curve_fit(lambda t, Fs: \
#                                     dPdt(dt, varname_CH4, Fs, CwCH4_0/1000,
#                                     k_CH4/86400., PCH4[0], T, hw, ha),
#                                     dt, dPdtCH4, bounds=([0], [1]))
#dPdtCH4_opt, dPdtCH4_cov = curve_fit(lambda t, k: \
#                                     dPdt(dt, varname_CH4, Fsed/86400/1000.,
#                                     CwCH4_0/1000, k, PCH4[0], T, hw, ha),
#                                     dt, dPdtCH4, bounds=([0], [1]))


dPdtCO2_opt, dPdtCO2_cov = curve_fit(lambda t, Fs, k: \
                                    dPdt(dt, varname_CO2, Fs, CwCO2_0/1000, k,
                                         PCO2[0], T, hw, ha),
                                    dt, dPdtCO2, bounds=([-1, 0], [1, 1]))
dPdtCO2_f = dPdt(dt, varname_CO2, dPdtCO2_opt[0], CwCO2_0/1000, dPdtCO2_opt[1],
                 PCO2[0], T, hw, ha)

## Calculation sediment fluxes and k
# Base on partial pressure funtion
Fs_PCH4_f = PCH4_opt[0]*1000*86400
Fs_PCO2_f = PCO2_opt[0]*1000*86400
k_PCH4 = PCH4_opt[1]*86400
k_PCO2 = PCO2_opt[1]*86400

# Base on dPdt funtion
Fs_dPdtCH4_f = dPdtCH4_opt[0]*1000*86400
#Fs_dPdtCH4_f = Fsed
Fs_dPdtCO2_f = dPdtCO2_opt[0]*1000*86400
k_dPdtCH4 = dPdtCH4_opt[1]*86400
#k_dPdtCH4 = k_CH4
#k_dPdtCH4 = dPdtCH4_opt[0]*86400
k_dPdtCO2 = dPdtCO2_opt[1]*86400
"""
