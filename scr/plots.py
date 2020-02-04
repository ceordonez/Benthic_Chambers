#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import os
import pdb

plt.style.use('presentation')

def plot_results(results, data_r, meta, path, save=True):

    t = np.arange(len(data_r['CH4d_ppm']['Time']))/60.
    dt = data_r['CH4d_ppm']['dt']/60.

    linCH4 = np.poly1d(results['CH4d_ppm']['Pol'])
    linCO2 = np.poly1d(results['CO2d_ppm']['Pol'])
    time_lin = data_r['CH4d_ppm']['Time_linf']

    fig, ax = plt.subplots(3, 1, figsize=(8,7),sharex=True)
    title = ' '.join([meta[12], meta[13]])
    fig.suptitle(title)
    title1 = 'k = %.2f (m/d), cw(0) = %.2f (umol/l), Fs_linfit = %.2f (mmol/m2/d), Fs_ffit = %.2f (mmol/m2/d)' \
        % (results['CH4d_ppm']['k'], results['CH4d_ppm']['Cw0'],
           results['CH4d_ppm']['Fs_lin'], results['CH4d_ppm']['Fs_dPdt'])
    label1 = 'Fsed = %.2f' % results['CH4d_ppm']['Fs_dPdt'] #Fs_dPdtCH4_f
    label2 = 'Fsed = %.2f' % results['CH4d_ppm']['Fs_lin'] #FsCH4
    ax[0].set_title(title1)
    ax[0].plot(t, data_r['CH4d_ppm']['Px'], label='Data')
    ax[0].plot(t[-time_lin[-1]-1:], linCH4(time_lin), label = 'linfit')
    #ax[0].plot(t, PCH4_f, '--', label = 'Pfit')
    ax[1].plot(dt, data_r['CH4d_ppm']['dPdt'], label='Data')
    ax[1].plot(dt, data_r['CH4d_ppm']['dPdt_fopt'], '--', label = label1)
    ax[1].plot(dt, data_r['CH4d_ppm']['dPdt_flin'], '--', label = label2)
    ax[2].plot([dt[0],dt[-1]], [meta[4], meta[5]], 'o', label='Data')
    #ax[2].plot(dt, CwCH4*1000)
    ax[2].plot(dt, data_r['CH4d_ppm']['Cw_fopt']*1000, label=label1)
    ax[2].plot(dt, data_r['CH4d_ppm']['Cw_flin']*1000, label=label2)
    ax[1].legend()
    ax[2].legend()
    ax[0].set_ylabel('pCH$_4$ [Pa]')
    ax[1].set_ylabel('dPdt CH$_4$ [Pa/s]')
    ax[2].set_ylabel('Cw CH$_4$ [umol/l]')
    ax[2].set_xlabel('Time [min]')
    ax[0].yaxis.set_major_locator(plt.MaxNLocator(5))
    ax[1].yaxis.set_major_locator(plt.MaxNLocator(5))
    ax[2].yaxis.set_major_locator(plt.MaxNLocator(5))

    if save:
        names = [str(meta[12]), str(meta[13]), str(meta[2]), str(meta[3]), 'CH4']
        figname = '_'.join(names)
        path_out = os.path.join(path, meta[12], 'Results', 'Benthic_Chamber')
        if not os.path.exists(path_out):
            os.makedirs(path_out)
        plt.savefig(path_out + '/'+ figname + '.png',fmt='.png',dpi=300)
    else:
        plt.show()

