#!/bin/env python

# option parser
import argparse
import matplotlib.pyplot as plt
#import mplhep as hep # <-- nice histogram plotting
from scipy.optimize import curve_fit
import os
import numpy as np

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


#Hier ist die Hauptfunktion, um deine Histogramme in eine Grafik (Plot) ansehnlich darzustellen. In Prinzip solltest Du hier nichts schreiben muessen, da alle noetigen Optionen in der Commandline eingegeben werden koennen.
#Zwingende Eingaben:
#histname: Welches Histogramm moechtest du speziell plotten. Du kannst mehrere plotten, trenne Argumente mit einem Komma (,) aber keinem Leerzeichen ( ). Aber Vorsicht, wenn du verschiedene Flags gesetzt hast wie xMin, etc.
#Weitere Inputs gibt es weiter unten (auf englisch)
def main(args):

    #print ("")
    #print ("     -----------")
    #print ("       Plotter  ")
    #print ("     -----------")
    #print ("")


    print("You are plotting histogram(s) " + args.histname + " to output directory " + args.outdir)
    print("Files used are given in " + args.indir)

    ### Ueberpruefe, ob das Eingangsverzeichnis / Dateien exisitieren
    indir = os.path.join(args.indir,"")
    if not os.path.exists(indir):
        print("The input directory "+indir+" does not exist - exit")
        return 0
    dataname = indir+args.histname+"_Data.npz"
    signalname = indir+args.histname+"_Signal.npz"
    backgroundname = indir+args.histname+"_Background.npz"
    if not os.path.isfile(dataname):
        print("The input file "+dataname+" does not exist - exit")
        return 0
    if not os.path.isfile(signalname):
        print("The input file "+signalname+" does not exist - exit")
        return 0
    if not os.path.isfile(backgroundname):
        print("The input file "+backgroundname+" does not exist - exit")
        return 0
    
    ### Stelle sicher, dass das Verzeichnis, in welche wir die Daten speichern wollen, existiert. Falls nicht, wird es erzeugt.
    outdir = os.path.join(args.outdir,"")
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    ### Lade die Daten
    _data = np.load(dataname)
    _sig  = np.load(signalname)
    _bkg  = np.load(backgroundname)
    ### Passe sie wieder in die Histogram-Form
    #hdata, bins = np.histogram(_data["binning"][:-1],bins=_data["binning"],weights=_data["histo"])
    #hsig, temp  = np.histogram( _sig["binning"][:-1],bins= _sig["binning"],weights= _sig["histo"])
    #hbkg, temp  = np.histogram( _bkg["binning"][:-1],bins= _bkg["binning"],weights= _bkg["histo"])
    hdata = _data["histo"]
    hsig  =  _sig["histo"]
    hbkg  =  _bkg["histo"]
    bins  = _data["binning"]
    hdataunc = _data["uncertainty"]
    hbkgunc  =  _bkg["uncertainty"]
    hsigunc  =  _sig["uncertainty"]

    ### Objekt, dass den Plot enthaelt
    if args.ratio:
        fig, (ax, ar) = plt.subplots(2, 1, height_ratios=[11, 2])
    else:
        fig, ax = plt.subplots()
    #fig.set_size_inches((12, 8))
    ### Gebe dem Histogram ein Titel
    ax.set_title(args.histtitle)
    ### Gebe der x- und y-Achsen Namen
    if not args.ratio:
        ax.set_xlabel(args.xtitle) # z.B. "m\${}_{ll}\$ [GeV/c\${}^2\$]"
    ax.set_ylabel(args.ytitle)
    ### Definiere das Objekt, welches du Plotten moechtest
    ### Zuerst die Daten
    bin_center = (bins[1:] + bins[:-1]) / 2 # Wollen Daten zentral anzeigen
    ax.errorbar(x=bin_center, y=hdata, yerr=hdataunc, fmt="ko", label="Daten")
    #ax.hist(hdata, label="Daten",  bins=bins)
    #ax.hist(bins[:-1], weights=hdata, label="Daten",  bins=bins)

    ### Nun Signal und Untegrund - die sind aufeinander aufgesetzt
    stack_x = [bins[:-1],bins[:-1]]
    stack_y = [hbkg, hsig]
    stack_label = ["Background", "Signal"]
    ax.hist(stack_x, weights=stack_y, label=stack_label, bins=bins, stacked=True)
    ### Logarithmische oder individuelle Achsen-Einstellungen
    bottom, top = ax.get_ylim()
    ax.set_xlim(bins[0],bins[-1]) #remove left/right margin
    left, right = ax.get_xlim()
    if args.yaxis_log:
        ax.set_yscale('log')
        ax.set_ylim(max(bottom,0.02),10.*top)
        if args.ratio:
            ax.set_ylim(max(bottom,0.02),25.*top)
    else:
        ax.set_ylim(bottom,1.1*top)
    if args.xaxis_log:
        ax.set_xscale('log')
    if args.xMin != -999 or args.xMax != -999:
        if args.xMin != -999:
            left = args.xMin
        if args.xMax != -999:
            right = args.xMax
        ax.set_xlim(left,right)
    if args.yMin != -999 or args.yMax != -999:
        if args.yMin != -999:
            bottom = args.yMin
        if args.yMax != -999:
            top = args.yMax
        ax.set_ylim(bottom,top)
    ### Darstellung der Legende, damit klar ist, was was zeigt
    ax.legend()
    ### Einige Extras, damit man weiss, was Daten bedeutet
    ax.text(0.02, 0.95, "ATLAS", weight="bold", transform=ax.transAxes)
    ax.text(0.125, 0.95, "Open Data", transform=ax.transAxes)
    ax.text(0.02, 0.90, r"13 TeV, 10 fb" + r"$^{-1}$", transform=ax.transAxes)
    ax.plot()

    ### Hier plotten wir den ratio plot, falls wir einen wollen
    if args.ratio:
        ###Erstelle das Verhaeltnis von Daten zu Simulation
        htot = hbkg+hsig # komplette Simulation von Untergrund plus Signal
        htot[htot == 0] = 1e-6
        htotunc = (hbkgunc**2 + hsigunc**2)**0.5
        hratio = hdata / htot
        hratiounc = ((hdataunc**2)/(htot**2)+((hdata**2)*(htotunc**2)/htot**4))**0.5
        ### Dies ist dann das Ratio-Histogramm als Plot
        ar.axline(xy1=(left,1.0), xy2=(right,1.0), color='tab:gray', lw=2,linestyle='--')#,colors='tab:gray',linestyles='dashed')
        ar.errorbar(x=bin_center, y=hratio, yerr=hratiounc, fmt="ko", label="Ratio")
        ###Auch hier muessen wir die Achsen einstellen
        ar.set_ylim(args.rMin,args.rMax)
        ar.set_xlim(bins[0],bins[-1]) #remove left/right margin
        if args.xMin != -999 or args.xMax != -999:
            left, right = 0, 0
            if args.xMin != -999:
                left = args.xMin
            if args.xMax != -999:
                right = args.xMax
            ar.set_xlim(left,right)
        ar.set_xlabel(args.xtitle) # z.B. "m\${}_{ll}\$ [GeV/c\${}^2\$]"
        ar.set_ylabel("Data / Sim.")
        ar.plot()
    plt.plot()
    if args.notSave and not args.ratio:
        plt.savefig(outdir+args.histname+".png")
        plt.savefig(outdir+args.histname+".pdf")
    elif args.notSave:
        plt.savefig(outdir+args.histname+"_ratio.png")
        plt.savefig(outdir+args.histname+"_ratio.pdf")
    if args.showPlot:
        plt.show()



if __name__ == "__main__":

    # Define options
    parser = argparse.ArgumentParser(description="Plotter for VVV analysis")
    parser.add_argument('-i' , '--indir'       , dest='indir'     , help='input directory where histograms are stored' , type=str  , required=False, default="HistogramData")
    parser.add_argument('-o' , '--outdir'      , dest='outdir'    , help='output directory where plot will be stored'  , type=str  , required=False, default="Plots")
    parser.add_argument('-hn', '--histname'    , dest='histname'  , help='Histogram to be plotted'                                 , type=str  , required=True)
    parser.add_argument('-ht', '--histtitle'   , dest='histtitle' , help='Title of histogram'                          , type=str  , required=False, default="")
    parser.add_argument('-xt', '--xtitle'      , dest='xtitle'    , help='Title of x axis'                             , type=str  , required=False, default="")
    parser.add_argument('-yt', '--ytitle'      , dest='ytitle'    , help='Title of y axis'                             , type=str  , required=False, default="")
    parser.add_argument('-ly', '--yaxis_log'   , dest='yaxis_log' , help='Y-axis set to log'                           ,                             default=False, action='store_true') 
    parser.add_argument('-lx', '--xaxis_log'   , dest='xaxis_log' , help='X-axis set to log'                           ,                             default=False, action='store_true') 
    parser.add_argument('-xn', '--xMin'        , dest='xMin'      , help='X-axis range setting'                        , type=float, required=False, default=-999) 
    parser.add_argument('-xx', '--xMax'        , dest='xMax'      , help='X-axis range setting'                        , type=float, required=False, default=-999)
    parser.add_argument('-yn', '--yMin'        , dest='yMin'      , help='Y-axis range setting'                        , type=float, required=False, default=-999) 
    parser.add_argument('-yx', '--yMax'        , dest='yMax'      , help='Y-axis range setting'                        , type=float, required=False, default=-999)  
    parser.add_argument('-sp', '--showPlot'    , dest='showPlot'  ,  help='Show directly the plot'                      ,                             default=False, action='store_true') 
    parser.add_argument('-ns', '--notSave'     , dest='notSave'   ,  help='Do not save the plot'                        ,                             default=True,  action='store_false') 
    parser.add_argument('-r' , '--ratio'       , dest='ratio'     ,  help='make a ratio plot'                           ,                             default=False, action='store_true')
    parser.add_argument('-rn', '--rMin'        , dest='rMin'      , help='ratio range setting'                         , type=float, required=False, default=0.5) 
    parser.add_argument('-rx', '--rMax'        , dest='rMax'      , help='ratio range setting'                         , type=float, required=False, default=1.5)  


    # Argument parser
    args = parser.parse_args()

    # Main
    main(args)

