{

  //Hier kompilieren das Hauptskript ScanEvents.C
  gROOT->ProcessLine(".L ScanEvents.C+");

  //string basepath = "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1lep/"; //from internet
  //string basepath = "http://opendata.cern.ch/eos/opendata/atlas/OutreachDatasets/2020-01-22/1lep/"; //from internet
  string basepath = "/lustre/fs22/group/atlas/haweber/SchuelerProjekte/ATLASOpenData/13TeV/1lep/"; //local path
  cout << "Basepath is " << basepath << endl;

  //Wir laden alle Daten-Dateien in eine TChain, und analysieren Sie mit ScanEvents
  TChain *chData = new TChain("mini"); 
  chData->Add((basepath+"Data/data_A.1lep.root").c_str());
  chData->Add((basepath+"Data/data_B.1lep.root").c_str());
  chData->Add((basepath+"Data/data_C.1lep.root").c_str());
  chData->Add((basepath+"Data/data_D.1lep.root").c_str());
  ScanEvents(chData, "output/data.root", true);

  TChain *chWlnu = new TChain("mini"); 
  chWlnu->Add((basepath+"MC/mc_361100.Wplusenu.1lep.root").c_str());
  chWlnu->Add((basepath+"MC/mc_361101.Wplusmunu.1lep.root").c_str());
  chWlnu->Add((basepath+"MC/mc_361102.Wplustaunu.1lep.root").c_str());
  chWlnu->Add((basepath+"MC/mc_361103.Wminusenu.1lep.root").c_str());
  chWlnu->Add((basepath+"MC/mc_361104.Wminusmunu.1lep.root").c_str());
  chWlnu->Add((basepath+"MC/mc_361105.Wminustaunu.1lep.root").c_str());
  ScanEvents(chWlnu, "output/mc_Wlnu.root", false);
  
  TChain *chBkg = new TChain("mini"); 
  chBkg->Add((basepath+"MC/mc_410000.ttbar_lep.1lep.root").c_str());//ttbar
  chBkg->Add((basepath+"MC/mc_363492.llvv.1lep.root").c_str());//diboson mit W bosonen
  chBkg->Add((basepath+"MC/mc_363493.lvvv.1lep.root").c_str());//diboson mit W bosonen
  chBkg->Add((basepath+"MC/mc_363359.WpqqWmlv.1lep.root").c_str());//diboson mit W bosonen
  chBkg->Add((basepath+"MC/mc_363360.WplvWmqq.1lep.root").c_str());//diboson mit W bosonen
  chBkg->Add((basepath+"MC/mc_363489.WlvZqq.1lep.root").c_str());//diboson mit W bosonen
  chBkg->Add((basepath+"MC/mc_361106.Zee.1lep.root").c_str());//Z bosonen
  chBkg->Add((basepath+"MC/mc_361107.Zmumu.1lep.root").c_str());//Z bosonen
  chBkg->Add((basepath+"MC/mc_361108.Ztautau.1lep.root").c_str());//Z bosonen
  //chBkg->Add((basepath+"MC/mc_410011.single_top_tchan.1lep.root").c_str());//single-t
  //chBkg->Add((basepath+"MC/mc_410012.single_antitop_tchan.1lep.root").c_str());//single-t
  //chBkg->Add((basepath+"MC/mc_410025.single_top_schan.1lep.root").c_str());//single-t
  //chBkg->Add((basepath+"MC/mc_410026.single_antitop_schan.1lep.root").c_str());//single-t
  //chBkg->Add((basepath+"MC/mc_410013.single_top_wtchan.1lep.root").c_str());//single-t
  //chBkg->Add((basepath+"MC/mc_410014.single_antitop_wtchan.1lep.root").c_str());//single-t
  ScanEvents(chBkg, "output/mc_lBackground.root", false); 
}
