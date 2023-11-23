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
        if args.printhits:
            printhits(0,x1,y1,z1)
            printhits(1,x2,y2,z2)


    plt.show()


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

def printhits(trackn,x,y,z):
    track = "first" if trackn==0 else ("second" if  trackn==1 else "")
    print("Coordinates of hits corresponding to "+track+" track in (x,y,z) - all values in cm:")
    for i in range(len(x)):
        print("hit "+str(i)+": ("+str(x[i])+", "+str(y[i])+", "+str(z[i])+")")
    print("Note: hit (0, 0, 0) is just the assumed collision point and no detector measurement.")

    
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
    parser.add_argument('-ph' , '--printhits'  ,  dest='printhits'   , help='Printout hit coordinates of tracks'          ,                            default=False, action='store_true')
 

    # Argument parser
    args = parser.parse_args()

    # Main
    main(args)

