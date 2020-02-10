#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import pdb

d = 5.9   #[cm]
R = 8.314 #[P m3 K-1 mol-1]

def Hcp(T, var):
    T = T + 273.15
    if 'CH4' in var:
        H = 1.4E-5 # mol/m3/Pa
        lndHdT = 1750
    elif 'CO2' in var:
        H = 3.3E-4 # mol/m3/Pa
        lndHdT = 2392.86
    Hcp = H*np.exp(lndHdT*(1/T-1/298.15)) # mol/m3/Pa
    return Hcp

def dcon_dt(data, varname, dt, hw, ha, T):
    """ Caculate dC/dt adjusting a linear fit every dt min to the concentrations
    in (Pa).
    """
    data = data[varname].values
    time = np.arange(0,len(data))
    dcdt = []
    for i in range(len(data[::int(dt*60)])):
        p = np.polyfit(time[i*int(dt*60):(i+1)*int(dt*60)],data[i*int(dt*60):(i+1)*int(60*dt)],1) #[Pa/s]
        dcdt.append(p[0])#*(a+b*q)/(b*R*Tk*a)*1000*24*60*60)
    dcdt = np.array(dcdt)
    return dcdt, time[::int(dt*60)]


def sed_flux(data, varname, t, hw, ha, T):
    """
    Caluculate air (Fa) and sediment (Fs) fluxes with the last X minutes of
    data.
    data = DataFrame
    varname = varname
    t = time in minutes
    hw = water height (cm)
    ha = air height (cm)
    d = tube diameter (cm)
    T = temperature (oC)

    return Fs and Fa in (mmol/m2/d), p are the fit values and time in secods (for plotting)
    """
    A = np.pi*(d/2./100)**2
    Va = ha/100.*A
    Tk = 273.15 + T
    Vw = hw/100.*A
    sec = t*60 # 10 min
    time = np.arange(0,sec)
    p = np.polyfit(time,data[varname][-sec:],1) #Pa/s
    F = p[0]*Va/(R*T)/A  #[mol/m2/s]
    Fa = F*1000*24*60*60 #[mmol/m2/d]
    H = Hcp(T, varname)
    a = A/Vw
    b = A/Va
    q = H*R*Tk
    Fs = p[0]*(a+b*q)/(b*R*Tk*a)*1000*24*60*60
    return Fa, Fs, p, time

def foot_pos(lgrfile):
    with open(lgrfile) as z:
        i = 0
        foot = False
        for line in z:
            if line.startswith('-----B'):
                ib = i
                foot = True
            i+=1
        if foot:
            ifoot = i - ib
        else:
            ifoot = 0
    return ifoot

def pC_sol(t, varname, Fs, cw0, k, P0, T, hw, ha):
    """
    Partial pressure function chamber experiment
    t = time in seconds
    varname = CH4 or CO2
    Fs = sediment flux in (mol/m2/s)
    cw0 = initial water concentration (mol/m3)
    k = air-water transfer coeficient (m/s)
    P0 = gas partial pressure (Pa)
    """
    H = Hcp(T, varname)
    A = np.pi*(d/2./100.)**2 #[m2]
    Va = ha/100.*A  #[m3]
    Vw = hw/100.*A  #[m3]
    Tk = 273.15 + T #[Kelvin]
    a = A/Vw        #[1/m]
    b = A/Va        #[1/m]
    q = H*R*Tk    #[-]
    C0 = a+b*q      #[1/m]
    C1 = b*R*Tk
    return P0+C1/C0*(Fs*a*t-1./(k*C0)*(Fs*a-k*C0*(cw0-P0*H))*(1-np.exp(-k*C0*t)))

def FdPdt(t, varname, Fs, cw0, k, P0, T, hw, ha):
    """
    Change of partial pressure in time
    t = time in seconds
    varname = CH4 or CO2
    Fs = sediment flux in (mol/m2/s)
    cw0 = initial water concentration (mol/m3)
    k= air-water transfer coefficient (m/s)
    P0 = initial gas partial pressure (Pa)
    """
    H = Hcp(T, varname)
    A = np.pi*(d/2./100.)**2
    Va = ha/100.*A
    Vw = hw/100.*A
    Tk = 273.15 + T
    a = A/Vw #[1/m]
    b = A/Va #[1/m]
    q = H*R*Tk #[-]
    C0 = a+b*q #[1/m]
    C1 = b*R*Tk #[Pa m2 mol-1]
    return C1/C0*(Fs*a - (Fs*a - k*C0*(cw0 - H*P0))*np.exp(-k*C0*t))

def pCsol(t,m1,m2,m3,m4):
    return m1 + m2*t + m3*(np.exp(-m4*t)-1)

def Fs(t, varname, dPdt, cw0, k, P0, T, hw, ha):

    H = Hcp(T, varname)
    A = np.pi*(d/2./100.)**2
    Va = ha/100.*A
    Vw = hw/100.*A
    Tk = 273.15 + T
    a = A/Vw #[1/m]
    b = A/Va #[1/m]
    q = H*R*Tk #[-]
    C0 = a+b*q #[1/m]
    C1 = b*R*Tk #[Pa m2 mol-1]

    Fs = (C0/C1*dPdt + C0*k*(cw0 - H*P0)*np.exp(-k*C0*t))/(a*(1-np.exp(-C0*k*t)))
    return Fs

def Cw(dPdt, P, k, varname, dt, hw, ha, T):
    """Water concentration in time
    """

    H = Hcp(T, varname)
    A = np.pi*(d/2./100.)**2
    Va = ha/100.*A
    Vw = hw/100.*A
    Tk = 273.15 + T

    Cw = Va/(R*Tk)*dPdt /(k*A) + H*P[::int(dt*60)]
    return Cw

def Fs_massbalance(Cw0, Cwf, Px0, Pxf, hw, ha, t_start, t_end, T):
    if Cwf < 0:
        return np.NAN, np.NAN
    else:
        Vw = np.pi*(5.9/100/2.)**2*hw/100. # (m3) Volume Water
        Va = np.pi*(5.9/100/2.)**2*ha/100. # (m3) Volume Air
        dt = pd.Timedelta(t_end - t_start, unit='s').total_seconds() # Time in sec
        dCw_dt = (Cwf-Cw0)/1000*Vw/dt
        dCa_dt = (Pxf-Px0)/dt*Va/(8.314*(T + 273.15))
        Fs_MB = (dCw_dt + dCa_dt)/(np.pi*(5.9/100/2.)**2)*86400*1000
        return Fs_MB, Cwf
