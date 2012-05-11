# -*- coding:utf-8 -*-
"""
@author Geir Arne Waagbø
@see http://code.google.com/p/pywrfplot/
"""
import pyplot as plt
from numpy import arange

from pywrfplotParams import *
from pywrfplotUtils import *

def tzCloudPlot(nest,plotMetar=False,offset=0):
    nc = openWRF(nest)
    Nx,Ny,Nz,_longs,_lats,_dx,_dy,x_nr,y_nr = getDimensions(nc)
    
    heightground_t, heighthalf_tz = _getHeight(nc, Nx, Ny, Nz, x_nr, y_nr)

    T_tz = np.zeros((Nz,Nt))
    qcloud_tz = np.zeros((Nz,Nt))
    qice_tz = np.zeros((Nz,Nt))
    qsnow_tz = np.zeros((Nz,Nt))
    qrain_tz = np.zeros((Nz,Nt))
    
    for t in arange(Nt):
        theta = nc.variables['T'][t,:,y_nr,x_nr] + T_base 
        P = nc.variables['P'][t,:,y_nr,x_nr] + nc.variables['PB'][t,:,y_nr,x_nr] 
        T_tz[:,t] = theta*(P/P_bot)**kappa # Temperatur i halvflatene (Kelvin)
        rho = P[:]/(R*T_tz[:,t]) # regner om til g/m3
        qcloud_tz[:,t] = 1000.0*nc.variables['QCLOUD'][t,:,y_nr,x_nr]*rho
        qice_tz[:,t] = 1000.0*nc.variables['QICE'][t,:,y_nr,x_nr]*rho
        qsnow_tz[:,t] = 1000.0*nc.variables['QSNOW'][t,:,y_nr,x_nr]*rho
        qrain_tz[:,t] = 1000.0*nc.variables['QRAIN'][t,:,y_nr,x_nr]*rho

    for s in [u'Snø','Regn']:
        plt.figure()
        plt.axis([-offset,Nt-1,0.0,z_max])
        grid = np.reshape(np.tile(arange(Nt),Nz),(Nz,-1))
        if (s==u"Snø"):
            var = qsnow_tz
            cm = cmap_blue
            levs = tz_snow_levels
        else:    
            var = qrain_tz
            cm = cmap_green
            levs = tz_rain_levels
        plt.contourf(grid, heighthalf_tz, qcloud_tz, alpha=0.9,levels=tz_cloudwater_levels, cmap=cmap_red)#
        plt.colorbar()
        plt.contourf(grid, heighthalf_tz, var, alpha=0.6,levels=levs, cmap=cm)#
        plt.colorbar()
        cs = plt.contour(grid, heighthalf_tz, T_tz-T_zero, temp_int,colors='black',linestyles='solid')
        plt.clabel(cs, inline=1,  fmt='%1.0f', fontsize=12,colors='black')
        plt.fill_between(arange(-offset,Nt),heightground_t[0],0,facecolor='lightgrey')
        if plotMetar:
            _metar()
        print s + ' ($g/m^3$)'
        plt.xlabel('Timer etter ' + date + 'T00:00Z')
        plt.ylabel(u'Høyde [m]')
        plt.yticks(np.arange(0,z_max,dz), fontsize='small')
        plt.show()
        plt.close()   
        
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.set_xlim(0,Nt-1)
    ax1.plot(np.sum(qcloud_tz,axis=0), color='black',label=u"skyvann")
    ax1.plot(np.sum(qsnow_tz,axis=0), color='green',label=u"snø")
    ax1.set_xlabel('Timer etter ' + date + 'T00:00Z')
    ax1.set_ylabel(u'Skyvann og snø ($g/m^2$)')
    ax2 = ax1.twinx()
    ax2.plot(np.sum(qice_tz,axis=0), color='blue',label="is")
    ax2.plot(np.sum(qrain_tz,axis=0), color='red',label="regn")
    ax2.set_ylabel('Regn og is ($g/m^2$)')
    ax1.set_xlim(0,Nt-1)
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.show()
    plt.close()   

def _getHeight(nc,Nx,Ny,Nz,x_nr,y_nr):
    # Calculate height above sea level for mass levels
    # Note: geopotential defined at full levels (w-levels)
    #       Must interpolate to find geopotential at half levels (u-levels)
    geopot = (nc.variables['PH'][:,0:Nz,y_nr,x_nr] + nc.variables['PHB'][:,0:Nz,y_nr,x_nr])
    mu = (nc.variables['MU'][:,y_nr,x_nr]+nc.variables['MUB'][:,y_nr,x_nr])
    znw = nc.variables['ZNW'][:,0:Nz] # full (w) levels
    znu = nc.variables['ZNU'][:,0:Nz] # half (u,mass) levels

    heighthalf = np.zeros((Nz,Nt))# height in meters
    for t in arange(Nt):
        pfull = mu[t]*znw[t,0:Nz]+P_top
        phalf = mu[t]*znu[t,0:Nz]+P_top
        for k in arange(Nz):
            heighthalf[k,t]=interp(geopot[t,:],pfull[:],phalf[k])/g
    heightground = geopot[:,0]/g
    return heightground,heighthalf


filename = 'metar-engm.txt'    
data = ['SG','-SG','SN','-SN','FZDZ','-FZDZ','FZRA','-FZRA']
fromday = 15

def _metar():
    dl = _metardata()
    min = -12.0
    for item in dl:
        itemnumber = (item[0]-fromday)*24 + item[1]
        type = item[2]
        if (type is not 'None'):
            plt.fill_between([itemnumber-1,itemnumber],[150,150],[0,0],facecolor=_itemcolor(type))

def _itemcolor(s):
    if (s=='-FZDZ' or s=='FZDZ'):
        return 'pink'
    if (s=='-FZRA'):
        return 'red'
    if (s=='FZRA'):
        return 'darkred'
    if (s=='SG' or s=='-SG'):
        return 'lightblue'
    if (s=='-SN'):
        return 'blue'
    if (s=='SN'):
        return 'darkblue'
     
def _metardata():
    datalist = list()
    f = open(filename,'r')
    s = f.readline()
    while (s is not ''):
        s = _strip(s)
        if (s is not ''):
            itemlist = list()
            t = s.split()
            itemlist.append(int(t[1][:2])) #day
            h = int(t[1][2:4]) #hour
            m = int(t[1][4:6])
            if (m >= 30):
                h = h+1
            itemlist.append(h) #hour
            j = 1
            if (_hasdata(s)):
                while (not _isdata(t[j])):
                    j = j+1
                itemlist.append(t[j])
            else:
                itemlist.append('None')    
            while (t[j][0] is not 'M'):
                j = j+1
            itemlist.append(-int(t[j][1:3]))        
            #print str(itemlist)
            datalist.append(itemlist)
        s = f.readline()    
    
    f.close()
    while True:
        item = datalist.pop()       
        if (item[0] >= fromday):
            datalist.append(item)
            break
    datalist.reverse()
    #print str(datalist)
    return datalist
    
def _strip(s):
    s = s.strip()
    index = s.find('TEMPO')
    if (index!=-1):
        s = s[0:index]
    return s
         
def _hasdata(s):
    for t in data:
        if (s.find(t)!=-1):
            return True  
    return False    

def _isdata(s):
    return s in data 
     
