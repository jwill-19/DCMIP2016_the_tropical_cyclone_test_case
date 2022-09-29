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
        hyam = ps_data.hyam.values
        hybm = ps_data.hybm.values
        
        for i in range(pm.shape[0]):
            for j in range(pm.shape[1]):
                pm[:,j,:,:] = hyam[j]*p00+hybm[j]*ps[i,:,:]
    
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
                pm[:,j,:,:] = hyam[j]*p00+hybm[j]*ps[i,:,:]
        
    if model == 'gem':
        u_files = open_config("U")
        u_data = open_dataset(u_files, model)
        pm = np.zeros((u_data.time.shape[0], u_data.lev.shape[0], 
                   u_data.lat.shape[0], u_data.lon.shape[0]))
        ps = ps_data.PS.values
        hyam = u_data.hyam.values
        hybm = u_data.hybm.values
        
        for i in range(pm.shape[0]):
            for j in range(pm.shape[1]):
                pm[:,j,:,:] = (1/100.0)*np.exp(hyam[j]+hybm[j]*np.log(ps[i,:,:]/p00))
                
    return pm

def pressure_to_height(model):
    """
    Converts pressure to height using the hypsometric equation.
    
    Inputs:
    model (string): model name
    
    Outputs:
    z (numpy ndarray): height at every time, lev, lat, and lon
    
    """
    g = 9.80616
    Rd = 287.0
    Mv = 0.608
    
    model_conf = open_config("models")
    t_files = open_config("T")
    t_data = open_dataset(t_files, model)
    q_files = open_config("Q")
    q_data = open_dataset(q_files, model)
    ps_files = open_config("PS")
    ps_data = open_dataset(ps_files, model)
    
    if model_conf[model]['levels'] == 'hybrid':
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
        P = p_data.P.values 
        PS = ps_data.PS.values 
        Q = q_data.Q.values
        T = t_data.T.values
    
    if model == 'dynamico':
        Z = np.zeros((t_data.time_counter.shape[0], t_data.lev.shape[0], t_data.lat.shape[0], t_data.lon.shape[0]))
        for i in range(Z.shape[0]):
            for j in range(Z.shape[1]):
                if j == 0:
                    Z[i,j,:,:] = (1/g)*Rd*T[i,j,:,:]*(1+Mv*Q[i,j,:,:])*(1/2.0)*(np.log(P[i,j,:,:])-np.log(PS[i,:,:]))
                else:
                    Z[i,j,:,:] = Z[i,j-1,:,:]+(1/g)*Rd*T[i,j,:,:]*(1+Mv*Q[i,j,:,:])*np.log(P[i,j-1,:,:]/P[i,j,:,:])
    else:
        if model == 'fv3_dzlow':
            Z = np.zeros((t_data.time.shape[0], t_data.pfull.shape[0], t_data.lat.shape[0], t_data.lon.shape[0]))
        else:
            Z = np.zeros((t_data.time.shape[0], t_data.lev.shape[0], t_data.lat.shape[0], t_data.lon.shape[0]))
        for i in range(Z.shape[0]):
            for j in range(Z.shape[1]-1, -1, -1):
                if j == Z.shape[1]-1:
                    Z[i,j,:,:] = (1/g)*Rd*T[i,j,:,:]*(1+Mv*Q[i,j,:,:])*(1/2.0)*(np.log(P[i,j,:,:])-np.log(PS[i,:,:]))
                else:
                    Z[i,j,:,:] = Z[i,j+1,:,:]+(1/g)*Rd*T[i,j,:,:]*(1+Mv*Q[i,j,:,:])*np.log(P[i,j+1,:,:]/P[i,j,:,:])
    
    return Z