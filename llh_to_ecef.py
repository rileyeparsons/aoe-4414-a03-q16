# llh_to_ecef.py

# Usage: python3 llh_to_ecef.py lat_deg lon_deg hae_km 
# Converting from lat/long/height to ECEF positions

# Parameters:
#  lat_deg : int | float | str
#   Latitude position in degrees
#  lon_deg : int | float | str
#   Longiutde position in degrees
#  hae_km : int | float | str
#   Height above sea level in kilometers

# Output:
#  r_x_km : float
#   i position of 3D position vector
#  r_y_km : float
#   j position of 3D position vector
#  r_z_km
#   k position of 3D position vector

# Written by Riley Parsons

import sys
import math

# "constants"
R_E_KM = 6378.1363
E_E = 0.081819221456

# helper functions
def calc_c_E(r_E, e_E, lat_deg):
  """
  Calculates C_E based on the ellipsoid
  """
  return (r_E)/(math.sqrt(1 - (e_E**2*math.sin(math.radians(lat_deg))**2)))

def calc_s_E(r_E, e_E, lat_deg):
  """
  Calculates S_E based on the ellipsoid
  """
  return (r_E*(1-e_E**2))/(math.sqrt(1 - (e_E**2*math.sin(math.radians(lat_deg))**2)))

def calc_r_i(c_E, lat_deg, lon_deg, hae_km):
  """
  Calculates i component of position vector based on lat/lon/height and ellipsoid values 
  """
  return (c_E + hae_km)*math.cos(math.radians(lat_deg))*math.cos(math.radians(lon_deg))

def calc_r_j(c_E, lat_deg, lon_deg, hae_km):
  """
  Calculates j component of position vector based on lat/lon/height and ellipsoid values
  """
  return (c_E + hae_km)*math.cos(math.radians(lat_deg))*math.sin(math.radians(lon_deg))

def calc_r_k(s_E, lat_deg, hae_km):
  """
  Calculates k component of position vector based on lat/lon/height and ellipsoid values
  """
  return (s_E + hae_km)*math.sin(math.radians(lat_deg))

# main function
def llh_to_ecef(lat_deg, lon_deg, hae_km, out=False):
  """
  Converts lat/lon/height to ECEF coordinates and prints x, y, z positions
  """
  if(lat_deg == None or lon_deg == None or hae_km == None):
    print('Please check input arguments, one or more cannot be resolved.')

  c_E = calc_c_E(R_E_KM, E_E, lat_deg)
  s_E = calc_s_E(R_E_KM, E_E, lat_deg)
  
  r_x_km = calc_r_i(c_E, lat_deg, lon_deg, hae_km)
  r_y_km = calc_r_j(c_E, lat_deg, lon_deg, hae_km)
  r_z_km = calc_r_k(s_E, lat_deg, hae_km)
  if(out):
    print(f"{round(r_x_km, 6)}\n{round(r_y_km, 6)}\n{round(r_z_km, 6)}" )
  return([r_x_km, r_y_km, r_z_km])

# write script below this line
if __name__ == '__main__':
  # initialize script arguments
  lat_deg = None
  lon_deg = None
  hae_km = None

  # parse script arguments
  if len(sys.argv)==4:
    lat_deg = float(sys.argv[1])
    lon_deg = float(sys.argv[2])
    hae_km = float(sys.argv[3])
  else:
    print('Usage: python3 lat_deg lon_deg hae_km')
    exit()

  llh_to_ecef(lat_deg, lon_deg, hae_km, out=True)