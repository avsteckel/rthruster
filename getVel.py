import math
from math import pi, sin, cos
import matplotlib as mpl
from numpy import floor
import numpy as np
import matplotlib.pyplot as plt
import Tkinter
import tkMessageBox
from Tkinter import *
from decimal import *

def getMdot(r,mdot,RPM):
    res=int(100)
    phi1 = np.deg2rad(45)
    vp1_theta=[]
    vp1_z=[]
    tvec=[]
    thrust=float(0)
    # Assume an equal distribution of particles along the radius
    rad = np.linspace(0,float(r)/100,num = res)
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

root = Tkinter.Tk()
var1 = StringVar()
var2 = StringVar()
var3 = StringVar()
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

Tkinter.Label(root, text="Z velocity ",borderwidth=1).grid(row=5,column=0)
Tkinter.Label(root, text="m/s at r=",borderwidth=1).grid(row=5,column=2)
Tkinter.Label(root, text="cm",borderwidth=1).grid(row=5,column=4)

def CallBack():
    [thrust,zvel,rmax]=getMdot(float(r.get()),float(mdot.get()),float(RPM.get()))
    var1.set(thrust)
    var2.set(zvel)
    var3.set(rmax)
    Tkinter.Label = Message( root, textvariable=var1,width=50).grid(row=4,column=1)
    Tkinter.Label = Message( root, textvariable=var2,width=50).grid(row=5,column=1)
    Tkinter.Label = Message( root, textvariable=var3,width=50).grid(row=5,column=3)
    #tkMessageBox.showinfo( "Hello Python", "Hello World")

B = Button(root, text ="Compute", command = CallBack).grid(row=7,column=1)

root.mainloop()
