{

  //Hier kompilieren das Hauptskript ScanEvents.C
  gROOT->ProcessLine(".L EreignisAnalyse.C+");
  gROOT->ProcessLine(".L ScanEvents.C+");

  //string basepath = "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/2lep/"; //from internet
  string basepath = "/lustre/fs22/group/atlas/haweber/SchuelerProjekte/ATLASOpenData/13TeV/2lep/"; //local path

  //Wir laden alle Daten-Dateien in eine TChain, und analysieren Sie mit ScanEvents
  TChain *chData = new TChain("mini"); 
  chData->Add((basepath+"Data/data_A.2lep.root").c_str());
  chData->Add((basepath+"Data/data_B.2lep.root").c_str());
  chData->Add((basepath+"Data/data_C.2lep.root").c_str());
  chData->Add((basepath+"Data/data_D.2lep.root").c_str());
  ScanEvents(chData, "output/data.root", true);

  TChain *chZll = new TChain("mini"); 
  chZll->Add((basepath+"MC/mc_361106.Zee.2lep.root").c_str());
  chZll->Add((basepath+"MC/mc_361107.Zmumu.2lep.root").c_str());
  chZll->Add((basepath+"MC/mc_361108.Ztautau.2lep.root").c_str());
  ScanEvents(chZll, "output/mc_Zll.root", false);
  
  TChain *chBkg = new TChain("mini"); 
  chBkg->Add((basepath+"MC/mc_410000.ttbar_lep.2lep.root").c_str());
  chBkg->Add((basepath+"MC/mc_363492.llvv.2lep.root").c_str());
  ScanEvents(chBkg, "output/mc_llBackground.root", false); 
}
