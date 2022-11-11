import xarray
import numpy
import logging
import click
from pwrf.utils import xarray_utils

def test_calculation(input_filename):
  logging.info(f"calculation for {input_filename}")
  with xarray_utils.open_wrf_dataset(input_filename) as input:
      ls = nc.L_S
  return xarray.Dataset(dict(ls=ls))
 
@click.command()
@click.argument("input_filename")
@click.argument("output_filename")
def main(input_filename, output_filename):
    data = test_calculation(input_filename)
    data.to_netcdf(output_filename, unlimited_dims=["Time"], mode="w")


if __name__=="__main__":
    main()
