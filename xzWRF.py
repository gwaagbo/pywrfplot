# -*- coding:utf-8 -*-
"""
@author: Geir Arne Waagbø
"""
import pyplot as plt
from numpy import arange

from pywrfplotParams import *
from pywrfplotUtils import *

def xzCloudPlot(nest,time,plotTemp=True,plotRH=False):
    nc = openWRF(nest)
    Nx,Ny,Nz,longitude,_lats,_dx,_dy,x_nr,y_nr = getDimensions(nc)
    
    heightground_x,heighthalf_xz = _getHeight(nc, time, Nx, -1, Nz, -1, y_nr)    
    print 'Model height: ' + str(heightground_x[x_nr])

    theta = nc.variables['T'][time,:,y_nr,:] + T_base 
    P = nc.variables['P'][time,:,y_nr,:] + nc.variables['PB'][time,:,y_nr,:] 
    T = theta*(P/P_bot)**kappa # Temperatur i halvflatene (Kelvin)
    rho = P/(R*T) #[kg/m3]

    qcloud_xz = 1000.0*nc.variables['QCLOUD'][time,:,y_nr,:]*rho # regner om til g/m3
    qrain_xz = 1000.0*nc.variables['QRAIN'][time,:,y_nr,:]*rho 
    qsnow_xz = 1000.0*nc.variables['QSNOW'][time,:,y_nr,:]*rho 
   
    plt.figure()
    plt.set_cmap(cmap_red)
    plt.axis([0,Nx-1,0.0,z_max])
    print u'Cloud water red, snow blue, rain green ($g/m^3$)'
    grid = np.reshape(np.tile(arange(Nx),Nz),(Nz,-1))
    plt.contourf(grid, heighthalf_xz, qcloud_xz, alpha=0.9,levels=xz_cloudwater_levels, cmap=cmap_red)#
    plt.colorbar()
    plt.contourf(grid, heighthalf_xz, qrain_xz, alpha=0.6,levels=xz_rain_levels, cmap=cmap_green)#
    plt.colorbar()
    plt.contourf(grid, heighthalf_xz, qsnow_xz, alpha=0.6,levels=xz_snow_levels,cmap=cmap_blue)# 
    plt.colorbar()

    if plotTemp:
        temp_int = arange(-80.0,50.0,2.0)
        cs = plt.contour(grid, heighthalf_xz, T-T_zero, temp_int,colors='black',linestyles='solid')#linewidths=4
        plt.clabel(cs, inline=1,  fmt='%1.0f', fontsize=12,colors='black')
    if plotRH:
        rh = _getRH(nc,time,-1,y_nr,T,P)
        rh_int = arange(90.,111.,5.)
        cs = plt.contour(grid, heighthalf_xz,rh , rh_int, colors='grey')
        plt.clabel(cs, inline=1,  fmt='%1.0f', fontsize=12, colors='grey')
    plt.plot(arange(Nx),heightground_x,color='black')
    plt.fill_between(arange(Nx),heightground_x,0,facecolor='lightgrey')
    plt.xticks(np.arange(0,Nx,8),np.round(longitude[Ny/2,::8], 1), fontsize='small')
    plt.yticks(np.arange(0,z_max,dz), fontsize='small')
    plt.xlabel('Lengdegrad')
    plt.ylabel(u'Høyde [m]')
    plt.show()
    plt.close()        

def yzCloudPlot(nest,time,plotTemp=True,plotRH=False):
    nc = openWRF(nest)
    Nx,Ny,Nz,_longs,latitude,_dx,_dy,x_nr,y_nr = getDimensions(nc)
    
    heightground_y,heighthalf_yz = _getHeight(nc, time, -1, Ny, Nz, x_nr,-1)    
    print 'Model height: ' + str(heightground_y[y_nr])

    theta = nc.variables['T'][time,:,:,x_nr] + T_base 
    P = nc.variables['P'][time,:,:,x_nr] + nc.variables['PB'][time,:,:,x_nr] 
    T = theta*(P/P_bot)**kappa # Temperatur i halvflatene (Kelvin)
    rho = P/(R*T) #[kg/m3]

    qcloud_yz = 1000.0*nc.variables['QCLOUD'][time,:,:,x_nr]*rho # regner om til g/m3
    qrain_yz = 1000.0*nc.variables['QRAIN'][time,:,:,x_nr]*rho 
    qsnow_yz = 1000.0*nc.variables['QSNOW'][time,:,:,x_nr]*rho 
   
    plt.figure()
    plt.set_cmap(cmap_red)
    plt.axis([0,Ny-1,0.0,z_max])
    print u'Cloud water red, snow blue, rain green ($g/m^3$)'
    grid = np.reshape(np.tile(arange(Ny),Nz),(Nz,-1))
    plt.contourf(grid, heighthalf_yz, qcloud_yz, alpha=0.9,levels=xz_cloudwater_levels, cmap=cmap_red)#
    plt.colorbar()
    plt.contourf(grid, heighthalf_yz, qrain_yz, alpha=0.6,levels=xz_rain_levels, cmap=cmap_green)#
    plt.colorbar()
    plt.contourf(grid, heighthalf_yz, qsnow_yz, alpha=0.6,levels=xz_snow_levels,cmap=cmap_blue)# 
    plt.colorbar()

    if plotTemp:
        cs = plt.contour(grid, heighthalf_yz, T-T_zero, temp_int,colors='black',linestyles='solid')#linewidths=4
        plt.clabel(cs, inline=1,  fmt='%1.0f', fontsize=12,colors='black')
    if plotRH:
        rh = _getRH(nc,time,x_nr,-1,T,P)
        rh_int = arange(90.,111.,5.)
        cs = plt.contour(grid, heighthalf_yz,rh , rh_int,colors='grey')
        plt.clabel(cs, inline=1,  fmt='%1.0f', fontsize=12,colors='grey')
    plt.plot(arange(Ny),heightground_y,color='black')
    plt.fill_between(arange(Ny),heightground_y,0,facecolor='lightgrey')
    plt.xticks(np.arange(0,Ny,8),np.round(latitude[::8,Nx/2], 1), fontsize='small')
    plt.yticks(np.arange(0,z_max,dz), fontsize='small')
    plt.xlabel('Breddegrad')
    plt.ylabel(u'Høyde [m]')
    plt.show()
    plt.close()        

def _getHeight(nc,time,Nx,Ny,Nz,x_nr,y_nr):
    # Calculate height above sea level for mass levels
    # NB! Either x_nr must be -1 or y_nr must be -1
    # Note: geopotential defined at full levels (w-levels)
    #       Must interpolate to find geopotential at half levels (u-levels)
    geopot = (nc.variables['PH'][time,0:Nz,y_nr,:] + nc.variables['PHB'][time,0:Nz,y_nr,:]) if y_nr!=-1 else \
             (nc.variables['PH'][time,0:Nz,:,x_nr] + nc.variables['PHB'][time,0:Nz,:,x_nr])
    mu = (nc.variables['MU'][time,y_nr,:]+nc.variables['MUB'][time,y_nr,:]) if y_nr!=-1 else \
         (nc.variables['MU'][time,:,x_nr]+nc.variables['MUB'][time,:,x_nr])
    znw = nc.variables['ZNW'][time,0:Nz] # full (w) levels
    znu = nc.variables['ZNU'][time,0:Nz] # half (u,mass) levels

    heighthalf = np.zeros((Nz,Nx if y_nr!=-1 else Ny))# height in meters
    for i in arange(Nx if y_nr!=-1 else Ny):
        pfull = mu[i]*znw+P_top
        phalf = mu[i]*znu+P_top
        for k in arange(Nz):
            heighthalf[k,i]=interp(geopot[:,i],pfull[:],phalf[k])/g
    heightground = geopot[0,:]/g
    return heightground,heighthalf

def _getRH(nc,time,x_nr,y_nr,T,P):
    es_w = es(T-T_zero) # metningstrykk (Pascal)
    qsat = eps*es_w/(P-0.378*es_w)
    #es_ice = es_w*(T/T_zero)**2.66
    #qsat_ice = eps*es_ice/(P-0.378*es_w)
    qvapor = nc.variables['QVAPOR'][time,:,y_nr,:] if y_nr!=-1 else nc.variables['QVAPOR'][time,:,:,x_nr]
    rh = 100.*qvapor*(1-qsat)/(qsat*(1-qvapor))
    #rh_ice = 100.*qvapor*(1-qsat_ice)/(qsat_ice*(1-qvapor))
    return rh
    
