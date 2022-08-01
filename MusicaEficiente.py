import numpy as np
import matplotlib.pyplot as plt
import math
import sounddevice as sd

fs = 22050
T = 1
w = 2*np.pi/T

f1 = []
f2 = []
ts = []

f = open("ExampleSignal/signal4",'r')
out = f.readlines()
nlines = len(out)
print(nlines)
signalx = []
signaly = []
dt = T / nlines
t = 0
centrox = 0
centroy = 0

for line in out :
    x = float(line.split()[0])
    y = float(line.split()[1])
    f1.append(x)
    f2.append(y)
    ts = ts + [t]
    t += dt
    centrox+=x
    centroy+=y

centrox/=len(out)
centroy/=len(out)

for i in range(len(out)):
    f1[i]-=centrox
    f2[i]-=centroy
    an = -np.pi
    f1[i]= -(f1[i]*math.cos(an) + f2[i]*math.sin(an))
    f2[i]= -f1[i]*math.sin(an) + f2[i]*math.cos(an)


def ABs(n,f1,f2,ts,dt,T):
    an1 = 0
    an2 = 0
    bn1 = 0
    bn2 = 0
    for i in range(0,len(f1)):
        an1 += f1[i]*math.cos(n*w*ts[i])*dt
        an2 += f2[i]*math.cos(n*w*ts[i])*dt
        bn1 += f1[i]*math.sin(n*w*ts[i])*dt
        bn2 += f2[i]*math.sin(n*w*ts[i])*dt
    an1 = (2*an1) / T
    an2 = (2*an2) / T
    bn1 = (2*bn1) / T
    bn2 = (2*bn2) / T
    return (an1,an2,bn1,bn2)

def signals(f1,f2,ts,t,T):

    fs = 22050
    dt = T/fs
    w = 2*np.pi/T

    a01 , a02 , _ , _ = ABs(0,f1,f2,ts,dt,T)
    ff1 = np.array([0]*t)+ (a01/2)
    ff2 = np.array([0]*t)+ (a02/2)

    N = int(len(f1)/2)
    fr = 50 #35

    for n in range(1,N):
        an1 , an2 , bn1 , bn2 = ABs(n,f1,f2,ts,dt,T)

        armonico1 = an1*np.cos(n*fr*w*t) + bn1*np.sin(n*fr*w*t)
        armonico2 = an2*np.cos(n*fr*w*t) + bn2*np.sin(n*fr*w*t)

        ff1 = np.add(ff1,armonico1)
        ff2 = np.add(ff2,armonico2)

    return (ff1 , ff2)

N = int(len(f1)/2)
dt = T/fs
t = np.arange(0,T*10,dt)

ff1 , ff2 = signals(f1,f2,ts,t,T)

fig = plt.figure(figsize = (10, 10))
##plt.plot(f1,f2)
plt.plot(ff1,ff2)
'''
#plt.plot(ts,f1)
#plt.plot(t,ff1)

#plt.plot(ts,f2)
#plt.plot(t,ff2)
'''
plt.grid()
plt.show()
print("Playing Signal")
stereo_sine = np.column_stack((ff1*0.1,ff2*0.1))
sd.play(stereo_sine, fs)
sd.wait()
