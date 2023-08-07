{

  //Hier kompilieren das Hauptskript ScanEvents.C
  gROOT->ProcessLine(".L ScanEvents.C+");

  //string basepath = "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/"; //from internet
  //string basepath = "http://opendata.cern.ch/eos/opendata/atlas/OutreachDatasets/2020-01-22/4lep/"; //from internet
  string basepath = "/lustre/fs22/group/atlas/haweber/SchuelerProjekte/ATLASOpenData/13TeV/4lep/"; //local path
  cout << "Basepath is " << basepath << endl;

  //Wir laden alle Daten-Dateien in eine TChain, und analysieren Sie mit ScanEvents
  TChain *chData = new TChain("mini"); 
  chData->Add((basepath+"Data/data_A.4lep.root").c_str());
  chData->Add((basepath+"Data/data_B.4lep.root").c_str());
  chData->Add((basepath+"Data/data_C.4lep.root").c_str());
  chData->Add((basepath+"Data/data_D.4lep.root").c_str());
  ScanEvents(chData, "output/data.root", true);

  TChain *chHZZ = new TChain("mini"); 
  chHZZ->Add((basepath+"MC/mc_345060.ggH125_ZZ4lep.4lep.root").c_str());
  chHZZ->Add((basepath+"MC/mc_344235.VBFH125_ZZ4lep.4lep.root").c_str());
  chHZZ->Add((basepath+"MC/mc_341947.ZH125_ZZ4lep.4lep.root").c_str());
  chHZZ->Add((basepath+"MC/mc_341964.WH125_ZZ4lep.4lep.root").c_str());
  ScanEvents(chHZZ, "output/mc_HZZ.root", false);
  
  TChain *chBkg = new TChain("mini"); 
  chBkg->Add((basepath+"MC/mc_363490.llll.4lep.root").c_str());//diboson mit ZZ bosonen
  chBkg->Add((basepath+"MC/mc_363491.lllv.4lep.root").c_str());//diboson mit WZ bosonen
  chBkg->Add((basepath+"MC/mc_361106.Zee.4lep.root").c_str());//Z bosonen
  chBkg->Add((basepath+"MC/mc_361107.Zmumu.4lep.root").c_str());//Z bosonen
  chBkg->Add((basepath+"MC/mc_361108.Ztautau.4lep.root").c_str());//Z bosonen
  ScanEvents(chBkg, "output/mc_llllBackground.root", false); 
}
