from math import pi
import matplotlib.pyplot as plt
import numpy as np
from copy import copy, deepcopy


def phase_distance(th1, th2):
    if th1 > th2:
        val = (th1 - th2) % (2*pi)
    else:
        val = (th2 - th1) % (2*pi)

    if val > pi:
        val = 2*pi - val

    return val


def runTrials(trials, N, K, T, w, dt, vizVal):

    Kdt = K*dt
    alldata = np.empty((trials,T,N))
    fname = "N"+str(N)+"_Kdt"+str(Kdt)+"_Nth"+str(vizVal)

    for trial in range(trials):

        states = np.zeros((2,N), dtype=bool)
        thetas = pi*np.random.rand(N)

        th_hist = np.zeros((T,N), dtype=float)
        th_hist[0] = copy(thetas)

        for t in range(1,T):

            for i in range(N): # todo randomize?
                n1 = (i-1) % N
                n2 = (i+1) % N

                th1 = th_hist[t-1][n1] 
                th2 = th_hist[t-1][n2] 

                # update i if either neighbor inflated
                if th1 > 0 and th1 < pi and states[0][n1] == False: # if new neighbor inflate
                    states[1][n1] = True
                    if states[0][i] == False: # current agent in rest state
                        if vizVal == True:
                            thetas[i] += K*phase_distance(thetas[i],th1)*dt # apply phase offset jump
                        else:
                            thetas[i] += K*thetas[i]*dt # apply phase offset jump

                if th1 != th2 and th2 > 0 and th2 < pi and states[0][n2] == False: # if new neighbor inflate
                    states[1][n2] = True
                    if states[0][i] == False: # current agent in rest state
                        if vizVal == True:
                            thetas[i] += K*phase_distance(thetas[i],th2)*dt # apply phase offset jump
                        else:
                            thetas[i] += K*thetas[i]*dt # apply phase offset jump
                

                thetas[i] += w*dt


                if thetas[i] > pi and states[0][i] == True:
                    states[1][i] = False

                if thetas[i] > 2*pi:
                    thetas[i] = thetas[i] % (2*pi)

            th_hist[t] = copy(thetas)
            states[0] = copy(states[1])

        alldata[trial] = deepcopy(th_hist)

    return alldata, fname



def order_param(ths, N, axis=None):
    return (1/N)*np.abs(np.sum(np.exp(ths*1j), axis=axis))

def makeplots(alldata, fname, N, T):
    #plot1 = plt.figure(1)
    #for i in range(N):
    #    plt.plot(range(T), th_hist[:,i])
    #plt.savefig(fname+"_trajectories.png",bbox_inches='tight')

    all_ops = np.array([order_param(ths, N, axis=1) for ths in alldata])
    #print(all_ops)

    avg_ops = np.average(all_ops, axis=0)
    #print("average:",avg_ops)
    std_ops = np.std(all_ops, axis=0)
    #print("std:",std_ops)

    #plot2 = plt.figure(2)
    #
    #for t in range(trials):
    #    plt.plot(range(T), all_ops[t])


    fig, ax = plt.subplots()
    plt.ylim((0.,1.1))
    ax.errorbar(range(T), avg_ops, yerr=std_ops)
    plt.plot(range(T), avg_ops, 'k', linewidth=2, label="average")
    plt.savefig(fname+"_avgOP.png",bbox_inches='tight')
    #plt.show()
