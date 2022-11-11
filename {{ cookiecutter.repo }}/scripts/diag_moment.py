import xarray
import numpy
import logging

import click
from pwrf.utils import xarray_utils
from pwrf.diag import moments

def calc_moment_reff(input_filename, mu=1):
    with xarray_utils.open_wrf_dataset(input_filename) as nc:
      ls = nc.L_S

      if hasattr(nc,"TRC03"):
        mom = moments.Moment(nc.TRC02,nc.TRC01,nc.TRC03)
      else:
        mom = moments.Moment(nc.TRC02,nc.TRC01,None,mu=mu)
    
      rv = mom.veffreff(means=lambda x: x.mean("west_east"))
      rm = nc.REFF_DUST.mean("west_east")
      if "VEFF_DUST" in nc:
          vm = nc.VEFF_DUST.mean("west_east")
      else:
          vm = 0.25
      tau = nc.TAU_OD.mean("west_east")
      nlif1 = nc.NLIF1.mean("west_east")
      dlif1 = nc.DLIF1.mean("west_east")

    data = dict(ls=ls
               ,veff=rv["veff"]
               ,reff=rv["reff"]
               ,mreff=rm
               ,mveff=vm
               ,tau=tau
               ,nlif1=nlif1
                #nlif2=nlif2,nlif3=nlif3,
               ,dlif1=dlif1
                #dlif2=dlif2,dlif3=dlif3
               )
    return xarray.Dataset(data)
               

    
@click.command()
@click.argument("input_filename")
@click.argument("output_filename")
def main(input_filename, output_filename):
    data = calc_moment_reff(input_filename)
    data.to_netcdf(output_filename, unlimited_dims=["Time"], mode="w")


if __name__=="__main__":
    main()
