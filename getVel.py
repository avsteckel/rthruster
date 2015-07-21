# Set up python and import packages for GUI and matlab calcs
import math
from math import pi, sin, cos
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import time
from numpy import floor, arange, sin, pi
import numpy as np

import Tkinter
import tkMessageBox
from Tkinter import *
from decimal import *

# get the velocity for the given r, mdot and RPM
def getMdot(r,mdot,RPM):
    res=int(100)
    phi1 = np.deg2rad(45)
    vp1_theta=[]
    vp1_z=[]
    tvec=[]
    thrust=float(0)
    # Assume an equal distribution of particles along the radius
    rad = np.linspace(0,float(r)/100,num = res)
    massflow=mdot
    for x in range(0,res):
        vb=RPM*(2*pi/60)*float(rad[x])  # convert rotational vel to linear
        vp1_theta.append(-sin(90-2*phi1)*vb)
        vp1_z.append(-cos(90-2*phi1)*vb)
        tvec=mdot*vp1_z[x]
        thrust=thrust+tvec
    thrustr=Decimal(thrust).quantize(Decimal('.01'))
    rmax=Decimal(r).quantize(Decimal('.1'))
    zvel=Decimal(vp1_z[res-1]).quantize(Decimal('.1'))
    return [thrustr,zvel,rmax]
    #print ("Vertical Velocity: ", vp1_z[3])

def getPWR(mdot,zvel):
    vel=float(zvel)
    power=float(mdot)*(vel*vel)/1000
    pwr=Decimal(power).quantize(Decimal('.1'))
    #print("Power: ",power)
    return pwr

def getBatt(p):
    # this is gonna get the mass estimate assuming the battery type
    #dry mass of the spacecraft is 30 kg without batteries, including pld
    dryMass = 10
    mass_per_unit = 2.2 # kg
    cap = 12 # Ahr
    V = 12 # V
    A = 400 # Amps
    time = 10 # sec

    pwr = V*A/1000 #in kW
    numBatt=np.floor(float(p)/pwr)+1
    return numBatt

#def getPerformance():
    # normalize the parameters to a


root = Tk()
root.title("Regolith Thruster Shenanagins")
var1 = StringVar()
var2 = StringVar()
var3 = StringVar()
var4 = StringVar()
# Enter the radius
Tkinter.Label(root, text="radius",borderwidth=1 ).grid(row=0,column=0)
r=Entry(root, bd =5)
r.grid(row=0,column=1)
Tkinter.Label(root, text="cm",borderwidth=1 ).grid(row=0,column=2)

# Enter the mass flow rate
Tkinter.Label(root, text="mass flow",borderwidth=1 ).grid(row=1,column=0)
mdot=Tkinter.Entry(root, bd =5)
mdot.grid(row=1,column=1)
Tkinter.Label(root, text="kg/s",borderwidth=1 ).grid(row=1,column=2)

# Enter the RPM
Tkinter.Label(root, text="Impeller Speed",borderwidth=1).grid(row=2,column=0)
RPM=Tkinter.Entry(root, bd=5)
RPM.grid(row=2,column=1)
Tkinter.Label(root, text="RPM",borderwidth=1 ).grid(row=2,column=2)

# Set up results section
Tkinter.Label(root, text="Thrust").grid(row=4,column=0)
Tkinter.Label(root, text="N",borderwidth=1).grid(row=4,column=2)

Tkinter.Label(root, text="Z velocity",borderwidth=1).grid(row=5,column=0)
Tkinter.Label(root, text="m/s at r=",borderwidth=1).grid(row=5,column=2)
Tkinter.Label(root, text="cm",borderwidth=1).grid(row=5,column=4)

Tkinter.Label(root, text="Power",borderwidth=1).grid(row=6,column=0)
Tkinter.Label(root, text="kW",borderwidth=1).grid(row=6,column=2)

# Make a plot
f = Figure()
a = f.add_subplot(111)
x = [0]
perf = [0] # some function

a.plot(x,perf)
a.set_xlabel("Mass")
a.set_title("Performance of the design")
a.set_ylabel("Total Performance Score (0-10)")


# Draw the plot!
root2 = Tk()#.Tk()
root2.title("Plot")
#canvas = Tkinter.Canvas(root, bg="white").grid(row=8,column=1)
canvas = FigureCanvasTkAgg(f, master=root2)
canvas.get_tk_widget().grid(row=0,column=0)
#.pack()

# Update GUI
def Compute():
    [thrust,zvel,rmax]=getMdot(float(r.get()),float(mdot.get()),float(RPM.get()))
    pwr=getPWR(float(mdot.get()),zvel)
    numBatt = getBatt(pwr)
    var1.set(thrust)
    var2.set(zvel)
    var3.set(rmax)
    var4.set(pwr)
    Tkinter.Label = Message( root, textvariable=var1,width=50).grid(row=4,column=1)
    Tkinter.Label = Message( root, textvariable=var2,width=50).grid(row=5,column=1)
    Tkinter.Label = Message( root, textvariable=var3,width=50).grid(row=5,column=3)
    Tkinter.Label = Message( root, textvariable=var4,width=50).grid(row=6,column=1)
    x.append(numBatt)
    perf.append(thrust)

    f = Figure(figsize=(5,4), dpi=100)
    a = f.add_subplot(111)
    a.plot(x,perf)
    canvas = FigureCanvasTkAgg(f, master=root2)
    canvas.get_tk_widget().grid(row=0,column=1)
    tkMessageBox.showinfo( "number of batteries", x)
    tkMessageBox.showinfo( "thrust", perf)


B = Button(root, text ="Compute", command = Compute).grid(row=7,column=1)

root.mainloop()
