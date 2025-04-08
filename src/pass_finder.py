# Find passes above the horizon of a satellite, LEO
#

from skyfield.api import wgs84, EarthSatellite, load

ts = load.timescale()

# From/to dates
t0 = ts.utc(2025, 4, 8)
t1 = ts.utc(2025, 4, 9)

# TLE
tle_name = 'ISS (ZARYA)'
line1 = '1 25544U 98067A   25097.52056586  .00011719  00000-0  21806-3 0  9999'
line2 = '2 25544  51.6365 297.0255 0004979  19.0825 341.0349 15.49320680504205'

observer = wgs84.latlon(+51.8, -2.1, elevation_m=100)

satellite = EarthSatellite(line1, line2, tle_name, ts)

# show how we are configured
print("Observer :", observer)
print("Satellite:", satellite)
print(f"  {line1}")
print(f"  {line2}")

# get the pass data, horizon to horizon
t, events = satellite.find_events(observer, t0, t1, altitude_degrees=0.0)

# print the pass events out
if len(events) == 0:
    print(" - No passes")
else:
    # event types are 0,1,2
    event_names = 'Rise', 'Peak', 'Set '
    pass_count = 1
    for ti, event in zip(t, events):
        name = event_names[event]

        # get az, el, range and rate at this time
        difference = satellite - observer
        topo_centric = difference.at(ti)

        # Could use this for just el, az and range
        # el, az, slant_range = topo_centric.altaz()

        # frame_latlon_and_rates() allows us to calculate doppler as well
        el, az, slant_range, _, _, range_rate = topo_centric.frame_latlon_and_rates(observer)

        # Calculate doppler in Hz per MHz
        # doppler = f₀ - ((f₀(3e8)/(3e8 + range_rate))
        doppler = 1e6 - ((1e6 * 2.9979246e8) / (2.9979246e8 + 1000 * range_rate.km_per_s))

        if event == 0:
            print(f"Pass {pass_count}")
            pass_count += 1
        print(f"{name}"
              f"\t{ti.utc_strftime('%Y %b %d %H:%M:%S')} UTC"
              f"\tEl {abs(el.degrees):5.2f}"
              f"\tAz {az.degrees:5.2f}"
              f"\trange {slant_range.km:8.3f}km"
              f"\trate {range_rate.km_per_s:5.3f}km/s"
              f"\tdoppler {doppler:.3f}Hz/MHz")


