import yaml
import numpy as np
import xarray as xr
from utils import open_config, open_dataset

def hybrid_to_pressure(model):
    """
    Converts atmosphere_hybrid_sigma_pressure_coordinate to pressure and 
    returns full array of pressures with positive being "up".
    
    Inputs:
    model (string): model name
    
    Outputs:
    pm (numpy ndarray): pressure at every time, lev, lat and lon
    
    """
    p00 = 100000.0  #reference pressure in Pa
    ps_files = open_config("PS")
    ps_data = open_dataset(ps_files, model)
    
    if model == 'cam-se':
        pm = np.zeros((ps_data.time.shape[0], ps_data.lev.shape[0], 
                   ps_data.lat.shape[0], ps_data.lon.shape[0]))
        ps = ps_data.PS.values        
        hyam = ps_data.hyam.values    #get values of coefficients
        hybm = ps_data.hybm.values
        
        for i in range(pm.shape[0]):
            for j in range(pm.shape[1]):
                pm[:,j,:,:] = hyam[j]*p00+hybm[j]*ps[i,:,:]  #convert pressure array
    
    if model == 'acme-a':
        u_files = open_config("U")
        u_data = open_dataset(u_files, model)
        pm = np.zeros((u_data.time.shape[0], u_data.lev.shape[0], 
                   u_data.lat.shape[0], u_data.lon.shape[0]))
        ps = ps_data.ps.values
        coeff_data = open_dataset(ps_files, 'cam-se')  #use cam values because no A or B given
        hyam = coeff_data.hyam.values
        hybm = coeff_data.hybm.values
        
        for i in range(pm.shape[0]):
            for j in range(pm.shape[1]):
                pm[:,j,:,:] = hyam[j]*p00+hybm[j]*ps[i,:,:] #convert pressure array 
                
    return pm

def pressure_to_height(model):
    """
    Converts pressure to height using the hypsometric equation.
    
    Inputs:
    model (string): model name
    
    Outputs:
    z (numpy ndarray): height at every time, lev, lat, and lon
    
    """
    g = 9.80616     #acceleration due to gravity
    Rd = 287.0      #gas constant for dry air
    Mv = 0.608      #constant for virtual temperature conversion
    Ts = 302.15     #prescribed surface temperature
    
    model_conf = open_config("models")
    t_files = open_config("T")             #get temperature files
    t_data = open_dataset(t_files, model)
    q_files = open_config("Q")             #get specific humidity files
    q_data = open_dataset(q_files, model)
    ps_files = open_config("PS")           #open surface pressure data
    ps_data = open_dataset(ps_files, model)
    
    if model_conf[model]['levels'] == 'hybrid': #convert pressure array if model has hybrid coords
        P = hybrid_to_pressure(model)
        T = t_data.T.values
        Q = q_data.Q.values   
        
        if model == 'acme-a':
            PS = ps_data.ps.values
        else:
            PS = ps_data.PS.values
        
    else:
        p_files = open_config("P")
        p_data = open_dataset(p_files, model)
        P = p_data.P.values        #pressure
        PS = ps_data.PS.values     #surface pressure
        Q = q_data.Q.values        #specific humidity
        T = t_data.T.values        #temperature
    
    #use hypsometric equation to convert pressures to height
    
    if model == 'dynamico': #dyamico increases in the "up" direction unlike its metadata
        Z = np.zeros((t_data.time_counter.shape[0], t_data.lev.shape[0], 
                      t_data.lat.shape[0], t_data.lon.shape[0]))
        for i in range(Z.shape[0]):
            for j in range(Z.shape[1]): #loop up to outut heights with increase in "up" direction
                if j == 0:               
                    Ti = ((Ts+T[i,j,:,:])/2.0)*(1+Mv*Q[i,j,:,:])  #calculate mean virtual temp, take avg of temp at surface and first level
                    Z[i,j,:,:] = (Rd/g)*Ti*np.log(PS[i,:,:]/P[i,j,:,:])  #hypsometric equation, convert to height
                else:
                    #calculate mean virtual temp, take avg of temp of temp at current and previous levels 
                    Ti = ((T[i,j,:,:]+T[i,j-1,:,:])/2.0)*(1+Mv*(Q[i,j,:,:]+Q[i,j-1,:,:])/2.0)
                    Z[i,j,:,:] = Z[i,j-1,:,:]+(Rd/g)*Ti*np.log(P[i,j-1,:,:]/P[i,j,:,:])   #hypsometric equation, convert to height
    else:
        if model == 'fv3_dzlow':
            Z = np.zeros((t_data.time.shape[0], t_data.pfull.shape[0], 
                          t_data.lat.shape[0], t_data.lon.shape[0]))
        else:
            Z = np.zeros((t_data.time.shape[0], t_data.lev.shape[0], 
                          t_data.lat.shape[0], t_data.lon.shape[0]))
        for i in range(Z.shape[0]):
            for j in range(Z.shape[1]-1, -1, -1):  #loop down to outut heights with increase in "up" direction
                if j == Z.shape[1]-1:
                    Ti = ((Ts+T[i,j,:,:])/2.0)*(1+Mv*Q[i,j,:,:]) #calculate mean virtual temp, take avg of temp at surface and first level
                    Z[i,j,:,:] = (Rd/g)*Ti*np.log(PS[i,:,:]/P[i,j,:,:]) #hypsometric equation, convert to height
                else:
                    #calculate mean virtual temp, take avg of temp of temp at current and previous levels 
                    Ti = ((T[i,j,:,:]+T[i,j+1,:,:])/2.0)*(1+Mv*(Q[i,j,:,:]+Q[i,j+1,:,:])/2.0)
                    Z[i,j,:,:] = Z[i,j+1,:,:]+(Rd/g)*Ti*np.log(P[i,j+1,:,:]/P[i,j,:,:])  #hypsometric equation, convert to height
    
    return Z