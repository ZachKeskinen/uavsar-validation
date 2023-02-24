import sys
import os
from os.path import basename, exists, expanduser, join
import shutil
import asf_search as asf
import pandas as pd
import xarray as xr
import rioxarray as rxa
from rioxarray.merge import merge_arrays
import shapely.geometry
from datetime import date
from tqdm import tqdm
from glob import glob

import sys
from nsidc import cmr_download, cmr_search

import logging
log = logging.getLogger(__name__)

def download_dem(out_dir = './tmp'):
    """
    Function to download snow-free DEMs to outdir
    https://nsidc.org/data/snex20_qsi_dem/versions/1
    Args:
    out_dir: directory to save lidar veg height tifs to
    Returns:
    None
    """
    os.makedirs(out_dir, exist_ok = True)
    old_cd = os.getcwd()
    os.chdir(out_dir)

    short_name = 'SNEX20_QSI_DEM'
    version = '1'
    time_start = '2021-09-16T00:00:00Z'
    time_end = '2021-09-21T23:59:59Z'
    bounding_box = '-117.07,41.3,-113.85,44.35'
    polygon = ''
    filename_filter = ''
    url_list = []
        
    quiet = False
    force = False

    try:
        if not url_list:
            url_list = cmr_search(short_name, version, time_start, time_end,
                                    bounding_box=bounding_box, polygon=polygon,
                                    filename_filter=filename_filter, quiet=quiet)

        cmr_download(url_list, force=force, quiet=quiet)
    except KeyboardInterrupt:
        quit()

    os.chdir(old_cd)

def download_snow_depth(out_dir = './tmp'):
    """
    Function to download snow depth files to outdir.
    https://nsidc.org/data/snex20_qsi_sd/versions/1
    Args:
    out_dir: directory to save lidar veg height tifs to
    Returns:
    None
    """

    os.makedirs(out_dir, exist_ok = True)
    old_cd = os.getcwd()
    os.chdir(out_dir)

    short_name = 'SNEX20_QSI_SD'
    version = '1'
    time_start = '2020-02-09T00:00:00Z'
    time_end = '2021-03-20T23:59:59Z'
    bounding_box = '-117.07,41.3,-113.85,44.35'
    polygon = ''
    filename_filter = ''
    url_list = []
    
    quiet = False
    force = False

    try:
        if not url_list:
            url_list = cmr_search(short_name, version, time_start, time_end,
                                    bounding_box=bounding_box, polygon=polygon,
                                    filename_filter=filename_filter, quiet=quiet)

        cmr_download(url_list, force=force, quiet=quiet)
    except KeyboardInterrupt:
        quit()
    
    os.chdir(old_cd)

def download_veg_height(out_dir = './tmp'):
    """
    Function to download vegation height files to outdir
    https://nsidc.org/data/snex20_qsi_vh/versions/1
    Args:
    out_dir: directory to save lidar veg height tifs to
    Returns:
    None
    """

    os.makedirs(out_dir, exist_ok = True)
    old_cd = os.getcwd()
    os.chdir(out_dir)

    short_name = 'SNEX20_QSI_VH'
    version = '1'
    time_start = '2020-02-01T00:00:00Z'
    time_end = '2021-03-20T23:59:59Z'
    bounding_box = '-117.07,41.3,-113.85,44.35'
    polygon = ''
    filename_filter = ''
    url_list = []
    
    quiet = False
    force = False

    try:
        if not url_list:
            url_list = cmr_search(short_name, version, time_start, time_end,
                                    bounding_box=bounding_box, polygon=polygon,
                                    filename_filter=filename_filter, quiet=quiet)

        cmr_download(url_list, force=force, quiet=quiet)
    except KeyboardInterrupt:
        quit()
    
    os.chdir(old_cd)

def make_site_ds(site: str, lidar_dir: str) -> xr.Dataset:
    """
    Makes a dataset of snow depth, veg height, and DEM for a specific site abbreviation
    in the lidar directory. Returns it reprojected to EPSG4326.
    Args:
    site: Site abbreviation to search for
    lidar_dir: Direction of lidar tiffs
    Returns:
    dataset: xarray dataset of dem, sd, vh for site
    """

    dataset = xr.Dataset()

    for img_type in ['SD', 'VH', 'DEM']:
        files = glob(join(lidar_dir, f'*_{img_type}_*_{site}_*.tif'))
        assert files, f"No files found for {img_type} at {site}"
        
        imgs = []
        for f in files:

            date = pd.to_datetime(basename(f).split('_')[-2])

            img = rxa.open_rasterio(f)

            img = img.squeeze(dim = 'band')
            
            img = img.expand_dims(time = [date])

            imgs.append(img)
    
        dataset['lidar-' + img_type.lower()] = xr.concat(imgs, dim = 'time')

    dataset = dataset.rio.reproject('EPSG:4326')
    
    return dataset

if __name__ == '__main__':

    out_dir = '/bsuhome/zacharykeskinen/scratch/data/uavsar/lidar/idaho'
    download_dem(out_dir)
    download_snow_depth(out_dir)
    download_veg_height(out_dir)


    sites = {'USIDBS': 'Banner', 'USIDDC': 'Dry_Creek', 'USIDMC': 'Mores'}

    for site, site_name in sites.items():

        out_nc = join('/bsuhome/zacharykeskinen/scratch/data/uavsar/ncs/lidar', f'{site_name}.nc')

        if exists(out_nc):
            print(f'Outfile {out_nc} exists already.')
            continue

        print(''.center(40, '-'))
        print(f'Starting {site_name}')

        lidar_ds = make_site_ds(site, lidar_dir = out_dir)

        lidar_ds = lidar_ds.where(lidar_ds < 1000).where(lidar_ds > -1000)

        lidar_ds.attrs['site'] = site_name
        lidar_ds.attrs['site_abbrev'] = site

        try:
            lidar_ds.to_netcdf(out_nc)
        except:
            print('Unable to create netcdf4 for {site_name}')
