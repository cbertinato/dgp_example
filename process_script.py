from datetime import datetime

from dgp.lib.gravity_ingestor import read_at1a
from dgp.lib.trajectory_ingestor import import_trajectory
from dgp.lib.etc import align_frames
from dgp.lib.transform.transform_graphs import AirbornePost
from dgp.lib.transform.filters import detrend


# import gravity
print('Importing gravity')
gravity_filepath = '/Users/chrisbert/Documents/Git/dgp_example/data/AN04_F1001_20171103_2127.dat'
gravity = read_at1a(gravity_filepath, interp=True)

# import trajectory
print('Importing trajectory')
trajectory_filepath = '/Users/chrisbert/Documents/Git/dgp_example/data/AN04_F1001_20171103_DGS-INS_FINAL_DGS.txt'
gps_fields = ['mdy', 'hms', 'lat', 'long', 'ortho_ht', 'ell_ht', 'num_stats', 'pdop']
trajectory = import_trajectory(trajectory_filepath,
                               columns=gps_fields, skiprows=1, timeformat='hms')

# ROSETTA 3, F1001
# 11/3/2017
k_factor = 1.0737027
first_static = 14555.4
second_static = 14554.9
tie_gravity = 980352

# L650
begin_line = datetime(2017, 11, 4, 0, 27)
end_line = datetime(2017, 11, 4, 1, 45)

# pre-processing prep
gravity = gravity[(begin_line <= gravity.index) & (gravity.index <= end_line)]
trajectory = trajectory[(begin_line <= trajectory.index) & (trajectory.index <= end_line)]

# align gravity and trajectory frames
gravity, trajectory = align_frames(gravity, trajectory)

# adjust for crossing the prime meridian
trajectory['long'] = trajectory['long'].where(trajectory['long'] > 0, trajectory['long'] + 360)

# dedrift
gravity['gravity'] = detrend(gravity['gravity'], first_static, second_static)

# adjust to absolute
offset = tie_gravity - k_factor * first_static
gravity['gravity'] += offset

# def compute_static(begin, end):
#     return gravity[(begin < gravity.index) & (gravity.index < end)]['gravity'].mean()

# statics
# begin_first_static = datetime(2016, 8, 10, 19, 57)
# end_first_static = datetime(2016, 8, 10, 20, 8)
# first_static = compute_static(begin_first_static, end_first_static)
#
# begin_second_static = datetime(2016, 8, 10, 21, 7)
# end_second_static = datetime(2016, 8, 10, 21, 17)
# second_static = compute_static(begin_second_static, end_second_static)

print('Processing')
g = AirbornePost(trajectory, gravity, begin_static=first_static,
                 end_static=second_static)
results = g.execute()
