#!/bin/env python

# option parser
import argparse
import matplotlib.pyplot as plt
#from matplotlib import gridspec
#import mplhep as hep # <-- nice histogram plotting
from scipy.optimize import curve_fit
from scipy.interpolate import make_interp_spline
import os
import numpy as np
import math

#import argparse
#import sys
#import os
#import glob
#import fnmatch
#import ROOT
#from inspect import currentframe, getframeinfo
#import csv
#import math
#from MakePlotHelper import ColorTranslator


def main(args):

    if args.inputHypatia != "":
        getValuesHypatia(args.inputHypatia,"%.4f")
    fig = ATLAStracker()
    arphi = fig.get_axes()[0]
    arz = fig.get_axes()[1]
    if args.truthhits:
        x1, y1, z1, x2, y2, z2 = loadeventfile(args,True)
        fig = drawtrack(args,fig,2,x1,y1,z1)
        fig = drawtrack(args,fig,3,x2,y2,z2)
    if args.recohits:
        x1, y1, z1, x2, y2, z2 = loadeventfile(args,False)
        fig = drawtrack(args,fig,0,x1,y1,z1)
        fig = drawtrack(args,fig,1,x2,y2,z2)

    """
    R1 = plt.Circle((-8596.237522882617, -1771.2335161156957),  8776.81990919414, fill=False, color='darkgray')
    R2 = plt.Circle((-6195.979828752785, -1403.7452370285118),  6353.004543426017, fill=False, color='black')
    arphi.add_patch(R1)
    arphi.add_patch(R2)
    arphi.plot(-0.6766833581348944,3.2809449298675046, marker ='X',ms=6,alpha=1)
    arphi.plot(-1.020553899125501,4.945803245073518, marker ='X',ms=6,alpha=1)
    arphi.plot(-1.790371717580463,8.667010390722279, marker ='X',ms=6,alpha=1)
    arphi.plot(-2.4805217609634824,11.996229065560001, marker ='X',ms=6,alpha=1)
    arphi.plot(-6.083936296086438,29.274489220909764, marker ='X',ms=6,alpha=1)
    arphi.plot(-7.563862834336622,36.32076512166754, marker ='X',ms=6,alpha=1)
    arphi.plot(-9.049570535899747,43.365830709393485, marker ='X',ms=6,alpha=1)
    arphi.plot(-10.520303973434668,50.31185947971447, marker ='X',ms=6,alpha=1)
    arphi.plot(0.7393468381068649,-3.2673944134403765, marker ='P',ms=6,alpha=1)
    arphi.plot(1.113878757106234,-4.925624236019985, marker ='P',ms=6,alpha=1)
    arphi.plot(1.9494632709247273,-8.632617966487075, marker ='P',ms=6,alpha=1)
    arphi.plot(2.6952120547978136,-11.9498256045715, marker ='P',ms=6,alpha=1)
    arphi.plot(6.537994666486615,-29.176439565872194, marker ='P',ms=6,alpha=1)
    arphi.plot(8.09184552438796,-36.20679543966081, marker ='P',ms=6,alpha=1)
    arphi.plot(9.637730252324282,-43.23891945439239, marker ='P',ms=6,alpha=1)
    arphi.plot(11.154341927935395,-50.17509996158157, marker ='P',ms=6,alpha=1)
    """

    plt.show()

### Hilfsfunktion fuer den Betreuer - im Praktikum nicht wichtig.
def getValuesHypatia(iH,rounding):
    sr = "%.12f" if rounding == "" else rounding

    l = iH.split(",")
    p1 = float(l[0])
    phi1 = float(l[1])
    theta1 = float(l[2])
    q1 = float(l[3])
    p2 = float(l[4])
    phi2 = float(l[5])
    theta2 = float(l[6])
    q2 = float(l[7])

    pz1 = p1*math.cos(theta1)
    pt1 = p1*math.sin(theta1)
    px1 = pt1*math.cos(phi1)
    py1 = pt1*math.sin(phi1)
    eta1 = -math.log(math.tan(theta1/2.))
    pz2 = p2*math.cos(theta2)
    pt2 = p2*math.sin(theta2)
    px2 = pt2*math.cos(phi2)
    py2 = pt2*math.sin(phi2)
    eta2 = -math.log(math.tan(theta2/2.))
    mass = math.sqrt(2*pt1*pt2*(math.cosh(eta1-eta2)-math.cos(phi1-phi2)))
    mass2 = math.sqrt((p1+p2)**2-(px1+px2)**2-(py1+py2)**2-(pz1+pz2)**2)
    print("Lep1: pT = "+str(pt1)+", px = "+str(px1)+", py = "+str(py1)+", pz = "+str(pz1)+", eta = "+str(eta1))
    print("Lep2: pT = "+str(pt2)+", px = "+str(px2)+", py = "+str(py2)+", pz = "+str(pz2)+", eta = "+str(eta2))
    print("m12 = "+str(mass)+" ("+str(mass2)+")")
    s1 = max(max(55./(abs(px1)/p1),55./(abs(py1)/p1)),275./(abs(pz1)/p1))
    s2 = max(max(55./(abs(px2)/p2),55./(abs(py2)/p2)),275./(abs(pz2)/p2))
    print("dir1: x = "+str(px1/p1)+", y = "+str(py1/p1)+", r = "+str(pt1/p1)+", z = "+str(pz1/p1))
    print("dir2: x = "+str(px2/p2)+", y = "+str(py2/p2)+", r = "+str(pt2/p2)+", z = "+str(pz2/p2))
    r1 = 100.*pt1/(0.3*2.) # 100 = cm -> m
    r2 = 100.*pt2/(0.3*2.) # 100 = cm -> m
    print(py1,q1,pt1,math.copysign(-py1,q1),math.copysign(py1,q1))
    #print("er1: x = "+str(math.copysign(-py1,q1)/pt1)+", y = "+str(math.copysign(px1,q1)/pt1)+", Rx = "+str(math.copysign(-py1,q1)*r1/pt1)+", Ry = "+str(math.copysign(px1,q1)*r1/pt1)+", R = " +str(r1))
    #print("er2: x = "+str(math.copysign(-py2,q2)/pt2)+", y = "+str(math.copysign(px2,q2)/pt2)+", Rx = "+str(math.copysign(-py2,q2)*r2/pt2)+", Ry = "+str(math.copysign(px2,q2)*r2/pt2)+", R = " +str(r2))
    print("er1: x = "+str(-np.sign(q1)*py1/pt1)+", y = "+str(np.sign(q1)*px1/pt1)+", Rx = "+str(-np.sign(q1)*py1*r1/pt1)+", Ry = "+str(np.sign(q1)*px1*r1/pt1)+", R = " +str(r1))
    print("er2: x = "+str(-np.sign(q2)*py2/pt2)+", y = "+str(np.sign(q2)*px2/pt2)+", Rx = "+str(-np.sign(q2)*py2*r2/pt2)+", Ry = "+str(np.sign(q2)*px2*r2/pt2)+", R = " +str(r2))
    print("    R1 = plt.Circle(("+str(-np.sign(q1)*py1*r1/pt1)+", "+str(np.sign(q1)*px1*r1/pt1)+"), "+str(r1)+", fill=False, color='forestgreen')")
    print("    R2 = plt.Circle(("+str(-np.sign(q2)*py2*r2/pt2)+", "+str(np.sign(q2)*px2*r2/pt2)+"), "+str(r2)+", fill=False, color='blue')")
    
    print("track1,truthhits,x,0.,"+str(px1/p1*s1))
    print("track1,truthhits,y,0.,"+str(py1/p1*s1))
    print("track1,truthhits,z,0.,"+str(pz1/p1*s1))
    print("track2,truthhits,x,0.,"+str(px2/p2*s2))
    print("track2,truthhits,y,0.,"+str(py2/p2*s2))
    print("track2,truthhits,z,0.,"+str(pz2/p2*s2))
    #x1, y1, z1 = [], [], []
    ### if particle fully in barrel
    x1 = [px1/pt1*3.35, px1/pt1*5.05, px1/pt1*8.85, px1/pt1*12.25, px1/pt1*29.9,px1/pt1*37.1, px1/pt1*44.3, px1/pt1*51.4]
    y1 = [py1/pt1*3.35, py1/pt1*5.05, py1/pt1*8.85, py1/pt1*12.25, py1/pt1*29.9,py1/pt1*37.1, py1/pt1*44.3, py1/pt1*51.4]
    z1 = [pz1/pt1*3.35, pz1/pt1*5.05, pz1/pt1*8.85, pz1/pt1*12.25, pz1/pt1*29.9,pz1/pt1*37.1, pz1/pt1*44.3, pz1/pt1*51.4]
    x2 = [px2/pt2*3.35, px2/pt2*5.05, px2/pt2*8.85, px2/pt2*12.25, px2/pt2*29.9,px2/pt2*37.1, px2/pt2*44.3, px2/pt2*51.4]
    y2 = [py2/pt2*3.35, py2/pt2*5.05, py2/pt2*8.85, py2/pt2*12.25, py2/pt2*29.9,py2/pt2*37.1, py2/pt2*44.3, py2/pt2*51.4]
    z2 = [pz2/pt2*3.35, pz2/pt2*5.05, pz2/pt2*8.85, pz2/pt2*12.25, pz2/pt2*29.9,pz2/pt2*37.1, pz2/pt2*44.3, pz2/pt2*51.4]
    ### both barrel and endcap
    #B
    #x2 = [px2/pt2*3.35, px2/pt2*5.05, px2/pt2*8.85, px2/abs(pz2)*49.50, px2/abs(pz2)*58.00, px2/abs(pz2)*129.99, px2/abs(pz2)*139.97, px2/abs(pz2)*177.14, px2/abs(pz2)*211.52]
    #y2 = [py2/pt2*3.35, py2/pt2*5.05, py2/pt2*8.85, py2/abs(pz2)*49.50, py2/abs(pz2)*58.00, py2/abs(pz2)*129.99, py2/abs(pz2)*139.97, py2/abs(pz2)*177.14, py2/abs(pz2)*211.52]
    #z2 = [pz2/pt2*3.35, pz2/pt2*5.05, pz2/pt2*8.85, pz2/abs(pz2)*49.50, pz2/abs(pz2)*58.00, pz2/abs(pz2)*129.99, pz2/abs(pz2)*139.97, pz2/abs(pz2)*177.14, pz2/abs(pz2)*211.52]
    #D /F
    #x1 = [px1/pt1*3.35, px1/pt1*5.05, px1/abs(pz1)*58.00, px1/abs(pz1)*65.00, px1/abs(pz1)*177.14, px1/abs(pz1)*211.52, px1/abs(pz1)*250.50, px1/abs(pz1)*272.02]
    #y1 = [py1/pt1*3.35, py1/pt1*5.05, py1/abs(pz1)*58.00, py1/abs(pz1)*65.00, py1/abs(pz1)*177.14, py1/abs(pz1)*211.52, py1/abs(pz1)*250.50, py1/abs(pz1)*272.02]
    #z1 = [pz1/pt1*3.35, pz1/pt1*5.05, pz1/abs(pz1)*58.00, pz1/abs(pz1)*65.00, pz1/abs(pz1)*177.14, pz1/abs(pz1)*211.52, pz1/abs(pz1)*250.50, pz1/abs(pz1)*272.02]
    #x2 = [px2/pt2*3.35, px2/pt2*5.05, px2/pt2*8.85, px2/abs(pz2)*49.50, px2/abs(pz2)*58.00, px2/abs(pz2)*129.99, px2/abs(pz2)*139.97, px2/abs(pz2)*177.14, px2/abs(pz2)*211.52]
    #y2 = [py2/pt2*3.35, py2/pt2*5.05, py2/pt2*8.85, py2/abs(pz2)*49.50, py2/abs(pz2)*58.00, py2/abs(pz2)*129.99, py2/abs(pz2)*139.97, py2/abs(pz2)*177.14, py2/abs(pz2)*211.52]
    #z2 = [pz2/pt2*3.35, pz2/pt2*5.05, pz2/pt2*8.85, pz2/abs(pz2)*49.50, pz2/abs(pz2)*58.00, pz2/abs(pz2)*129.99, pz2/abs(pz2)*139.97, pz2/abs(pz2)*177.14, pz2/abs(pz2)*211.52]
    #I
    #x1 = [px1/pt1*3.35, px1/pt1*5.05, px1/pt1*8.85, px1/pt1*12.25, px1/pt1*29.9,px1/pt1*37.1, px1/pt1*44.3, px1/abs(pz1)*85.38, px1/abs(pz1)*93.40]
    #y1 = [py1/pt1*3.35, py1/pt1*5.05, py1/pt1*8.85, py1/pt1*12.25, py1/pt1*29.9,py1/pt1*37.1, py1/pt1*44.3, py1/abs(pz1)*85.38, py1/abs(pz1)*93.40]
    #z1 = [pz1/pt1*3.35, pz1/pt1*5.05, pz1/pt1*8.85, pz1/pt1*12.25, pz1/pt1*29.9,pz1/pt1*37.1, pz1/pt1*44.3, pz1/abs(pz1)*85.38, pz1/abs(pz1)*93.40]
    #J
    #x1 = [px1/pt1*3.35, px1/pt1*5.05, px1/abs(pz1)*49.50, px1/abs(pz1)*58.00, px1/abs(pz1)*65.00,  px1/abs(pz1)*129.99, px1/abs(pz1)*139.97, px1/abs(pz1)*177.14, px1/abs(pz1)*211.52, px1/abs(pz1)*250.50]
    #y1 = [py1/pt1*3.35, py1/pt1*5.05, py1/abs(pz1)*49.50, py1/abs(pz1)*58.00, py1/abs(pz1)*65.00,  py1/abs(pz1)*129.99, py1/abs(pz1)*139.97, py1/abs(pz1)*177.14, py1/abs(pz1)*211.52, py1/abs(pz1)*250.50]
    #z1 = [pz1/pt1*3.35, pz1/pt1*5.05, pz1/abs(pz1)*49.50, pz1/abs(pz1)*58.00, pz1/abs(pz1)*65.00,  pz1/abs(pz1)*129.99, pz1/abs(pz1)*139.97, pz1/abs(pz1)*177.14, pz1/abs(pz1)*211.52, pz1/abs(pz1)*250.50]
    #K
    #x1 = [px1/pt1*3.35, px1/pt1*5.05, px1/abs(pz1)*58.00, px1/abs(pz1)*65.00, px1/abs(pz1)*177.14, px1/abs(pz1)*211.52, px1/abs(pz1)*250.50, px1/abs(pz1)*272.02]
    #y1 = [py1/pt1*3.35, py1/pt1*5.05, py1/abs(pz1)*58.00, py1/abs(pz1)*65.00, py1/abs(pz1)*177.14, py1/abs(pz1)*211.52, py1/abs(pz1)*250.50, py1/abs(pz1)*272.02]
    #z1 = [pz1/pt1*3.35, pz1/pt1*5.05, pz1/abs(pz1)*58.00, pz1/abs(pz1)*65.00, pz1/abs(pz1)*177.14, pz1/abs(pz1)*211.52, pz1/abs(pz1)*250.50, pz1/abs(pz1)*272.02]
    #M
    #x1 = [px1/pt1*3.35, px1/pt1*5.05, px1/pt1*8.85, px1/pt1*12.25, px1/abs(pz1)*93.40, px1/abs(pz1)*109.15, px1/abs(pz1)*129.99, px1/abs(pz1)*139.97, px1/abs(pz1)*177.14]
    #y1 = [py1/pt1*3.35, py1/pt1*5.05, py1/pt1*8.85, py1/pt1*12.25, py1/abs(pz1)*93.40, py1/abs(pz1)*109.15, py1/abs(pz1)*129.99, py1/abs(pz1)*139.97, py1/abs(pz1)*177.14]
    #z1 = [pz1/pt1*3.35, pz1/pt1*5.05, pz1/pt1*8.85, pz1/pt1*12.25, pz1/abs(pz1)*93.40, pz1/abs(pz1)*109.15, pz1/abs(pz1)*129.99, pz1/abs(pz1)*139.97, pz1/abs(pz1)*177.14]
    
    mystr = ""
    for x in x1: mystr += ","+str(sr % x)
    print("track1,truthhits,x,0."+mystr)
    mystr = ""
    for x in y1: mystr += ","+str(sr % x)
    print("track1,truthhits,y,0."+mystr)
    mystr = ""
    for x in z1: mystr += ","+str(sr % x)
    print("track1,truthhits,z,0."+mystr)
    mystr = ""
    for x in x2: mystr += ","+str(sr % x)
    print("track2,truthhits,x,0."+mystr)
    mystr = ""
    for x in y2: mystr += ","+str(sr % x)
    print("track2,truthhits,y,0."+mystr)
    mystr = ""
    for x in z2: mystr += ","+str(sr % x)
    print("track2,truthhits,z,0."+mystr)

    # full barrel
    rdet1=[ 3.3500,5.0500,8.8500,12.2500,29.9000,37.1000,44.3000,51.4000]
    rdet2=[ 3.3500,5.0500,8.8500,12.2500,29.9000,37.1000,44.3000,51.4000]
    #B
    #rdet2=[ 3.3500,5.0500,8.8500,12.0610,14.1321,31.6730,34.1047,43.1614,51.5383]
    #D
    #rdet1=[ 3.3500,5.0500,10.2305,11.4653,31.2455,37.3097,44.1853,47.9812]
    #rdet2=[ 3.3500,5.0500,8.8500,11.8302,13.8616,31.0667,33.4519,42.3352,50.5518]
    #F
    #rdet1=[ 3.3500,5.0500,11.1301,12.4733,33.9927,40.5902,48.0703,52.1999]
    #rdet2=[ 3.3500,5.0500,8.8500,11.9349,13.9843,31.3417,33.7479,42.7099,50.9992]
    #I
    #rdet1=[ 3.3500,5.0500,8.8500,12.2500,29.9000,37.1000,44.3000,51.0633,55.8598]
    #J
    #rdet1=[ 3.3500,5.0500,10.7577,12.6050,14.1263,28.2504,30.4194,38.4974,45.9692,54.4406]
    #K
    #rdet1=[ 3.3500,5.0500,9.5739,10.7294,29.2401,34.9151,41.3495,44.9018]
    #M
    #rdet1=[ 3.3500,5.0500,8.8500,12.2500,29.2601,34.1942,40.7229,43.8494,55.4939]


    x1_r, y1_r, x2_r, y2_r = [], [], [], []
    z1_r, z2_r = z1, z2
    

    for r in rdet1:
        x1r, y1r = get_intersection_circles(0,0,0,r,-np.sign(q1)*py1*r1/pt1,np.sign(q1)*px1*r1/pt1,r1,px1/pt1,py1/pt1)
        x1_r.append(x1r)
        y1_r.append(y1r)
    for r in rdet2:
        x2r, y2r = get_intersection_circles(1,0,0,r,-np.sign(q2)*py2*r2/pt2,np.sign(q2)*px2*r2/pt2,r2,px2/pt2,py2/pt2)
        x2_r.append(x2r)
        y2_r.append(y2r)
        mystr = ""
    for x in x1_r: mystr += ","+str(sr % x)
    print("track1,recohits,x,0."+mystr)
    mystr = ""
    for x in y1_r: mystr += ","+str(sr % x)
    print("track1,recohits,y,0."+mystr)
    mystr = ""
    for x in z1_r: mystr += ","+str(sr % x)
    print("track1,recohits,z,0."+mystr)
    mystr = ""
    for x in x2_r: mystr += ","+str(sr % x)
    print("track2,recohits,x,0."+mystr)
    mystr = ""
    for x in y2_r: mystr += ","+str(sr % x)
    print("track2,recohits,y,0."+mystr)
    mystr = ""
    for x in z2_r: mystr += ","+str(sr % x)
    print("track2,recohits,z,0."+mystr)

    mystr = "    rdet1=[ "
    for x, y in zip(x1,y1): mystr += ","+str(sr % math.sqrt(x**2+y**2))
    print(mystr+"]")
    mystr = "    rdet2=[ "
    for x, y in zip(x2,y2): mystr += ","+str(sr % math.sqrt(x**2+y**2))
    print(mystr+"]")
    mystr = ""
    #for x, y in zip(x1_r,y1_r): mystr += ","+str(sr % math.sqrt(x**2+y**2))
    #print(mystr)
    #mystr = ""
    #for x, y in zip(x2_r,y2_r): mystr += ","+str(sr % math.sqrt(x**2+y**2))
    #print(mystr)

def get_intersection_circles(ntrack,x0, y0, r0, x1, y1, r1,dirx, diry):
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1

    d=math.sqrt((x1-x0)**2 + (y1-y0)**2)

    # non intersecting
    if d > r0 + r1 :
        print("A",d,r0,r1)
        return {}
    # One circle within other
    if d < abs(r0-r1):
        print("B",d,r0,r1)
        return {}
    # coincident circles
    if d == 0 and r0 == r1:
        print("C",d,r0,r1)
        return {}
    else:
        a=(r0**2-r1**2+d**2)/(2*d)
        h=math.sqrt(r0**2-a**2)
        x2=x0+a*(x1-x0)/d   
        y2=y0+a*(y1-y0)/d   
        x3=x2+h*(y1-y0)/d     
        y3=y2-h*(x1-x0)/d 
        x4=x2-h*(y1-y0)/d
        y4=y2+h*(x1-x0)/d
        mymarker = ['X','P']
        
        if x3*dirx > 0 and y3*diry>0:
            #print("    arphi.plot("+str(x3)+","+str(y3)+", marker ='"+mymarker[ntrack]+"',ms=6,alpha=1)")
            return x3, y3
        else:
            #print("    arphi.plot("+str(x4)+","+str(y4)+", marker ='"+mymarker[ntrack]+"',ms=6,alpha=1)")
            return x4, y4
        return x3, y3, x4, y4

### Diese Funktion ladet die Information der Tracks in den ATLAS-Plot
def drawtrack(args,fig,trackn,x,y,z):
    arphi = fig.get_axes()[0]
    arz = fig.get_axes()[1]
    r = np.sqrt(x**2 + y**2)*np.sign(y)
    mycolor = ['red', 'brown','forestgreen','royalblue']
    mymarker = ['h','H','p','8']
    xy = plt.Line2D(x[1:],y[1:], marker=mymarker[trackn], markersize=4, linewidth=0, color=mycolor[trackn])
    rz = plt.Line2D(z[1:],r[1:], marker=mymarker[trackn], markersize=4, linewidth=0, color=mycolor[trackn])
    arphi.add_line(xy)
    arz.add_line(rz)
    if args.extratrack:
        xnew = x
        ynew = y
        znew = z
        rnew = r
        if args.interpolate:
           t=np.arange(len(x))
           tnew = np.arange(len(x),step=0.005)
           splxy = make_interp_spline(t,np.c_[x,y],3)
           xnew, ynew = splxy(tnew).T
           splrz = make_interp_spline(t,np.c_[z,r],3)
           znew, rnew = splrz(tnew).T
        lxy = plt.Line2D(xnew,ynew, linestyle='dotted', color=mycolor[trackn])
        lrz = plt.Line2D(znew,rnew, linestyle='dotted', color=mycolor[trackn])
        arphi.add_line(lxy)
        arz.add_line(lrz)

    return fig

    
### Lade die Informationen der beiden Tracks/Spuren, welche ein Z-Boson formen
def loadeventfile(args,truth):
    x1, y1, z1, x2, y2, z2 = [], [], [], [], [], []
    with open(args.eventfile) as f:
        lines = f.readlines()
    for line in lines:
        if line=="\n":
            continue
        l = line.split(",")
        if truth and l[1]!="truthhits":
            continue
        elif not truth and l[1]!="recohits":
            continue
        if l[0] == "track1" and l[2] == "x":
            x1 = np.array(l[3:])
            x1 = np.asarray(x1, dtype=float)
        if l[0] == "track1" and l[2] == "y":
            y1 = np.array(l[3:])
            y1 = np.asarray(y1, dtype=float)
        if l[0] == "track1" and l[2] == "z":
            z1 = np.array(l[3:])
            z1 = np.asarray(z1, dtype=float)
        if l[0] == "track2" and l[2] == "x":
            x2 = np.array(l[3:])
            x2 = np.asarray(x2, dtype=float)
        if l[0] == "track2" and l[2] == "y":
            y2 = np.array(l[3:])
            y2 = np.asarray(y2, dtype=float)
        if l[0] == "track2" and l[2] == "z":
            z2 = np.array(l[3:])
            z2 = np.asarray(z2, dtype=float)

            
    return x1, y1, z1, x2, y2, z2

### Hard-coded vereinfachte Version des inneren ATLAS-Detektor (pixel and SCT only)
### Werte entnommen von https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/PAPERS/PERF-2015-07/fig_01.png
def ATLAStracker():
    # Load specific event with x,y,z coordinates and Lepton-Detektor Path (and Truth-Path)
    # to be done later

    ### Lade den ATLAS Detektor
    # Zuerst bilden wir das Grid von xy/rphi und rz Ansichten.
    fig, (arphi, arz) = plt.subplots(1, 2, width_ratios=[1, 2],figsize=(12,4.35))
    arphi.set_xlim(-57.5,57.5)
    arphi.set_ylim(-57.5,57.5)
    arz.set_xlim(-285,285)
    arz.set_ylim(-57.5,57.5)
    plt.subplots_adjust(left=0.065,bottom=0.13,right=0.965,top=0.9,wspace=0.15)
    arphi.xaxis.set_ticks(np.arange(-55, 66, 11))
    arphi.yaxis.set_ticks(np.arange(-55, 66, 11))
    arz.yaxis.set_ticks(np.arange(-55, 66, 11))
    start, end = arz.get_xlim()
    arz.xaxis.set_ticks(np.arange(-275, 330, 55))
    arphi.set_xlabel("x [cm]")
    arphi.set_ylabel("y [cm]")
    arz.set_ylabel(r"r$_{\perp}$ [cm]")
    arz.set_xlabel("z [cm]")
    rphi_IBL   = plt.Circle((0, 0),  3.35, fill=False, color='peru')
    rphi_pixl1 = plt.Circle((0, 0),  5.05, fill=False, color='plum')
    rphi_pixl2 = plt.Circle((0, 0),  8.85, fill=False, color='plum')
    rphi_pixl3 = plt.Circle((0, 0), 12.25, fill=False, color='plum')
    rphi_SCTl1 = plt.Circle((0, 0), 29.90, fill=False, color='cornflowerblue')
    rphi_SCTl2 = plt.Circle((0, 0), 37.10, fill=False, color='cornflowerblue')
    rphi_SCTl3 = plt.Circle((0, 0), 44.30, fill=False, color='cornflowerblue')
    rphi_SCTl4 = plt.Circle((0, 0), 51.40, fill=False, color='cornflowerblue')
    arphi.add_patch(rphi_IBL)
    arphi.add_patch(rphi_pixl1)
    arphi.add_patch(rphi_pixl2)
    arphi.add_patch(rphi_pixl3)
    arphi.add_patch(rphi_SCTl1)
    arphi.add_patch(rphi_SCTl2)
    arphi.add_patch(rphi_SCTl3)
    arphi.add_patch(rphi_SCTl4)
    rz_IBL_u    = plt.Line2D([ -33.15,   33.15], [  3.35,   3.35], color='peru')
    rz_IBL_l    = plt.Line2D([ -33.15,   33.15], [ -3.35,  -3.35], color='peru')
    rz_pixl1_u  = plt.Line2D([ -40.05,   40.05], [  5.05,   5.05], color='plum')
    rz_pixl1_l  = plt.Line2D([ -40.05,   40.05], [ -5.05,  -5.05], color='plum')
    rz_pixl2_u  = plt.Line2D([ -40.05,   40.05], [  8.85,   8.85], color='plum')
    rz_pixl2_l  = plt.Line2D([ -40.05,   40.05], [ -8.85,  -8.85], color='plum')
    rz_pixl3_u  = plt.Line2D([ -40.05,   40.05], [ 12.25,  12.25], color='plum')
    rz_pixl3_l  = plt.Line2D([ -40.05,   40.05], [-12.25, -12.25], color='plum')
    rz_pixd1_lu = plt.Line2D([ -49.50,  -49.50], [  8.88,  14.96], color='plum')
    rz_pixd1_ru = plt.Line2D([  49.50,   49.50], [  8.88,  14.96], color='plum')
    rz_pixd1_ll = plt.Line2D([ -49.50,  -49.50], [ -8.88, -14.96], color='plum')
    rz_pixd1_rl = plt.Line2D([  49.50,   49.50], [ -8.88, -14.96], color='plum')
    rz_pixd2_lu = plt.Line2D([ -58.00,  -58.00], [  8.88,  14.96], color='plum')
    rz_pixd2_ru = plt.Line2D([  58.00,   58.00], [  8.88,  14.96], color='plum')
    rz_pixd2_ll = plt.Line2D([ -58.00,  -58.00], [ -8.88, -14.96], color='plum')
    rz_pixd2_rl = plt.Line2D([  58.00,   58.00], [ -8.88, -14.96], color='plum')
    rz_pixd3_lu = plt.Line2D([ -65.00,  -65.00], [  8.88,  14.96], color='plum')
    rz_pixd3_ru = plt.Line2D([  65.00,   65.00], [  8.88,  14.96], color='plum')
    rz_pixd3_ll = plt.Line2D([ -65.00,  -65.00], [ -8.88, -14.96], color='plum')
    rz_pixd3_rl = plt.Line2D([  65.00,   65.00], [ -8.88, -14.96], color='plum')
    rz_SCTl1_u  = plt.Line2D([ -74.90,   74.90], [ 29.90,  29.90], color='cornflowerblue')
    rz_SCTl1_l  = plt.Line2D([ -74.90,   74.90], [-29.90, -29.90], color='cornflowerblue')
    rz_SCTl2_u  = plt.Line2D([ -74.90,   74.90], [ 37.10,  37.10], color='cornflowerblue')
    rz_SCTl2_l  = plt.Line2D([ -74.90,   74.90], [-37.10, -37.10], color='cornflowerblue')
    rz_SCTl3_u  = plt.Line2D([ -74.90,   74.90], [ 44.30,  44.30], color='cornflowerblue')
    rz_SCTl3_l  = plt.Line2D([ -74.90,   74.90], [-44.30, -44.30], color='cornflowerblue')
    rz_SCTl4_u  = plt.Line2D([ -74.90,   74.90], [ 51.40,  51.40], color='cornflowerblue')
    rz_SCTl4_l  = plt.Line2D([ -74.90,   74.90], [-51.40, -51.40], color='cornflowerblue')
    rz_SCTd1_lu = plt.Line2D([ -85.38,  -85.38], [ 33.76,  56.00], color='steelblue')
    rz_SCTd1_ll = plt.Line2D([ -85.38,  -85.38], [-33.76, -56.00], color='steelblue')
    rz_SCTd1_ru = plt.Line2D([  85.38,   85.38], [ 33.76,  56.00], color='steelblue')
    rz_SCTd1_rl = plt.Line2D([  85.38,   85.38], [-33.76, -56.00], color='steelblue')
    rz_SCTd2_lu = plt.Line2D([ -93.40,  -93.40], [ 27.50,  56.00], color='steelblue')
    rz_SCTd2_ll = plt.Line2D([ -93.40,  -93.40], [-27.50, -56.00], color='steelblue')
    rz_SCTd2_ru = plt.Line2D([  93.40,   93.40], [ 27.50,  56.00], color='steelblue')
    rz_SCTd2_rl = plt.Line2D([  93.40,   93.40], [-27.50, -56.00], color='steelblue')
    rz_SCTd3_lu = plt.Line2D([-109.15, -109.15], [ 27.50,  56.00], color='steelblue')
    rz_SCTd3_ll = plt.Line2D([-109.15, -109.15], [-27.50, -56.00], color='steelblue')
    rz_SCTd3_ru = plt.Line2D([ 109.15,  109.15], [ 27.50,  56.00], color='steelblue')
    rz_SCTd3_rl = plt.Line2D([ 109.15,  109.15], [-27.50, -56.00], color='steelblue')
    rz_SCTd4_lu = plt.Line2D([-129.99, -129.99], [ 27.50,  56.00], color='steelblue')
    rz_SCTd4_ll = plt.Line2D([-129.99, -129.99], [-27.50, -56.00], color='steelblue')
    rz_SCTd4_ru = plt.Line2D([ 129.99,  129.99], [ 27.50,  56.00], color='steelblue')
    rz_SCTd4_rl = plt.Line2D([ 129.99,  129.99], [-27.50, -56.00], color='steelblue')
    rz_SCTd5_lu = plt.Line2D([-139.97, -139.97], [ 27.50,  56.00], color='steelblue')
    rz_SCTd5_ll = plt.Line2D([-139.97, -139.97], [-27.50, -56.00], color='steelblue')
    rz_SCTd5_ru = plt.Line2D([ 139.97,  139.97], [ 27.50,  56.00], color='steelblue')
    rz_SCTd5_rl = plt.Line2D([ 139.97,  139.97], [-27.50, -56.00], color='steelblue')
    rz_SCTd6_lu = plt.Line2D([-177.14, -177.14], [ 27.50,  56.00], color='steelblue')
    rz_SCTd6_ll = plt.Line2D([-177.14, -177.14], [-27.50, -56.00], color='steelblue')
    rz_SCTd6_ru = plt.Line2D([ 177.14,  177.14], [ 27.50,  56.00], color='steelblue')
    rz_SCTd6_rl = plt.Line2D([ 177.14,  177.14], [-27.50, -56.00], color='steelblue')
    rz_SCTd7_lu = plt.Line2D([-211.52, -211.52], [ 33.76,  56.00], color='steelblue')
    rz_SCTd7_ll = plt.Line2D([-211.52, -211.52], [-33.76, -56.00], color='steelblue')
    rz_SCTd7_ru = plt.Line2D([ 211.52,  211.52], [ 33.76,  56.00], color='steelblue')
    rz_SCTd7_rl = plt.Line2D([ 211.52,  211.52], [-33.76, -56.00], color='steelblue')
    rz_SCTd8_lu = plt.Line2D([-250.50, -250.50], [ 40.80,  56.00], color='steelblue')
    rz_SCTd8_ll = plt.Line2D([-250.50, -250.50], [-40.80, -56.00], color='steelblue')
    rz_SCTd8_ru = plt.Line2D([ 250.50,  250.50], [ 40.80,  56.00], color='steelblue')
    rz_SCTd8_rl = plt.Line2D([ 250.50,  250.50], [-40.80, -56.00], color='steelblue')
    rz_SCTd9_lu = plt.Line2D([-272.02, -272.02], [ 43.88,  56.00], color='steelblue')
    rz_SCTd9_ll = plt.Line2D([-272.02, -272.02], [-43.88, -56.00], color='steelblue')
    rz_SCTd9_ru = plt.Line2D([ 272.02,  272.02], [ 43.88,  56.00], color='steelblue')
    rz_SCTd9_rl = plt.Line2D([ 272.02,  272.02], [-43.88, -56.00], color='steelblue')
    arz.add_line(rz_IBL_u)
    arz.add_line(rz_IBL_l)
    arz.add_line(rz_pixl1_u)
    arz.add_line(rz_pixl1_l)
    arz.add_line(rz_pixl2_u)
    arz.add_line(rz_pixl2_l)
    arz.add_line(rz_pixl3_u)
    arz.add_line(rz_pixl3_l)
    arz.add_line(rz_pixd1_lu)
    arz.add_line(rz_pixd1_ru)
    arz.add_line(rz_pixd1_ll)
    arz.add_line(rz_pixd1_rl)
    arz.add_line(rz_pixd2_lu)
    arz.add_line(rz_pixd2_ru)
    arz.add_line(rz_pixd2_ll)
    arz.add_line(rz_pixd2_rl)
    arz.add_line(rz_pixd3_lu)
    arz.add_line(rz_pixd3_ru)
    arz.add_line(rz_pixd3_ll)
    arz.add_line(rz_pixd3_rl)
    arz.add_line(rz_SCTl1_u)
    arz.add_line(rz_SCTl1_l)
    arz.add_line(rz_SCTl2_u)
    arz.add_line(rz_SCTl2_l)
    arz.add_line(rz_SCTl3_u)
    arz.add_line(rz_SCTl3_l)
    arz.add_line(rz_SCTl4_u)
    arz.add_line(rz_SCTl4_l)
    arz.add_line(rz_SCTd1_lu)
    arz.add_line(rz_SCTd1_ll)
    arz.add_line(rz_SCTd1_ru)
    arz.add_line(rz_SCTd1_rl)
    arz.add_line(rz_SCTd2_lu)
    arz.add_line(rz_SCTd2_ll)
    arz.add_line(rz_SCTd2_ru)
    arz.add_line(rz_SCTd2_rl)
    arz.add_line(rz_SCTd3_lu)
    arz.add_line(rz_SCTd3_ll)
    arz.add_line(rz_SCTd3_ru)
    arz.add_line(rz_SCTd3_rl)
    arz.add_line(rz_SCTd4_lu)
    arz.add_line(rz_SCTd4_ll)
    arz.add_line(rz_SCTd4_ru)
    arz.add_line(rz_SCTd4_rl)
    arz.add_line(rz_SCTd5_lu)
    arz.add_line(rz_SCTd5_ll)
    arz.add_line(rz_SCTd5_ru)
    arz.add_line(rz_SCTd5_rl)
    arz.add_line(rz_SCTd6_lu)
    arz.add_line(rz_SCTd6_ll)
    arz.add_line(rz_SCTd6_ru)
    arz.add_line(rz_SCTd6_rl)
    arz.add_line(rz_SCTd7_lu)
    arz.add_line(rz_SCTd7_ll)
    arz.add_line(rz_SCTd7_ru)
    arz.add_line(rz_SCTd7_rl)
    arz.add_line(rz_SCTd8_lu)
    arz.add_line(rz_SCTd8_ll)
    arz.add_line(rz_SCTd8_ru)
    arz.add_line(rz_SCTd8_rl)
    arz.add_line(rz_SCTd9_lu)
    arz.add_line(rz_SCTd9_ll)
    arz.add_line(rz_SCTd9_ru)
    arz.add_line(rz_SCTd9_rl)

    return fig

if __name__ == "__main__":

    # Define options
    parser = argparse.ArgumentParser(description="Plotter for VVV analysis")
    parser.add_argument('-ef' , '--eventfile'  ,  dest='eventfile'   , help='Read in the event file to be plotted'        , type=str  , required=True, default="ZeventA.txt")
    parser.add_argument('-th' , '--truthhits'  ,  dest='truthhits'   , help='Use truth hits'                              ,                            default=False, action='store_true') 
    parser.add_argument('-rh' , '--recohits'   ,  dest='recohits'    , help='Use reco hits'                               ,                            default=False, action='store_true') 
    parser.add_argument('-ex' , '--extratrack' ,  dest='extratrack'  , help='Extrapolate a track'                         ,                            default=False, action='store_true') 
    parser.add_argument('-it' , '--interpolate',  dest='interpolate' , help='Interpolate a track (not strict lines)'      ,                            default=False, action='store_true')
    parser.add_argument('-iH',  '--inputHypatia', dest='inputHypatia', help='input Hypatia coordinates for testing'       , type=str  , required=False, default="")

    # Argument parser
    args = parser.parse_args()

    # Main
    main(args)

