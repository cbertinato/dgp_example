import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

from dgp.lib.gravity_ingestor import read_at1a
from dgp.lib.trajectory_ingestor import import_trajectory
from dgp.lib.etc import align_frames

# import gravity
print('Importing gravity')
# gravity_filepath = ('/Users/chrisbert/Documents/Projects/NASA-OIB/Data/F2001/DGS'
#                     '/OIB-P3_20170322_F2001_DGS_100600.dat')
gravity_filepath = '/Users/chrisbert/Documents/Git/dgp_example/data/AN04_F1001_20171103_2127.dat'
gravity = read_at1a(gravity_filepath, interp=True)

# import trajectory
print('Importing trajectory')
# trajectory_filepath = ('/Users/chrisbert/Documents/Projects/NASA-OIB/Data/F2001/DGS-INS'
#                        '/OIB-P3_20170322_F2001_DGS-INS_RAPID_DGS.txt')
trajectory_filepath = '/Users/chrisbert/Documents/Git/dgp_example/data/AN04_F1001_20171103_DGS-INS_FINAL_DGS.txt'
gps_fields = ['mdy', 'hms', 'lat', 'long', 'ortho_ht', 'ell_ht', 'num_stats', 'pdop']
trajectory = import_trajectory(trajectory_filepath,
                               columns=gps_fields, skiprows=1, timeformat='hms')

# align gravity and trajectory frames
gravity, trajectory = align_frames(gravity, trajectory)

fig = plt.figure()
fig.tight_layout()
ax1 = fig.add_subplot(4,1,1)
ax1.plot(gravity['gravity'])
ax1.grid()
ax1.get_xaxis().set_major_formatter(DateFormatter('%H:%M:%S'))
ax1.set_ylabel('raw gravity')

ax2 = fig.add_subplot(4,1,2, sharex=ax1)
ax2.plot(gravity['cross_accel'])
ax2.grid()
ax2.get_xaxis().set_major_formatter(DateFormatter('%H:%M:%S'))
ax2.set_ylabel('cross accel')

ax3 = fig.add_subplot(4,1,3, sharex=ax1)
ax3.plot(gravity['clamp'])
ax3.grid()
ax3.get_xaxis().set_major_formatter(DateFormatter('%H:%M:%S'))
ax3.set_ylabel('clamp')

ax4 = fig.add_subplot(4,1,4, sharex=ax1)
ax4.plot(trajectory['ell_ht'])
ax4.grid()
ax4.get_xaxis().set_major_formatter(DateFormatter('%H:%M:%S'))
ax4.set_ylabel('Ell height')

fig.show()
