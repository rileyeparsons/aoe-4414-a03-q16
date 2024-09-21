# sez_to_ecef.py

# Usage: python3 sez_to_ecef.py o_lat_deg o_lon_deg o_hae_km s_km e_km z_km
# Converting from SEZ positions to ECEF positions

# Parameters: 
#  o_lat_deg : int | float | str
#   Latitude position in degrees
#  o_lon_deg : int | float | str
#   Longiutde position in degrees
#  o_hae_km : int | float | str
#   Height above sea level in kilometers
#  s_km : int | float | str
#   south component of SEZ vector in kilometers
#  e_km : int | float | str
#   east component of SEZ vector in kilometers
#  z_km : int | float | str
#   z component of SEZ vector in kilometers

# Output:
#  r_x_km : float
#   i position of 3D position vector
#  r_y_km : float
#   j position of 3D position vector
#  r_z_km
#   k position of 3D position vector

# Written by Riley Parsons
# test case: py sez_to_ecef.py 40.496 -80.246 0.37 0 1 0.3

import sys
import numpy as np
import llh_to_ecef as le

# "constants"
R_E_KM = 6378.1363
E_E = 0.081819221456

# helper functions
def form_sez(s_km, e_km, z_km):
  return np.array([s_km, e_km, z_km]).reshape(-1, 1)

def y_rotation(lat, r_sez : np.ndarray):
  y_rot = np.array([
      [np.sin(np.deg2rad(lat)), 0, np.cos(np.deg2rad(lat))], 
      [0, 1, 0],
      [-np.cos(np.deg2rad(lat)), 0, np.sin(np.deg2rad(lat))]
    ])
  return np.dot(y_rot, r_sez)

def z_rotation(long, y_rot):
  z_rot = np.array([
    [np.cos(np.deg2rad(long)), -np.sin(np.deg2rad(long)), 0],
    [np.sin(np.deg2rad(long)), np.cos(np.deg2rad(long)), 0],
    [0, 0, 1]
  ])
  return np.dot(z_rot, y_rot)

# main function
def sez_to_ecef(o_lat_deg, o_lon_deg, o_hae_km, s_km, e_km, z_km, out=False):
  """
  Converts lat/lon/height to ECEF coordinates and prints x, y, z positions
  """
  r_sez = form_sez(s_km, e_km, z_km)
  y_rot = y_rotation(o_lat_deg, r_sez)
  r_ecef_sez = z_rotation(o_lon_deg, y_rot)
  r_ecef_llh = le.llh_to_ecef(o_lat_deg, o_lon_deg, o_hae_km)
  if(type(r_ecef_llh) == list):
    r_ecef_llh = np.array(r_ecef_llh).reshape(-1, 1)
  r_ecef = r_ecef_sez + r_ecef_llh
  if(out):
    print(np.round(r_ecef, 3))
  
# write script below this line
if __name__ == '__main__':
  # initialize script arguments
  o_lat_deg = None
  o_lon_deg = None
  o_hae_km = None
  s_km = None
  e_km = None
  z_km = None

  # parse script arguments
  if len(sys.argv)==7:
    o_lat_deg = float(sys.argv[1])
    o_lon_deg = float(sys.argv[2])
    o_hae_km = float(sys.argv[3])
    s_km = float(sys.argv[4])
    e_km = float(sys.argv[5])
    z_km = float(sys.argv[6])
  else:
    print('Usage: 3 lat_deg lon_deg hae_km')
    exit()

  sez_to_ecef(o_lat_deg, o_lon_deg, o_hae_km, s_km, e_km, z_km, out=True)
