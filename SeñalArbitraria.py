import numpy as np
import matplotlib.pyplot as plt
import math
import sounddevice as sd

fs = 22050
T = 1 
w = 2*np.pi/T

f = []
ts = []
t = 0
dt = 0.043

while t<=T:

    ftemp = t*0.5
    f = f + [ftemp]
    ts = ts + [t]
    t += dt

a0 = 0
for i in range(1,len(ts)):
    a0 += f[i]*(ts[i]-ts[i-1])
a0=a0*2/T

def a(n):
    an = 0
    for i in range(1,len(ts)):
      an += f[i]*math.cos(n*w*ts[i])*(ts[i]-ts[i-1])
    return (2*an/T)

def b(n):
    an = 0
    for i in range(1,len(ts)):
      an += f[i]*math.sin(n*w*ts[i])*(ts[i]-ts[i-1])
    return (2*an/T)

N = int(len(f)/2)
fr = 800
dt = T/fs

t = np.arange(0,T*5,dt)
ff = np.array([0]*t)+ (a0/2)

for n in range(1,N):
    armonico = a(n)*np.cos(n*fr*w*t) + b(n)*np.sin(n*fr*w*t)
    ff = np.add(ff,armonico)

fig = plt.figure(figsize = (10, 10))
plt.plot(ts,f)
plt.plot(t,ff)
plt.grid()
plt.show()

stereo_sine = np.column_stack((t,ff))
sd.play(stereo_sine, fs)
sd.wait()
