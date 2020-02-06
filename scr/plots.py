#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import os
import pdb

plt.style.use('presentation')

def plot_results(results, data_r, meta, path, save=True):

    for var in data_r:
        t = np.arange(len(data_r[var]['Time']))/60.
        dt = data_r[var]['dt']/60.

        linf = np.poly1d(results[var]['Pol'])
        time_lin = data_r[var]['Time_linf']

        fig, ax = plt.subplots(3, 1, figsize=(8,7),sharex=True)
        title = ' '.join([meta[12], meta[13]])
        fig.suptitle(title)
        title1 = 'k = %.2f (m/d), cw(0) = %.2f (umol/l), Fs_linfit = %.2f (mmol/m2/d), Fs_ffit = %.2f (mmol/m2/d)' \
            % (results[var]['k'], results[var]['Cw0'],
            results[var]['Fs_lin'], results[var]['Fs_dPdt'])
        label1 = 'Fsed = %.2f' % results[var]['Fs_dPdt'] #Fs_dPdtCH4_f
        label2 = 'Fsed = %.2f' % results[var]['Fs_lin'] #FsCH4
        ax[0].set_title(title1)
        ax[0].plot(t, data_r[var]['Px'], 'k', label='Data')
        ax[0].plot(t[-time_lin[-1]-1:], linf(time_lin), 'r', label = 'linfit')
        ax[1].plot(dt, data_r[var]['dPdt'], 'k', label='Data')
        if not np.isnan(data_r[var]['dPdt_fopt']).all():
            ax[1].plot(dt, data_r[var]['dPdt_fopt'], 'b--', label = label1)
            ax[1].plot(dt, data_r[var]['dPdt_flin'], 'r--', label = label2)
            ax[2].plot(dt, data_r[var]['Cw_fopt']*1000, 'b', label=label1)
            ax[2].plot(dt, data_r[var]['Cw_flin']*1000, 'r', label=label2)
        if 'CH4' in var:
            ax[2].plot([dt[0],dt[-1]], [meta[4], meta[5]], 'ko', label='Data')
        else:
            ax[2].plot([dt[0],dt[-1]], [meta[6], meta[7]], 'ko', label='Data')
        ax[1].legend()
        ax[2].legend()
        ax[2].set_xlabel('Time [min]')
        if 'CH4' in var:
            ax[0].set_ylabel('pCH$_4$ [Pa]')
            ax[1].set_ylabel('dPdt CH$_4$ [Pa/s]')
            ax[2].set_ylabel('Cw CH$_4$ [umol/l]')
        else:
            ax[0].set_ylabel('pCO$_2$ [Pa]')
            ax[1].set_ylabel('dPdt CO$_2$ [Pa/s]')
            ax[2].set_ylabel('Cw CO$_2$ [umol/l]')
        ax[0].yaxis.set_major_locator(plt.MaxNLocator(5))
        ax[1].yaxis.set_major_locator(plt.MaxNLocator(5))
        ax[2].yaxis.set_major_locator(plt.MaxNLocator(5))

        if save:
            names = [str(meta[12]), str(meta[13]), str(meta[2]), str(meta[3]),
                     var[:3]]
            figname = '_'.join(names)
            path_out = os.path.join(path, meta[12], 'Results', 'Benthic_Chamber')
            if not os.path.exists(path_out):
                os.makedirs(path_out)
            plt.savefig(path_out + '/'+ figname + '.png',fmt='.png',dpi=300)
    if not save:
        plt.show()

