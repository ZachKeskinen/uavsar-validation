from scipy.interpolate import griddata
import numpy as np
import pandas as pd
import xarray as xr
from tqdm import tqdm

model = xr.open_dataset('/bsuhome/zacharykeskinen/scratch/data/uavsar/ncs/model/model.nc')
model = model.rename({'east_west': 'x', 'south_north': 'y'})
model = model.rio.write_crs('EPSG:4326')

xg, yg = np.meshgrid(np.linspace(model.lon.min(), model.lon.max(), model.x.size), np.linspace(model.lat.min(), model.lat.max(), model.y.size))

points = (model.lon.data.ravel(), model.lat.data.ravel())

ds = xr.Dataset()

for var in model.data_vars:
    print(var)
    das = []
    for time in tqdm(model.time):
        time = pd.to_datetime(time.data)
        data = griddata(points, model[var].sel(time = time).data.ravel(), (xg, yg), method = 'cubic', fill_value = np.nan)
        
        dA = xr.DataArray(data = np.expand_dims(data,2),
                          dims = ["y" ,"x", "time"],
                          coords = {
            "y": (["y"], np.linspace(model.lat.min(), model.lat.max(), model.y.size)),
            "x": (["x"] ,np.linspace(model.lon.min(), model.lon.max(), model.x.size)),
            "time": [time]})

        das.append(dA)
    ds[var] = xr.concat(das, dim = 'time')
    
import rioxarray as rxa
ds = ds.rio.write_crs('epsg:4326')
ds = ds.transpose('time', 'y', 'x')
ds.to_netcdf('/bsuhome/zacharykeskinen/scratch/data/uavsar/ncs/model/model.re.nc')