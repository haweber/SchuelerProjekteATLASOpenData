{

  gROOT->ProcessLine(".L ScanChain.C+");

  TChain *ch = new TChain("mini"); 
  ch->Add("/lustre/fs22/group/atlas/haweber/SchuelerProjekte/ATLASOpenData/13TeV/2lep/MC/mc_361107.Zmumu.2lep.root");
  ScanChain(ch); 
}