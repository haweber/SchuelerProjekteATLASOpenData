#!/bin/env python

# option parser
import argparse
import sys
import os
import glob
import fnmatch
import ROOT
from inspect import currentframe, getframeinfo
import csv
import math
from MakePlotHelper import ColorTranslator

frameinfo = getframeinfo(currentframe())



#Hier ist die Hauptfunktion, um deine Histogramme in eine Grafik (Plot) ansehnlich darzustellen. In Prinzip solltest Du hier nichts schreiben muessen, da alle noetigen Optionen in der Commandline eingegeben werden koennen.
#Zwingende Eingaben:
#filelist: Wo sind deine Histogramme
#tag: ZPfad, HPfad, WPfad #not used yet
#outdir: In welchem Ordner soll der Plot abgespeichert werden?
#histname: Welches Histogramm moechtest du speziell plotten. Du kannst mehrere plotten, trenne Argumente mit einem Komma (,) aber keinem Leerzeichen ( ). Aber Vorsicht, wenn du verschiedene Flags gesetzt hast wie xMin, etc.
#Weitere Inputs gibt es weiter unten (auf englisch)
def main(args):

    #print ("")
    #print ("     -----------")
    #print ("       Plotter  ")
    #print ("     -----------")
    #print ("")

    ROOT.gStyle.SetOptStat(0);

    print("You are plotting histogram(s) " + args.histname + " for " + args.tag + " to output directory " + args.outdir)
    print("Files used are given in " + args.filelist)

    if not os.path.isfile(args.filelist):
        print("Given filelist (" + args.filelist + ") is not a file")
        return False
    if not os.access(args.filelist,os.R_OK):
        print("Given filelist (" + args.filelist + ") is not readable")
        return False

    histonames = args.histname.split(',')
    
    htemp = ROOT.TH1F()
    histos = dict()
    legnames = dict()
    colors = dict()
    isdata = dict()
    stacks = dict()

    
    leg = ROOT.TLegend(0.5,0.775,0.85,0.9025,"","brNDC")
    leg.SetBorderSize(0)
    leg.SetTextSize(0.033)
    leg.SetLineColor(1)
    leg.SetLineStyle(1)
    leg.SetLineWidth(2)
    leg.SetNColumns(2)
    leg.SetFillColor(0)
    leg.SetFillStyle(1001)
    
    with open(args.filelist,'r') as f:
        csvFile = csv.reader(filter(lambda row: row[0]!='#',f))
        for l in csvFile:
            sampleid,legname,color,filename=l[0],l[1],l[2],l[3]
            f = ROOT.TFile.Open(filename)
            ROOT.TH1.AddDirectory(0)
            for h in histonames:
                if h not in stacks:
                    stacks[h] = ROOT.THStack()
                hname = h+"_"+sampleid
                hnameMC = h+"_SimSum"
                htemp = f.Get(h)
                histos[hname] = htemp.Clone(hname)
                if args.overflow:
                    histos[hname].SetBinContent(histos[hname].GetNbinsX(),histos[hname].GetBinContent(histos[hname].GetNbinsX())+histos[hname].GetBinContent(histos[hname].GetNbinsX()+1))
                    histos[hname].SetBinError(histos[hname].GetNbinsX(),math.sqrt(math.pow(histos[hname].GetBinError(histos[hname].GetNbinsX()),2)+math.pow(histos[hname].GetBinError(histos[hname].GetNbinsX()+1),2)))
                if args.underflow:
                    histos[hname].SetBinContent(1,histos[hname].GetBinContent(1)+histos[hname].GetBinContent(0))
                    histos[hname].SetBinError(1,math.sqrt(math.pow(histos[hname].GetBinError(1),2)+math.pow(histos[hname].GetBinError(0),2)))
                legnames[hname] = legname
                colors[hname] = ColorTranslator(color)
                isdata[hname] = ('Data' in hname)
                histos[hname].SetTitle(args.histtitle)
                histos[hname].GetXaxis().SetTitle(args.xtitle)
                histos[hname].GetYaxis().SetTitleOffset(1.8)
                histos[hname].GetYaxis().SetTitle(args.ytitle)
                if isdata[hname]:
                    histos[hname].SetLineWidth(2) 
                    histos[hname].SetLineColor(1) #Data is black
                    histos[hname].SetMarkerColor(1) #Data is black
                    histos[hname].SetMarkerStyle(20)
                    if h == histonames[0]:
                        leg.AddEntry(histos[hname],legname,"ep")
                else:
                    if args.scale!=1:
                        histos[hname].Scale(args.scale)
                    if hnameMC not in histos:
                        histos[hnameMC] = histos[hname].Clone(hnameMC)
                        histos[hnameMC].SetLineWidth(2) 
                        histos[hnameMC].SetLineColor(1) 
                        histos[hnameMC].SetMarkerColor(1)
                        histos[hnameMC].SetFillColor(1)
                        histos[hnameMC].SetFillStyle(3544)
                    else:
                        histos[hnameMC].Add(histos[hname])
                    histos[hname].SetLineColor(colors[hname]) 
                    histos[hname].SetFillColor(colors[hname]) 
                    histos[hname].SetMarkerColor(colors[hname]) 
                    if h == histonames[0]:
                        leg.AddEntry(histos[hname],legname,"f")
                    stacks[h].Add(histos[hname])
                #print(hname,histos[hname].GetName(),legnames[hname],colors[hname],isdata[hname])
    for h in histonames:
        histos[h+"_Ratio"] = histos[h+"_Data"].Clone(h+"_Ratio")#This will fail if there is no data and simulation histograms
        histos[h+"_Ratio"].Divide(histos[h+"_SimSum"])

    tLumi = ROOT.TLatex(0.95,0.955,"10 fb^{-1} (13 TeV)")
    tLumi.SetNDC()
    tLumi.SetTextAlign(31)
    tLumi.SetTextFont(42)
    tLumi.SetTextSize(0.042)
    tLumi.SetLineWidth(2)
    tCMS = ROOT.TLatex(0.125,0.955,"ATLAS")
    tCMS.SetNDC()
    tCMS.SetTextAlign(11)
    tCMS.SetTextFont(61)
    tCMS.SetTextSize(0.0525)
    tCMS.SetLineWidth(2)
    tPrel = ROOT.TLatex(0.26,0.955,"Open Data")
    tPrel.SetNDC()
    tPrel.SetTextAlign(11)
    tPrel.SetTextFont(52)
    tPrel.SetTextSize(0.042)
    tPrel.SetLineWidth(2)

    outdirname = args.outdir
    if outdirname[-1] != '/':
        outdirname = outdirname + '/'
    if not os.path.exists(outdirname):
        os.makedirs(outdirname)
    

    for h in histonames:
        maximum = -1
        if args.yMax>0:
            maximum = args.yMax
        else:
            maximum = max(histos[h+"_SimSum"].GetMaximum(),histos[h+"_Data"].GetMaximum())*1.667
            if args.yaxis_log:
                maximum *= 40
        minimum = 0
        if args.yaxis_log:
            minimum = 0.2
        if args.yMin>0 and args.yMin<args.yMax:
            minimum = args.yMin
        #print  getframeinfo(currentframe()).lineno, h
        stacks[h].SetMaximum(maximum)
        histos[h+"_SimSum"].SetMaximum(maximum)
        histos[h+"_Data"].SetMaximum(maximum)
        stacks[h].SetMinimum(minimum)
        histos[h+"_SimSum"].SetMinimum(minimum)
        histos[h+"_Data"].SetMinimum(minimum)
        if args.xMin> (-990.) and args.xMin>=histos[h+"_Data"].GetBinLowEdge(1) and args.xMax>args.xMin and args.xMax<=histos[h+"_Data"].GetBinLowEdge(histos[h+"_Data"].GetNbinsX()+1):
            stacks[h].GetXaxis().SetRangeUser(args.xMin,args.xMax)
            histos[h+"_SimSum"].GetXaxis().SetRangeUser(args.xMin,args.xMax)
            histos[h+"_Data"].GetXaxis().SetRangeUser(args.xMin,args.xMax)
            histos[h+"_Ratio"].GetXaxis().SetRangeUser(args.xMin,args.xMax)
        histos[h+"_Ratio"].SetMaximum(args.rMax)
        histos[h+"_Ratio"].SetMinimum(args.rMin)

        c1 = ROOT.TCanvas("c1", "",334,192,600,600)
        c1.SetFillColor(0)
        c1.SetBorderMode(0)
        c1.SetBorderSize(2)
        c1.SetTickx(1)
        c1.SetTicky(1)
        c1.SetLeftMargin(0.18)
        c1.SetRightMargin(0.05)
        c1.SetTopMargin(0.07)
        c1.SetBottomMargin(0.15)
        c1.SetFrameFillStyle(0)
        c1.SetFrameBorderMode(0)
        c1.SetFrameFillStyle(0)
        c1.SetFrameBorderMode(0)
        plotpad = ROOT.TPad("plotpad", "Pad containing the overlay plot",0,0.165,1,1)
        plotpad.Draw()
        plotpad.cd()
        plotpad.SetFillColor(0)
        plotpad.SetBorderMode(0)
        plotpad.SetBorderSize(2)
        plotpad.SetTickx(1)
        plotpad.SetTicky(1)
        plotpad.SetLeftMargin(0.12)
        plotpad.SetRightMargin(0.04)
        plotpad.SetTopMargin(0.05)
        #plotpad.SetBottomMargin(0.15)
        plotpad.SetFrameFillStyle(0)
        plotpad.SetFrameBorderMode(0)
        plotpad.SetFrameFillStyle(0)
        plotpad.SetFrameBorderMode(0)
        if args.yaxis_log:
            plotpad.SetLogy()
        
        plotpad.cd()

        #stacks[h].GetXaxis().SetTitleSize(0)
        histos[h+"_SimSum"].GetXaxis().SetTitleSize(0)
        histos[h+"_Data"].GetXaxis().SetTitleSize(0)
        stacks[h].Draw("hist")
        stacks[h].SetHistogram(histos[h+"_SimSum"])
        stacks[h].Draw("hist")
        histos[h+"_SimSum"].Draw("sameE2")
        histos[h+"_Data"].Draw("sameE0X0")
        leg.Draw()
        tLumi.Draw()
        tCMS.Draw()
        tPrel.Draw()

        c1.cd()
        ratiopad = ROOT.TPad("ratiopad", "Pad containing the ratio",0,0,1,0.21)
        ratiopad.Draw()
        ratiopad.cd()
        ratiopad.SetFillColor(0)
        ratiopad.SetBorderMode(0)
        ratiopad.SetBorderSize(2)
        ratiopad.SetTickx(1)
        ratiopad.SetTicky(1)
        ratiopad.SetLeftMargin(0.12)
        ratiopad.SetRightMargin(0.04)
        ratiopad.SetBottomMargin(0.3)
        ratiopad.SetFrameFillStyle(0)
        ratiopad.SetFrameBorderMode(0)
        ratiopad.SetFrameFillStyle(0)
        ratiopad.SetFrameBorderMode(0)
    
        histos[h+"_Ratio"].GetXaxis().SetTitleSize(0.16)
        histos[h+"_Ratio"].GetXaxis().SetTitleOffset(0.76)
        histos[h+"_Ratio"].GetXaxis().SetLabelSize(0.0)
        histos[h+"_Ratio"].GetYaxis().SetNdivisions(504)
        histos[h+"_Ratio"].GetYaxis().SetTitle("data / sim")
        histos[h+"_Ratio"].GetYaxis().SetTitleSize(0.14)
        histos[h+"_Ratio"].GetYaxis().SetTitleOffset(0.28)
        histos[h+"_Ratio"].GetYaxis().SetLabelSize(0.14)
        histos[h+"_Ratio"].Draw()
        rline = ROOT.TLine(histos[h+"_Ratio"].GetXaxis().GetBinLowEdge(1),1.,histos[h+"_Ratio"].GetXaxis().GetBinLowEdge(histos[h+"_Ratio"].GetNbinsX()+1),1.)
        rline.SetLineWidth(2)
        rline.SetLineStyle(7)
        rline.Draw()
        outname = outdirname + h +'.pdf'
        c1.cd()
        c1.SaveAs(outname)
        c1.cd()
    
    return True



if __name__ == "__main__":

    # Define options
    parser = argparse.ArgumentParser(description="Plotter for VVV analysis")
    parser.add_argument('-f' , '--filelist'  , dest='filelist' , help='List of Files, through text file'            , type=str  , required=True)
    parser.add_argument('-o' , '--outdir'    , dest='outdir'   , help='output directory where file is stored'       , type=str  , required=True)
    parser.add_argument('-t' , '--tag'       , dest='tag'      , help='tag of analysis, either ZPfad, WPfad, HPfad' , type=str  , required=True)
    parser.add_argument('-s' , '--scale'     , dest='scale'    , help='scale simulation'                            , type=float, required=False, default=1.)
    parser.add_argument('-hn', '--histname'  , dest='histname' , help='name of the histogram'                       , type=str  , required=True)
    parser.add_argument('-ht', '--histtitle' , dest='histtitle', help='Title of histogram'                          , type=str  , required=False, default="")
    parser.add_argument('-xt', '--xtitle'    , dest='xtitle'   , help='Title of x axis'                             , type=str  , required=False, default="")
    parser.add_argument('-yt', '--ytitle'    , dest='ytitle'   , help='Title of y axis'                             , type=str  , required=False, default="")
    parser.add_argument('-l' , '--yaxis_log' , dest='yaxis_log', help='Y-axis set to log'                           ,                             default=False, action='store_true') 
    parser.add_argument('-of', '--overflow'  , dest='overflow' , help='Add overflow'                                ,                             default=False, action='store_true') 
    parser.add_argument('-uf', '--underflow' , dest='underflow', help='Add underflow'                               ,                             default=False, action='store_true') 
    parser.add_argument('-xn', '--xMin'      , dest='xMin'     , help='X-axis range setting'                        , type=float, required=False, default=-999.) 
    parser.add_argument('-xx', '--xMax'      , dest='xMax'     , help='X-axis range setting'                        , type=float, required=False, default=-999.)
    parser.add_argument('-yn', '--yMin'      , dest='yMin'     , help='Y-axis range setting'                        , type=float, required=False, default=-999.) 
    parser.add_argument('-yx', '--yMax'      , dest='yMax'     , help='Y-axis range setting'                        , type=float, required=False, default=-999.)  
    parser.add_argument('-rn', '--rMin'      , dest='rMin'     , help='ratio range setting'                         , type=float, required=False, default=0.5) 
    parser.add_argument('-rx', '--rMax'      , dest='rMax'     , help='ratio range setting'                         , type=float, required=False, default=1.5)  
    # Argument parser
    args = parser.parse_args()
    args.tag

    # Main
    main(args)
