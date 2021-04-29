from math import pi
import matplotlib.pyplot as plt
import numpy as np
from copy import copy, deepcopy
from random import random


def phase_distance(th1, th2):
    if th1 > th2:
        val = (th1 - th2) % (2*pi)
    else:
        val = (th2 - th1) % (2*pi)

    if val > pi:
        val = 2*pi - val

    return val

class Bot:

    def __init__(self, K, dt):
        self.K = K
        self.dt = dt
        self.Tinf = 9
        self.Tdef = 6
        self.Tinfi = 9
        self.Tdefi = 6
        self.Trest = 15
        self.infFrac = self.Tinf/(self.Tinf+self.Tdef)
        self.T = self.Trest*random() # start at random point in rest phase
        self.state = "r"
        self.phase = 2*np.pi*(self.T/(self.Tinf+self.Tdef+self.Trest))
        self.currCycleTime = self.Tinfi + self.Tdefi + self.Trest

    def passiveUpdate(self):
        self.T += self.dt
        self.phase = 2*np.pi*self.T/(self.Tinfi+self.Tdefi+self.Trest)

    def activeUpdate(self):
        self.T += self.K*self.dt
        self.phase = 2*np.pi*self.T/(self.Tinfi+self.Tdefi+self.Trest)

    def inflationRule(self):
        self.state = "e"
        self.Tinfi = self.infFrac* (self.Tinf + self.Tdef - (self.T - self.Tinfi - self.Tdefi - self.Trest))
        self.Tdefi = self.Tdef*(self.Tinfi/self.Tinf)
        self.currCycleTime = self.Tinfi + self.Tdefi + self.Trest
        self.T = 0.
        self.phase = 0.


    def checkTransition(self):
        if self.T >= self.Tinfi and self.state == "e":
            self.state = 'c'
        elif self.T >= (self.Tinfi+ self.Tdefi) and self.state == 'c':
            self.state = 'r'
            self.Tinfi = self.Tinf
            self.Tdefi = self.Tdef
        elif self.T >= (self.currCycleTime):
            self.inflationRule()
        else:
            pass


def runTrials(trials, N, K, T, dt):

    Kdt = K*dt
    alldata = np.empty((trials,T,N))
    allstatedata = np.empty((trials,T,N),dtype=str)
    fname = "N"+str(N)+"_Kdt"+str(Kdt)

    for trial in range(trials):

        # start all agents at rest, uniformly random phase
        states = np.zeros((2,N), dtype=str)
        #thetas = pi + pi*np.random.rand(N)


        bots = [Bot(K,dt) for i in range(N)]

        th_hist = np.zeros((T,N), dtype=float)
        state_hist = np.zeros((T,N), dtype=str)
        th_hist[0] = np.array(copy([b.phase for b in bots]))
        state_hist[0] = np.array(copy([b.state for b in bots]))
        states[0] = np.array([b.state for b in bots])
        states[1] = np.array([b.state for b in bots])

        for t in range(1,T):

            for i in range(N): # todo randomize?
                n1 = (i-1) % N
                n2 = (i+1) % N


                # update i if either neighbor inflated
                if states[1][i] == 'r': # current agent in rest state
                    if (states[0][n1] == 'r' and states[1][n1] == 'e') or (states[0][n2] == 'r' and states[1][n2] == 'e'): # if new neighbor inflation
                        bots[i].activeUpdate()
                        bots[i].checkTransition()
                    else:
                        bots[i].passiveUpdate()
                        bots[i].checkTransition()
                else:
                    bots[i].passiveUpdate()
                    bots[i].checkTransition()


            th_hist[t] = copy([b.phase for b in bots])
            states[0] = copy(states[1])
            state_hist[t] = copy(states[1])
            states[1] = [b.state for b in bots]

        alldata[trial] = deepcopy(th_hist)
        allstatedata[trial] = deepcopy(state_hist)

    return alldata, allstatedata, fname

def order_param(ths, N, axis=None):
    return (1/N)*np.abs(np.sum(np.exp(ths*1j), axis=axis))


def plot_colourline(t,val,c):
    cmap ={'r':'k', 'e':'b','c':'g'}
    ax = plt.gca()
    for i in np.arange(len(t)-1):
        ax.plot([t[i],t[i+1]],[val[i],val[i+1]], c=cmap[c[i]])
    return


def makeplots(alldata, statedata, fname, N, T):
    trial1 = alldata[0]
    trial1s = statedata[0]
    plot1 = plt.figure(1)
    for j in range(N):
        plot_colourline(range(T),trial1[:,j],trial1s[:,j])
    plt.savefig(fname+"_trajectories.png",bbox_inches='tight')
    plt.clf()

    all_ops = np.array([order_param(ths, N, axis=1) for ths in alldata])

    avg_ops = np.average(all_ops, axis=0)
    std_ops = np.std(all_ops, axis=0)

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
