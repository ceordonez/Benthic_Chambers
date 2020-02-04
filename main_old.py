#!/usr/bin/env python
# -*- coding: utf-8 -*-


def processing_BC(data, meta):
    # Selecting time frame
    data = data[meta[2] + ' ' + meta[0]:meta[2] + ' ' + meta[1]]
    P = meta[10] # (hPa) Pressure
    T = meta[11] # (C) Temperature
    hw = meta[8] # (cm) Water height inside core
    ha = meta[9] # (cm) Air height inside core
    for var in data:
        # Changing ppm to partial pressure
        data[var] = data[var]*P*1E-4 #[Pa]
        # Calculate flux: Derivative
        dPdtCH4, dt = dcon_dt(data, varname_CH4, dtmin, hw, ha, T)

def ppmtoP(data, meta, var):
    """Selecting time frame and change to partial pressure
    """
    data[varname_CO2] = data[varname_CO2]*P*1E-4 #[Pa]

    varname_CH4 = data.keys()[0]
    varname_CO2 = data.keys()[1]

    CwCH4_0 = meta[4]  # (umol/l) initial CH4 concentration measured with headspace
    CwCO2_0 = meta[6]  # (umol/l) initial CH4 concentration measured with headspace

    pdb.set_trace()


print(data.iloc[0], data.iloc[-1])

## Flux calculations
# Derivative
dtmin = 30/60.
dPdtCO2, dt = dcon_dt(data, varname_CO2, dtmin, hw, ha, T)

FaCH4, FsCH4, polCH4, time1 = sed_flux(data, varname_CH4, 10, hw, ha, T)
FaCO2, FsCO2, polCO2, time2 = sed_flux(data, varname_CO2, 10, hw, ha, T)

## Fittings
PCH4 = data[varname_CH4].values
PCO2 = data[varname_CO2].values
t = np.arange(0,len(PCO2))

# Base on partial pressure function
"""
PCO2_opt, PCO2_cov = curve_fit(lambda t, Fs, k: \
                            pC_sol(t, varname_CO2, Fs, CwCO2_0/1000., k, PCO2[0], T, hw, ha),
                            t, PCO2, bounds=([-1, 0], [1, 1]))
PCO2_f = pC_sol(t, varname_CO2, PCO2_opt[0], CwCO2_0/1000., PCO2_opt[1], PCO2[0], T, hw, ha)

PCH4_opt, PCH4_cov = curve_fit(lambda t, Fs, k: \
                            pC_sol(t, varname_CH4, Fs, CwCH4_0/1000., k, PCH4[0], T, hw, ha)
                            t, PCH4, bounds=([0, 0], [1, 1]))
PCH4_f = pC_sol(t, varname_CH4, PCH4_opt[0], CwCH4_0/1000., PCH4_opt[1], PCH4[0], T, hw, ha)
"""
# Base on dP/dt funtion
#dPdtCH4_opt, dPdtCH4_cov = curve_fit(lambda t, Fs, k: \
#                                    dPdt(dt, varname_CH4, Fs, CwCH4_0/1000., k,
#                                         PCH4[0], T, hw, ha), dt, dPdtCH4,
#                                     bounds=([0, 14/86400.], [1, 25/86400.]))
dPdtCH4_opt, dPdtCH4_cov = curve_fit(lambda t, Fs, k: \
                                    dPdt(dt, varname_CH4, Fs, CwCH4_0/1000., k,
                                         PCH4[0], T, hw, ha), dt, dPdtCH4,
                                     bounds=([0, 0/86400.], [1, 1]))
#dPdtCH4_opt, dPdtCH4_cov = curve_fit(lambda t, Fs: \
#                                     dPdt(dt, varname_CH4, Fs, CwCH4_0/1000,
#                                     k_CH4/86400., PCH4[0], T, hw, ha),
#                                     dt, dPdtCH4, bounds=([0], [1]))
#dPdtCH4_opt, dPdtCH4_cov = curve_fit(lambda t, k: \
#                                     dPdt(dt, varname_CH4, Fsed/86400/1000.,
#                                     CwCH4_0/1000, k, PCH4[0], T, hw, ha),
#                                     dt, dPdtCH4, bounds=([0], [1]))
dPdtCH4_f = dPdt(dt, varname_CH4, dPdtCH4_opt[0], CwCH4_0/1000., dPdtCH4_opt[1],
                 PCH4[0], T, hw, ha)
dPdtCH4_f2 = dPdt(dt, varname_CH4, FsCH4/86400/1000., CwCH4_0/1000.,
                  dPdtCH4_opt[1], PCH4[0], T, hw, ha)

CwCH4_f = Cw(dPdtCH4_f, PCH4, dPdtCH4_opt[1], varname_CH4, dtmin, hw, ha, T)
CwCH4_f2 = Cw(dPdtCH4_f2, PCH4, dPdtCH4_opt[1], varname_CH4, dtmin, hw, ha, T)

dPdtCO2_opt, dPdtCO2_cov = curve_fit(lambda t, Fs, k: \
                                    dPdt(dt, varname_CO2, Fs, CwCO2_0/1000, k,
                                         PCO2[0], T, hw, ha),
                                    dt, dPdtCO2, bounds=([-1, 0], [1, 1]))
dPdtCO2_f = dPdt(dt, varname_CO2, dPdtCO2_opt[0], CwCO2_0/1000, dPdtCO2_opt[1],
                 PCO2[0], T, hw, ha)
"""
## Calculation sediment fluxes and k
# Base on partial pressure funtion
Fs_PCH4_f = PCH4_opt[0]*1000*86400
Fs_PCO2_f = PCO2_opt[0]*1000*86400
k_PCH4 = PCH4_opt[1]*86400
k_PCO2 = PCO2_opt[1]*86400
"""
# Base on dPdt funtion
Fs_dPdtCH4_f = dPdtCH4_opt[0]*1000*86400
#Fs_dPdtCH4_f = Fsed
Fs_dPdtCO2_f = dPdtCO2_opt[0]*1000*86400
k_dPdtCH4 = dPdtCH4_opt[1]*86400
#k_dPdtCH4 = k_CH4
#k_dPdtCH4 = dPdtCH4_opt[0]*86400
k_dPdtCO2 = dPdtCO2_opt[1]*86400

## Plots
t = t/60.
dt = dt/60.
linCH4 = np.poly1d(polCH4)
linCO2 = np.poly1d(polCO2)
#title1 = 'k = %.2f (m/d), cw(0) = %.2f (umol/l), Fs_linfit = %.2f (mmol/m2/d), Fs_ffit = %.2f (mmol/m2/d)' \
#    % (k_PCH4, CwCH4_0, FsCH4, Fs_PCH4_f)
#title2 = 'k = %.2f (m/d), cw(0) = %.2f (umol/l), Fs_linfit = %.2f (mmol/m2/d), Fs_ffit = %.2f (mmol/m2/d)' \
#    % (k_PCO2, CwCO2_0, FsCO2, Fs_PCO2_f)

fig, ax = plt.subplots(3, 1, figsize=(8,7),sharex=True)
title = ' '.join([meta[12], meta[13]])
fig.suptitle(title)
title1 = 'k = %.2f (m/d), cw(0) = %.2f (umol/l), Fs_linfit = %.2f (mmol/m2/d), Fs_ffit = %.2f (mmol/m2/d)' \
    % (k_dPdtCH4, CwCH4_0, FsCH4, Fs_dPdtCH4_f)
label1 = 'Fsed = %.2f' % Fs_dPdtCH4_f
label2 = 'Fsed = %.2f' % FsCH4
ax[0].set_title(title1)
ax[0].plot(t, PCH4, label='Data')
ax[0].plot(t[-time1[-1]-1:], linCH4(time1), label = 'linfit')
#ax[0].plot(t, PCH4_f, '--', label = 'Pfit')
ax[1].plot(dt, dPdtCH4, label='Data')
ax[1].plot(dt, dPdtCH4_f, '--', label = label1)
ax[1].plot(dt, dPdtCH4_f2, '--', label = label2)
ax[2].plot([dt[0],dt[-1]], [meta[4], meta[5]], 'o', label='Data')
#ax[2].plot(dt, CwCH4*1000)
ax[2].plot(dt, CwCH4_f*1000, label=label1)
ax[2].plot(dt, CwCH4_f2*1000, label=label2)
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
    plt.savefig(figname + '.png',fmt='.png',dpi=300)
plt.show()

#ax[1].set_title(title2)
#ln1 = ax[1].plot(t, PCO2, label = 'Data')
#ln2 = ax[1].plot(t[-time2[-1]-1:], linCO2(time2), label = 'linfit')
#ln3 = ax[1].plot(t, PCO2_f,'--', label='Pfit')
#lns = ln1 + ln2 + ln3
#lbs = [l.get_label() for l in lns]
#ax[1].set_ylabel('pCO$_2$ [Pa]')
#ax[1].legend(lns, lbs, loc='upper center', ncol=6, bbox_transform=fig.transFigure,
#             bbox_to_anchor=(0.5,0.1))
#plt.subplots_adjust(bottom = 0.20)

"""

title2 = 'k = %.2f (m/d), cw(0) = %.2f (umol/l), Fs_linfit = %.2f (mmol/m2/d), Fs_ffit = %.2f (mmol/m2/d)' \
    % (k_dPdtCO2, CwCO2_0, FsCO2, Fs_dPdtCO2_f)
fig, ax = plt.subplots(2,1,figsize=(10,7),sharex=True)
ax[1].set_title(title2)
ln1 = ax[1].plot(dt, dPdtCO2, label = 'Data')
ln2 = ax[1].plot(dt, dPdtCO2_f,'--', label='dPdtfit')
lns = ln1 + ln2
lbs = [l.get_label() for l in lns]
ax[1].set_xlabel('Time [min]')
ax[1].set_ylabel('dPdt CO$_2$ [Pa/s]')
ax[0].yaxis.set_major_locator(plt.MaxNLocator(5))
ax[1].yaxis.set_major_locator(plt.MaxNLocator(5))
ax[1].legend(lns, lbs, loc='upper center', ncol=6, bbox_transform=fig.transFigure,
             bbox_to_anchor=(0.5,0.1))
plt.subplots_adjust(bottom = 0.20)
if save:
    plt.savefig('BC_'+date+'_'+file_number+'.png',fmt='.png',dpi=300)
plt.show()
"""

