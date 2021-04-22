from testsync import *

N = 6
trials = 20

timesteps_per_cycle = 1500.
cycle_time = 15. # 15 "seconds"
num_cycles = 20

dt = cycle_time/timesteps_per_cycle
T = int(timesteps_per_cycle*num_cycles)
w = 2*pi/cycle_time




i=0

for vizVal in [True, False]:
    for Kdt in [0.01, 0.025, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 1.0]:
        print(i)
        K = Kdt/dt
        alldata, fname = runTrials(trials, N, K, T, w, dt, vizVal)
        makeplots(alldata, fname, N, T)
        i+=1
