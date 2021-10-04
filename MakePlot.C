#include <sys/stat.h>
#include <iostream>
#include <fstream>
#include "map"



map<string, int> MyColor{
  { "kWhite"  , 0},
    { "kBlack"  , 1},
      { "kGray"   , 920},
	{ "kRed"    , 632},
	  { "kGreen"  , 416},
	    { "kBlue"   , 600},
	      { "kYellow" , 400},
		{ "kMagenta", 616},
		  { "kCyan"   , 432},
		    { "kOrange" , 800},
		      { "kSpring" , 820},
			{ "kTeal"   , 840},
			  { "kAzure"  , 860},
			    { "kViolet" , 880},
			      { "kPink"   , 900}
};

void MakeMultiplePlots();//gan am Ende
bool MakePlot(string filelist, string outdir, string tag, string histname, float scale = 1, string histtitle="", string xtitle="", string ytitle="", bool yaxis_log = false, bool overflow = true, bool underflow = true, float xMin = -999, float xMax = -999., float yMin = -999., float yMax = -999., float rMin = 0.5, float rMax = 1.5);
bool IsPathExist(const std::string &s);
int ColorTranslator(string s);
  
bool IsPathExist(const std::string &s)
{
  struct stat buffer;
  return (stat (s.c_str(), &buffer) == 0);
}

int ColorTranslator(string s){
  int colorintbase = 0;
  int colorintappend = 0;
  stringstream sss(s);
  string parsed;
  vector<string> separated;
  size_t posdel = s.find(string("+"));
  if(posdel!=std::string::npos){
    string color = s.substr(0, posdel);
    int number = stoi(s.substr(posdel+1,string::npos));
    return MyColor[color]+number;
  }
  posdel = s.find(string("-"));
  if(posdel!=std::string::npos){
    string color = s.substr(0, posdel);
    int number = stoi(s.substr(posdel+1,string::npos));
    return MyColor[color]-number;
    }
  return MyColor[s];
}

bool MakePlot(string filelist, string outdir, string tag, string histname, float scale, string histtitle, string xtitle, string ytitle, bool yaxis_log, bool overflow, bool underflow, float xMin, float xMax, float yMin, float yMax, float rMin, float rMax){

  gStyle->SetOptStat(0);

  map<string,TH1F*> histos;
  map<string,string> legnames;
  map<string,int> colors;
  map<string,bool> isdata;

  cout << "You are plotting histogram(s) " << histname << " for " << tag <<  " to output directory " << outdir << endl << "Files used are given in " << filelist << endl;
  string outname = outdir;
  if(outname.back()!=string("/")) outname += "/";
  if (!IsPathExist(outdir)){
    string pathmaker = "mkdir -p " + outname;
    gSystem->Exec(pathmaker.c_str());
  }
  outname += (histname + ".pdf");
  ifstream filelistSS(filelist);
  if (!filelistSS.good()) {
    std::cout << "No input filelist found " << filelist << std::endl;
    return false;							   
  }
  string filelistline;
  // Open an existing file
  THStack *stack = new THStack();
  TLegend *leg = new TLegend(0.5,0.775,0.85,0.9025,"","brNDC");
  leg->SetBorderSize(0);
  leg->SetTextSize(0.033);
  leg->SetLineColor(1);
  leg->SetLineStyle(1);
  leg->SetLineWidth(2);
  leg->SetNColumns(2);
  leg->SetFillColor(0);
  leg->SetFillStyle(1001);
  
  while(std::getline(filelistSS,filelistline, '\n')){
    if(filelistline.at(0)==string("#"))
      continue;
    size_t pos = 0;
    string delim = ",";
    vector<string> samplestemp;
    auto start = 0U;
    auto end = filelistline.find(delim);
    while (end != std::string::npos){
      samplestemp.push_back(filelistline.substr(start, end - start));
      start = end + delim.length();
      end = filelistline.find(delim, start);
    }
    samplestemp.push_back(filelistline.substr(start, end));
    string sampleid = samplestemp[0];
    string legname = samplestemp[1];
    int color = ColorTranslator(samplestemp[2]);
    string infilename = samplestemp[3];
    //for(unsigned int i = 0; i<samplestemp.size();++i) cout << samplestemp[i] << ";"; cout << endl;
    TFile *fin = TFile::Open(infilename.c_str());
    TH1F *htemp = (TH1F*)fin->Get(histname.c_str());
    string hname = histname + "_" + sampleid;
    string hnameMC = histname + "_SimSum";
    histos[hname] = (TH1F*)htemp->Clone(hname.c_str());
    bool is_data = false;
    if(hname.find("Data") != string::npos) is_data = true;
    isdata[hname] = is_data;
    if(overflow){
      histos[hname]->SetBinContent(histos[hname]->GetNbinsX(),histos[hname]->GetBinContent(histos[hname]->GetNbinsX())+histos[hname]->GetBinContent(histos[hname]->GetNbinsX()+1));
      histos[hname]->SetBinError(histos[hname]->GetNbinsX(),sqrt(pow(histos[hname]->GetBinError(histos[hname]->GetNbinsX()),2)+pow(histos[hname]->GetBinError(histos[hname]->GetNbinsX()+1),2)));
    }
    if(underflow){
      histos[hname]->SetBinContent(1,histos[hname]->GetBinContent(1)+histos[hname]->GetBinContent(0));
      histos[hname]->SetBinError(1,sqrt(pow(histos[hname]->GetBinError(1),2)+pow(histos[hname]->GetBinError(0),2)));
    }
    legnames[hname] = legname;
    colors[hname] = color;
    histos[hname]->SetTitle(histtitle.c_str());
    histos[hname]->GetXaxis()->SetTitle(xtitle.c_str());
    histos[hname]->GetYaxis()->SetTitleOffset(1.8);
    histos[hname]->GetYaxis()->SetTitle(ytitle.c_str());
    if(is_data){
      histos[hname]->SetLineWidth(2) ;
      histos[hname]->SetLineColor(1); //Data is black
      histos[hname]->SetMarkerColor(1); //Data is black
      histos[hname]->SetMarkerStyle(20);
      leg->AddEntry(histos[hname],legname.c_str(),"ep");
    }
    else{
      histos[hname]->Scale(scale);
      if(histos.count(hnameMC) == 0 ){
	histos[hnameMC] = (TH1F*)histos[hname]->Clone(hnameMC.c_str());
	histos[hnameMC]->SetLineWidth(2);
	histos[hnameMC]->SetLineColor(1);
	histos[hnameMC]->SetMarkerColor(1);
	histos[hnameMC]->SetFillColor(1);
	histos[hnameMC]->SetFillStyle(3544);
      }
      else{
	histos[hnameMC]->Add(histos[hname]);
      }
      
      histos[hname]->SetLineColor(colors[hname]);
      histos[hname]->SetFillColor(colors[hname]);
      histos[hname]->SetMarkerColor(colors[hname]);
      leg->AddEntry(histos[hname],legname.c_str(),"f");
      stack->Add(histos[hname]);
    }
  }
  //Got all histograms
  histos[histname+"_Ratio"] = (TH1F*)histos[histname+"_Data"]->Clone((histname+"_Ratio").c_str());
  histos[histname+"_Ratio"]->Divide(histos[histname+"_SimSum"]);
  
  TLatex *tLumi = new TLatex(0.95,0.955,"10 fb^{-1} (13 TeV)");
  tLumi->SetNDC();
  tLumi->SetTextAlign(31);
  tLumi->SetTextFont(42);
  tLumi->SetTextSize(0.042);
  tLumi->SetLineWidth(2);
  TLatex *tCMS = new TLatex(0.125,0.955,"ATLAS");
  tCMS->SetNDC();
  tCMS->SetTextAlign(11);
  tCMS->SetTextFont(61);
  tCMS->SetTextSize(0.0525);
  tCMS->SetLineWidth(2);
  TLatex *tPrel = new TLatex(0.26,0.955,"Open Data");
  tPrel->SetNDC();
  tPrel->SetTextAlign(11);
  tPrel->SetTextFont(52);
  tPrel->SetTextSize(0.042);
  tPrel->SetLineWidth(2);

  float maximum = -1;
  if(yMax>0){
    maximum = yMax;
  }
  else{
    maximum = max(histos[histname+"_SimSum"]->GetMaximum(),histos[histname+"_Data"]->GetMaximum())*1.6667;
    if(yaxis_log){
      maximum *= 40;
    }
  }
  float minimum = 0;
  if(yaxis_log){
    minimum = 0.2;
  }
  if(yMin>0 && yMin<yMax){
    minimum = yMin;
  }
  stack->SetMaximum(maximum);
  histos[histname+"_SimSum"]->SetMaximum(maximum);
  histos[histname+"_Data"]->SetMaximum(maximum);
  stack->SetMinimum(minimum);
  histos[histname+"_SimSum"]->SetMinimum(minimum);
  histos[histname+"_Data"]->SetMinimum(minimum);
  if(xMin> (-990.) && xMin>=histos[histname+"_Data"]->GetBinLowEdge(1) && xMax>xMin && xMax<=histos[histname+"_Data"]->GetBinLowEdge(histos[histname+"_Data"]->GetNbinsX()+1)){
    stack->GetXaxis()->SetRangeUser(xMin,xMax);
    histos[histname+"_SimSum"]->GetXaxis()->SetRangeUser(xMin,xMax);
    histos[histname+"_Data"]->GetXaxis()->SetRangeUser(xMin,xMax);
    histos[histname+"_Ratio"]->GetXaxis()->SetRangeUser(xMin,xMax);
  }
  histos[histname+"_Ratio"]->SetMaximum(rMax);
  histos[histname+"_Ratio"]->SetMinimum(rMin);
      
  TCanvas *c1 = new TCanvas("c1", "",334,192,600,600);
  c1->SetFillColor(0);
  c1->SetBorderMode(0);
  c1->SetBorderSize(2);
  c1->SetTickx(1);
  c1->SetTicky(1);
  c1->SetLeftMargin(0.18);
  c1->SetRightMargin(0.05);
  c1->SetTopMargin(0.07);
  c1->SetBottomMargin(0.15);
  c1->SetFrameFillStyle(0);
  c1->SetFrameBorderMode(0);
  c1->SetFrameFillStyle(0);
  c1->SetFrameBorderMode(0);
  TPad *plotpad = new TPad("plotpad", "Pad containing the overlay plot",0,0.165,1,1);
  plotpad->Draw();
  plotpad->cd();
  plotpad->SetFillColor(0);
  plotpad->SetBorderMode(0);
  plotpad->SetBorderSize(2);
  plotpad->SetTickx(1);
  plotpad->SetTicky(1);
  plotpad->SetLeftMargin(0.12);
  plotpad->SetRightMargin(0.04);
  plotpad->SetTopMargin(0.05);
  //plotpad->SetBottomMargin(0.15);
  plotpad->SetFrameFillStyle(0);
  plotpad->SetFrameBorderMode(0);
  plotpad->SetFrameFillStyle(0);
  plotpad->SetFrameBorderMode(0);
  if (yaxis_log){
    plotpad->SetLogy();
  }
  plotpad->cd();

  histos[histname+"_SimSum"]->GetXaxis()->SetTitleSize(0);
  histos[histname+"_Data"]->GetXaxis()->SetTitleSize(0);
  stack->Draw("hist");
  stack->SetHistogram(histos[histname+"_SimSum"]);
  stack->Draw("hist");
  histos[histname+"_SimSum"]->Draw("sameE2");
  histos[histname+"_Data"]->Draw("sameE0X0");
  leg->Draw();
  tLumi->Draw();
  tCMS->Draw();
  tPrel->Draw();

  c1->cd();
  TPad *ratiopad = new TPad("ratiopad", "Pad containing the ratio",0,0,1,0.21);
  ratiopad->Draw();
  ratiopad->cd();
  ratiopad->SetFillColor(0);
  ratiopad->SetBorderMode(0);
  ratiopad->SetBorderSize(2);
  ratiopad->SetTickx(1);
  ratiopad->SetTicky(1);
  ratiopad->SetLeftMargin(0.12);
  ratiopad->SetRightMargin(0.04);
  ratiopad->SetBottomMargin(0.3);
  ratiopad->SetFrameFillStyle(0);
  ratiopad->SetFrameBorderMode(0);
  ratiopad->SetFrameFillStyle(0);
  ratiopad->SetFrameBorderMode(0);
    
  histos[histname+"_Ratio"]->GetXaxis()->SetTitleSize(0.16);
  histos[histname+"_Ratio"]->GetXaxis()->SetTitleOffset(0.76);
  histos[histname+"_Ratio"]->GetXaxis()->SetLabelSize(0.0);
  histos[histname+"_Ratio"]->GetYaxis()->SetNdivisions(504);
  histos[histname+"_Ratio"]->GetYaxis()->SetTitle("data / sim");
  histos[histname+"_Ratio"]->GetYaxis()->SetTitleSize(0.14);
  histos[histname+"_Ratio"]->GetYaxis()->SetTitleOffset(0.28);
  histos[histname+"_Ratio"]->GetYaxis()->SetLabelSize(0.14);
  histos[histname+"_Ratio"]->Draw();
  TLine *rline = new TLine(histos[histname+"_Ratio"]->GetXaxis()->GetBinLowEdge(1),1.,histos[histname+"_Ratio"]->GetXaxis()->GetBinLowEdge(histos[histname+"_Ratio"]->GetNbinsX()+1),1.);
  rline->SetLineWidth(2);
  rline->SetLineStyle(7);
  rline->Draw();
  c1->cd();
  c1->SaveAs(outname.c_str());
  c1->cd();

  delete tLumi;
  delete tCMS;
  delete tPrel;
  delete leg;
  delete rline;
  delete stack;
  delete ratiopad;
  delete plotpad;
  delete c1;
    
  return true;

}




void MakeMultiplePlots(){
  //bool MakePlot(string filelist, string outdir, string tag, string histname, float scale = 1, string histtitle="", string xtitle="", string ytitle="", bool yaxis_log = false, bool overflow = true, bool underflow = true, float xMin = -999, float xMax = -999., float yMin = -999., float yMax = -999., float rMin = 0.5, float rMax = 1.5);

  MakePlot("ZPfad/output/filelist_Zll.txt","ZPfad/output/plots/","ZPfad","hMll",  1., "", "m_{ll} [GeV]",    "Events / 5 GeV",   true,  true, true, -999,-999,-999,-999,0.5,1.5);
  MakePlot("ZPfad/output/filelist_Zll.txt","ZPfad/output/plots/","ZPfad","hNLeps",1., "", "n_{leptons}",     "Events / 1",       false, true, true, -999,-999,-999,-999,0.5,1.5);
  MakePlot("ZPfad/output/filelist_Zll.txt","ZPfad/output/plots/","ZPfad","hLepPt",1., "", "lep-p_{T} [GeV]", "leptons / 10 GeV", true,  true, true, -999,-999,-999,-999,0.5,1.5);

}
