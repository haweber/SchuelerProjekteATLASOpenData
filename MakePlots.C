#include <sys/stat.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <map>
#include <cmath>
#include <string>
#include <vector>
#include "TLatex.h"
#include "TLegend.h"
#include "TPad.h"
#include "TCanvas.h"
#include "THStack.h"
#include "TH1F.h"
#include "TH1.h"
#include "TLine.h"

#include "MakePlotBase.C"

using namespace std;



void MakePlots(string analysis="Z"){
  //bool MakePlot(string filelist, string outdir, string tag, string histname, float scale = 1, string histtitle="", string xtitle="", string ytitle="", bool yaxis_log = false, bool overflow = true, bool underflow = true, float xMin = -999, float xMax = -999., float yMin = -999., float yMax = -999., float rMin = 0.5, float rMax = 1.5, bool printsimple=false, bool printcsv=false, bool printlatex=false);

  if(analysis.find(std::string("Z")) != std::string::npos){
    MakePlot("ZPfad/output/filelist_Zll.txt","ZPfad/output/plots/","ZPfad","hMll",  1., "", "m_{ll} [GeV]",    "Events / 5 GeV",   true,  true, true, -999,-999,-999,-999,0.5,1.5,false,false,false);
    MakePlot("ZPfad/output/filelist_Zll.txt","ZPfad/output/plots/","ZPfad","hNLeps",1., "", "n_{leptons}",     "Events / 1",       false, true, true, -999,-999,-999,-999,0.5,1.5,false,false,false);
    MakePlot("ZPfad/output/filelist_Zll.txt","ZPfad/output/plots/","ZPfad","hLepPt",1., "", "lep-p_{T} [GeV]", "leptons / 10 GeV", true,  true, true, -999,-999,-999,-999,0.5,1.5,false,false,false);
  }
  else if(analysis.find(std::string("W")) != std::string::npos){
    MakePlot("WPfad/output/filelist_Wlnu.txt","WPfad/output/plots/","WPfad","hNLeps", 1., "", "n_{leptons}",        "Events / 1",       false, true, true, -999,-999,-999,-999,0.5,1.5,false,false,false);
    MakePlot("WPfad/output/filelist_Wlnu.txt","WPfad/output/plots/","WPfad","hETmiss",1., "", "p_{T}^{miss} [GeV]", "Events / 10 GeV",  true,  true, true, -999,-999,-999,-999,0.5,1.5,false,false,false);
    MakePlot("WPfad/output/filelist_Wlnu.txt","WPfad/output/plots/","WPfad","hLepPt", 1., "", "lep-p_{T} [GeV]",    "Events / 10 GeV",  true,  true, true, -999,-999,-999,-999,0.5,1.5,false,false,false);
    MakePlot("WPfad/output/filelist_Wlnu.txt","WPfad/output/plots/","WPfad","hMT",    1., "", "m_{T} [GeV]",        "Events / 5 GeV",   true,  true, true, -999,-999,-999,-999,0.5,1.5,false,false,false);
  }
  else if(analysis.find(std::string("H")) != std::string::npos){
    MakePlot("HPfad/output/filelist_HZZ.txt","HPfad/output/plots/","HPfad","hNLeps",  1., "", "n_{leptons}",        "Events / 1",       false, true, true, -999,-999,-999,-999,0.5,1.5,false,false,false);
    MakePlot("HPfad/output/filelist_HZZ.txt","HPfad/output/plots/","HPfad","hLepPt",  1., "", "lep-p_{T} [GeV]",    "leptons / 10 GeV", true,  true, true, -999,-999,-999,-999,0.5,1.5,false,false,false);
    MakePlot("HPfad/output/filelist_HZZ.txt","HPfad/output/plots/","HPfad","hMll_1",  1., "", "m_{ll}(Z_1) [GeV]",  "Events / 5 GeV",   true,  true, true, -999,-999,-999,-999,0.5,1.5,false,false,false);
    MakePlot("HPfad/output/filelist_HZZ.txt","HPfad/output/plots/","HPfad","hMll_2",  1., "", "m_{ll}(Z_2) [GeV]",  "Events / 5 GeV",   true,  true, true, -999,-999,-999,-999,0.5,1.5,false,false,false);
    MakePlot("HPfad/output/filelist_HZZ.txt","HPfad/output/plots/","HPfad","hMllll",  1., "", "m_{llll} [GeV]",     "Events / 5 GeV",   true,  true, true, -999,-999,-999,-999,0.5,1.5,false,false,false);
  }
  else
    std::cout << "Keine gueltige Analyse ausgewaehlt - nur ZPfad, WPfad oder HPfad moeglich. Gewaehlt: " << analysis << std::endl;

}


