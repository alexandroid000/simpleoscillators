from testsync import *

N = 3
trials = 3

cycle_time = 10. 
num_cycles = 20

dt = 0.05
timesteps_per_cycle = cycle_time/dt
T = int(timesteps_per_cycle*num_cycles)
print("T=", T)


i=0

for Kdt in [0.05*j for j in range(0,21)]:
    print("exp",i)
    print("KDT=",Kdt)
    K = Kdt/dt
    alldata, statedata, fname = runTrials(trials, N, K, T, dt)
    makeplots(alldata, statedata, fname, N, T)
    i+=1
