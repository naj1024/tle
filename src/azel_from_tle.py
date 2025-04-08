# Graph the az/el position of a geostationary satellite over a number of days
#

import datetime

from astropy.coordinates import EarthLocation
from astropy import time
from pycraf import satellite
import matplotlib.pyplot as plt
import numpy as np

# define observer location
location = EarthLocation(lon=-2.1, lat=51.8, height=100.0)

# create a SatelliteObserver instance
sat_obs = satellite.SatelliteObserver(location)

# A tle we are interested in
tle_string = '''INTELSAT 10-02          
1 28358U 04022A   24306.13806737  .00000008  00000+0  00000+0 0  9990
2 28358   0.0040 271.5751 0000423 334.5736 203.5135  1.00271606 74687'''

print(f"Location: {location.lat:.1f}, {location.lon:.1f}, {location.height:.0f}")
print(tle_string)

# variation of az/el over time
# from a particular day
date = datetime.datetime(year=2024, month=11, day=1, hour=13, minute=11, second=0)

# record the data in this
points = []

number_of_days = 5
print(f"Calculating over {number_of_days} days in 1 hour steps")
for day in range(number_of_days):
    # print(f"Calculating day {day}")
    for hour in range(24):
        date = date + datetime.timedelta(hours=1)
        obs_time = time.Time(date)

        # the angles
        az, el, dist = sat_obs.azel_from_sat(tle_string, obs_time)
        # print(f'{dt} az: {az:.4f}, el: {el:.4f}, dist :{dist:.4f}')
        points.append((az, el, dist))

# Extract the azimuth and elevation values
azimuths = [az.value for az, el, dist in points]
elevations = [el.value for az, el, dist in points]
distances = [dist.value for az, el, dist in points]

# what is the maximum deviation in degrees
max_az = np.max(azimuths)
min_az = np.min(azimuths)
print(f"Min az {min_az:.3f}deg, Max az {max_az:.3f}deg, diff {(max_az - min_az):.3f}deg")
max_el = np.max(elevations)
min_el = np.min(elevations)
print(f"Min el {min_el:.3f}deg, Max el {max_el:.3f}deg, diff {(max_el - min_el):.3f}deg")
max_ds = np.max(distances)
min_ds = np.min(distances)
print(f"Min dst {min_ds:.3f}km, Max dst {max_ds:.3f}kms, diff {(max_ds - min_ds):.3f}km")

# Create the plot
plt.figure(figsize=(8, 6))
plt.plot(azimuths, elevations, marker='o', linestyle='-')  # Line plot with points
plt.xlabel('Azimuth (degrees)')
plt.ylabel('Elevation (degrees)')
plt.title('Azimuth vs Elevation')
plt.grid(True)
plt.show()


