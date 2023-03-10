# uavsar-validation

This is a research repository comparing UAVSAR L-band InSAR images against snow depth observations over the Sawtooth Mountains of Idaho.

## Workplan

- [ ] Download data
    - [x] Download UAVSAR unwrapped phase, wrapped phase, coherence, and incidence angles to netcdfs.
    - [x] Download Lidar datasets for Banner Summit (QSI), Dry Creek (QSI and maybe helicopter), Mores Creek (QSI).
    - [x] Download SnowEx pits, probing, other in-situ observations to pandas dataframe
    - [x] Download snotel observations of flight dates for all snotel sites
    - [x] Download SNOWMODEL data

- [ ] Prepare UAVSAR
    - [x] Run phase, inc -> SWE change using in-situ observations
    - [ ] Sum seasonal SWE for time series
    - [x] Add UAVSAR snow deltas to in-situ dataset

- [ ] In-situ compare
    - [x] Compare r2, rmse of all in-situ change vs UAVSAR SD delta
    - [ ] Compare r2, rmse for individual types of observations
    - [ ] Create time series vs snotel sites of UAVSAR changes vs snotel changes
    - [ ] Compare r2, rmse for in-situ changes binned by coherence, snow depth, trees
    - [ ] r2 and rmse for other insitu probed depths independent of setting phase

- [ ] Model compare
    - [x] Compare r2, rmse of all model observations (100 m) vs UAVSAR SD delta
    - [ ] Compare r2, rmse for binned SD classes
    - [ ] Compare r2, rmse for binned vegetation classes
    - [ ] Compare r2, rmse for binned wetness classes
    - [ ] Compare r2, rmse binned by coherence

- [ ] Lidar compare
    - [ ] Compare r2, rmse of summed SWE vs lidar for each location
    - [ ] Compare r2 of UAVSAR sd delta vs snotel SD - table with snotel SD change
    - [ ] plot of r2 vs binned slope, aspect, tree %
    - [ ] check covariance of independent datasets

- [ ] Ancillary figures
    - [x] Figure showing UAVSAR flight box, insitu sites, lidar flight boxes
    - [ ] Met summary figure for each study/lidar site's met data

- [ ] Writing - rough draft
    - [x] introduction
    - [x] methods
    - [ ] results
    - [ ] discussion
    - [ ] conclusion

- [ ] Writing - polished draft
    - [ ] introduction
    - [ ] methods
    - [ ] results
    - [ ] discussion
    - [ ] conclusion
