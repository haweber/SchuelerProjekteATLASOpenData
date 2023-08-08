{ // a simple wrapper for ScanEvents with data samples already defined.
  gROOT->ProcessLine(".L ScanEvents.C+");

  int nleps=4;//this needs to be 1, 2 or 4
  
  string basepath = "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/"; //from internet
  string lepstring = "";
  if(nleps==1) lepstring = "1lep";
  else if(nleps==2) lepstring = "2lep";
  else if(nleps==4) lepstring = "4lep";

  basepath = basepath + lepstring + "/";

  TChain *chData = new TChain("mini"); 
  chData->Add((basepath+"Data/data_A."+lepstring+".root").c_str());
  chData->Add((basepath+"Data/data_B."+lepstring+".root").c_str());
  chData->Add((basepath+"Data/data_C."+lepstring+".root").c_str());
  chData->Add((basepath+"Data/data_D."+lepstring+".root").c_str());
  ScanEvents(chData, "OutputTrees/data_"+lepstring+".root", true,true,-1,"",nleps);

  TChain *chSig = new TChain("mini"); 
  TChain *chBkg = new TChain("mini"); 

  if(nleps==1){
    
    chSig->Add((basepath+"MC/mc_361100.Wplusenu."+lepstring+".root").c_str());
    chSig->Add((basepath+"MC/mc_361101.Wplusmunu."+lepstring+".root").c_str());
    chSig->Add((basepath+"MC/mc_361102.Wplustaunu."+lepstring+".root").c_str());
    chSig->Add((basepath+"MC/mc_361103.Wminusenu."+lepstring+".root").c_str());
    chSig->Add((basepath+"MC/mc_361104.Wminusmunu."+lepstring+".root").c_str());
    chSig->Add((basepath+"MC/mc_361105.Wminustaunu."+lepstring+".root").c_str());
    ScanEvents(chSig, "OutputTrees/simulation_signal_"+lepstring+".root", false,true,-1,"",nleps);
    
    chBkg->Add((basepath+"MC/mc_361106.Zee."+lepstring+".root").c_str());
    chBkg->Add((basepath+"MC/mc_361107.Zmumu."+lepstring+".root").c_str());
    chBkg->Add((basepath+"MC/mc_361108.Ztautau."+lepstring+".root").c_str());
    chBkg->Add((basepath+"MC/mc_363359.WpqqWmlv."+lepstring+".root").c_str());
    chBkg->Add((basepath+"MC/mc_363360.WplvWmqq."+lepstring+".root").c_str());
    chBkg->Add((basepath+"MC/mc_363489.WlvZqq."+lepstring+".root").c_str());
    chBkg->Add((basepath+"MC/mc_410000.ttbar_lep."+lepstring+".root").c_str());
    ScanEvents(chBkg, "OutputTrees/simulation_background_"+lepstring+".root", false,true,-1,"",nleps);
  }
  if(nleps==2){
    chSig->Add((basepath+"MC/mc_361106.Zee."+lepstring+".root").c_str());
    chSig->Add((basepath+"MC/mc_361107.Zmumu."+lepstring+".root").c_str());
    chSig->Add((basepath+"MC/mc_361108.Ztautau."+lepstring+".root").c_str());
    ScanEvents(chSig, "OutputTrees/simulation_signal_"+lepstring+".root", false,true,-1,"",nleps);
  
    chBkg->Add((basepath+"MC/mc_410000.ttbar_lep."+lepstring+".root").c_str());
    chBkg->Add((basepath+"MC/mc_363492.llvv."+lepstring+".root").c_str());
    ScanEvents(chBkg, "OutputTrees/simulation_background_"+lepstring+".root", false,true,-1,"",nleps);
  }
  if(nleps==4){
    chSig->Add((basepath+"MC/mc_341947.ZH125_ZZ4lep."+lepstring+".root").c_str());
    chSig->Add((basepath+"MC/mc_341964.WH125_ZZ4lep."+lepstring+".root").c_str());
    chSig->Add((basepath+"MC/mc_344235.VBFH125_ZZ4lep."+lepstring+".root").c_str());
    chSig->Add((basepath+"MC/mc_345060.ggH125_ZZ4lep."+lepstring+".root").c_str());
    ScanEvents(chSig, "OutputTrees/simulation_signal_"+lepstring+".root", false,true,-1,"",nleps);
  
    chBkg->Add((basepath+"MC/mc_345337.ZH125J_llWW2lep."+lepstring+".root").c_str());
    chBkg->Add((basepath+"MC/mc_363490.llll."+lepstring+".root").c_str());
    chBkg->Add((basepath+"MC/mc_363491.lllv."+lepstring+".root").c_str());
    chBkg->Add((basepath+"MC/mc_410000.ttbar_lep."+lepstring+".root").c_str());
    //ttX samples are bugged - their cross section is wrong
    //chBkg->Add((basepath+"MC/mc_410155.ttW."+lepstring+".root").c_str());
    //chBkg->Add((basepath+"MC/mc_410218.ttee."+lepstring+".root").c_str());
    //chBkg->Add((basepath+"MC/mc_410219.ttmumu."+lepstring+".root").c_str());
    ScanEvents(chBkg, "OutputTrees/simulation_background_"+lepstring+".root", false,true,-1,"",nleps);
  }
  
}
