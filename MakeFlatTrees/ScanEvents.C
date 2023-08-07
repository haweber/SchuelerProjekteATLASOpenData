// -*- C++ -*-
// Usage:
// > root -b -q doAll.C

#include <iostream>
#include <vector>

// ROOT
#include "TBenchmark.h"
#include "TChain.h"
#include "TDirectory.h"
#include "TFile.h"
#include "TROOT.h"
#include "TTreeCache.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TGraph.h"
#include "TGraphErrors.h"
#include "TGraphAsymmErrors.h"
#include "TLorentzVector.h"
#include "Math/Vector4D.h"
#include "Math/Vector4Dfwd.h"

// OpenTuple
#include "OpenTuple.cc"

using namespace std;
using namespace tpl;

//Function Headers go first:
//ScanEvents: 1.) Argument: das ntuple, welches wir studieren, 2.) Name der Ausgabedatei, wo die Resultate gespeichert werden, 3.) Ist es ein Datenfile oder eine Simulation, 4.) Schnelle Suche? 5.) Nur die ersten nEvents untersuchen, -1 bedeutet alle Events, 6.) skimFilePrefix, nicht benutzt
int ScanEvents(TChain* chain, string outname, bool isdata = false, bool fast = true, int nEvents = -1, string skimFilePrefix = "test", int nleptonfilter=-1);
//GetLorentzVector: Hilfsfunktion, um einen Lorentzvektor aufzubauen. Hier braeuchten wir diese Funktion nicht, aber es zeigt, wie man so eine Funktion verwendet.
ROOT::Math::PtEtaPhiEVector GetLorentzVector(float pt, float eta, float phi, float E);

//In diesem Makro haben wir zwei Funktionen bestimmt
//Die erste ist ScanEvents - die Hauptfunktion
//Die zweite ist GetLorentzVector - eine Hilfsfunktion, die in AnalyzeOneDataset aufgerufen wird

//Die Hauptfunktion, in der wir die Analyse durchfuehren
int ScanEvents(TChain* chain, string outname, bool isdata, bool fast, int nEvents, string skimFilePrefix, int nleptonfilter) {

  // Benchmark
  TBenchmark *bmark = new TBenchmark();
  bmark->Start("benchmark");

  // Example Histograms
  TDirectory *rootdir = gDirectory->GetDirectory("Rint:");

  //Am Anfang hier definieren wir unsere Histogramme, die wir fuellen wollen, also worin wir unsere Resultate darstellen
  //Im Beispiel zeige ich drei Histogramme, eines davon werden wir haeufiger betrachten.
  //Das Format ist so, dass wir zuerst den C-Variablen-Name initialisieren mit einem TH1F (1D histogram mit floating-point precision).
  //Dieses TH1F braucht 5 (4) Eingaben, zuerst der ROOT-Variablen-Name (wie ROOT das Histogramm speichert), einen beschreibenen Titel (Histogramm-Titel; x-Achsenbeschreibung; y-Achsenbeschreibung), die Anzahl von Abschnitten (nbins), sowie die Histogramm-Grenzen der x-Achse

  //float GeVconversion = 0.001;
  float GeVconversion = 1.;
  float lvconversion = 0.001;
  //float lvconversion = 1.;
  Float_t lep1_px;
  Float_t lep1_py;
  Float_t lep1_pz;
  Float_t lep1_E;
  Int_t lep1_id;
  Float_t lep2_px;
  Float_t lep2_py;
  Float_t lep2_pz;
  Float_t lep2_E;
  Int_t lep2_id;
  Float_t lep3_px;
  Float_t lep3_py;
  Float_t lep3_pz;
  Float_t lep3_E;
  Int_t lep3_id;
  Float_t lep4_px;
  Float_t lep4_py;
  Float_t lep4_pz;
  Float_t lep4_E;
  Int_t lep4_id;
  
  /*
  Float_t lep_px[4];
  Float_t lep_py[4];
  Float_t lep_pz[4];
  Float_t lep_energy[4];
  Int_t lep_Q[4];
  Int_t lep_id[4];
  */
  //Int_t nlep;
  Float_t met_px;
  Float_t met_py;  
  Double_t weight;
  Bool_t istriggered;

  string dummy = skimFilePrefix;
  TFile *newfile = new TFile(outname.c_str(),"recreate");
  newfile->cd();
  TTree *newtree = new TTree("events","skimmed ATLAS open data");
  
  newtree->Branch("lep1_px",&lep1_px,"lep1_px/F");
  newtree->Branch("lep1_py",&lep1_py,"lep1_py/F");
  newtree->Branch("lep1_pz",&lep1_pz,"lep1_pz/F");
  newtree->Branch("lep1_E" ,&lep1_E ,"lep1_E/F");
  newtree->Branch("lep2_px",&lep2_px,"lep2_px/F");
  newtree->Branch("lep2_py",&lep2_py,"lep2_py/F");
  newtree->Branch("lep2_pz",&lep2_pz,"lep2_pz/F");
  newtree->Branch("lep2_E" ,&lep2_E ,"lep2_E/F");
  newtree->Branch("lep3_px",&lep3_px,"lep3_px/F");
  newtree->Branch("lep3_py",&lep3_py,"lep3_py/F");
  newtree->Branch("lep3_pz",&lep3_pz,"lep3_pz/F");
  newtree->Branch("lep3_E" ,&lep3_E ,"lep3_E/F");
  newtree->Branch("lep4_px",&lep4_px,"lep4_px/F");
  newtree->Branch("lep4_py",&lep4_py,"lep4_py/F");
  newtree->Branch("lep4_pz",&lep4_pz,"lep4_pz/F");
  newtree->Branch("lep4_E" ,&lep4_E ,"lep4_E/F");
  newtree->Branch("lep1_id",&lep1_id,"lep1_id/I");
  newtree->Branch("lep2_id",&lep2_id,"lep2_id/I");
  newtree->Branch("lep3_id",&lep3_id,"lep3_id/I");
  newtree->Branch("lep4_id",&lep4_id,"lep4_id/I");
  
  newtree->Branch("met_px",&met_px,"met_px/F");
  newtree->Branch("met_py",&met_py,"met_py/F");

  newtree->Branch("weight",&weight,"weight/D");
  // newtree->Branch("istriggered",&istriggered,"istriggered/O");
  /*
  newtree->Branch("nlep",&nlep,"nlep/I");
  newtree->Branch("lep_px",lep_px,"lep_px[4]/F");
  newtree->Branch("lep_py",lep_py,"lep_py[4]/F");
  newtree->Branch("lep_pz",lep_pz,"lep_pz[4]/F");
  newtree->Branch("lep_energy" ,lep_energy ,"lep_energy[4]/F");
  newtree->Branch("lep_Q",lep_Q,"lep_Q[4]/I");
  newtree->Branch("lep_id",lep_id,"lep_id[4]/I");
  */
  
  // Loop over events to Analyze
  unsigned int nEventsTotal = 0;
  unsigned int nEventsChain = chain->GetEntries();
  if (nEvents >= 0) nEventsChain = nEvents;
  TObjArray *listOfFiles = chain->GetListOfFiles();
  TIter fileIter(listOfFiles);
  TFile *currentFile = 0;

  // File Loop
  // Hier: Unseres Format laesst es zu, dass es mehrere Dateien zusammen analysiert. Hier ist die Schlaufe durch diese Dateien
  while ( (currentFile = (TFile*)fileIter.Next()) ) {

    //std::cout << "Looping over file " << currentFile->GetTitle() << std::endl;
    // Get File Content
    //Hier holen wir die Information um das Format
    auto file = TFile::Open(currentFile->GetTitle());
    //TFile file(currentFile->GetTitle());
    TTree *tree = (TTree*)file->Get("mini");
    if (fast) TTreeCache::SetLearnEntries(10);
    if (fast) tree->SetCacheSize(128*1024*1024);
    opentuple.Init(tree);
    std::cout << "Looping over file " << currentFile->GetTitle() << std::endl;

    // Loop over Events in current file
    if (nEventsTotal >= nEventsChain) continue;
    unsigned int nEventsTree = tree->GetEntriesFast();
    //Jetzt sind wir bei der event-Loop. Hier laufen wir durch die Ereignisse, die im tuple gespeichert sind.
    for (unsigned int event = 0; event < nEventsTree; ++event) {

      // Get Event Content
      //Jedes event hat die Eigenschaften, die ATLAS hier angibt: http://opendata.atlas.cern/release/2020/documentation/datasets/dataset13.html
      //Bespreche mit deinem Betreuer, was diese bedeuten.
      //Hier laden wir diese Eigenschaften
      if (nEventsTotal >= nEventsChain) continue;
      if (fast) tree->LoadTree(event);
      opentuple.GetEntry(event);
      ++nEventsTotal;
      /*
      nlep = -999;
      for(int i = 0; i<4; ++i){
	lep_px[i] = -999.;
	lep_py[i] = -999.;
	lep_pz[i] = -999.;
	lep_energy[i] = -999.;
	lep_Q[i] = -999;
	lep_id[i] = -999;
      }
      */
      
      lep1_px = -999.;
      lep1_py = -999.;
      lep1_pz = -999.;
      lep1_E = -999.;
      lep1_id = -999;
      lep2_px = -999.;
      lep2_py = -999.;
      lep2_pz = -999.;
      lep2_E = -999.;
      lep2_id = -999;
      lep3_px = -999.;
      lep3_py = -999.;
      lep3_pz = -999.;
      lep3_E = -999.;
      lep3_id = -999;
      lep4_px = -999.;
      lep4_py = -999.;
      lep4_pz = -999.;
      lep4_E = -999.;
      lep4_id = -999;
      
      met_px = -999.;
      met_py = -999.;
      weight = 1.;
      istriggered = false;

      // Progress
      OpenTuple::progress( nEventsTotal, nEventsChain );

      // Analysis Code
      //Hier sind wir jetzt da, um unsere Analyse zu machen.

      //Zuerst brauchen wir ein Eventweight. Diese Gewichtung ist fuer die Simulation wichtig, allerdings soll Sie nicht fuer Daten geaendert werden.
      float eventweight = 1;
      if(!isdata){
	//Dieses Gewicht ist dafuer zustaendig, dass sich die Simulation sich an die Daten anschmiegt (beziehungsweise dies sollte)
	//Durch das OpenTuple Funktionalitaet, die ich geladen habe, kannst du die Branches (http://opendata.atlas.cern/release/2020/documentation/datasets/dataset13.html) als Funktion aufrufen.
	eventweight *= mcWeight()*scaleFactor_PILEUP()*scaleFactor_ELE()*scaleFactor_MUON()*scaleFactor_LepTRIGGER()*XSection()/SumWeights()*10000.;
      }
      weight = eventweight;
      //Nun schauen wir uns die Daten/Simulation an. Da wir nur Ereignisse wollen, die von Leptonentrigger selektiert wurden, machen wir hier eine Selektion.
      //Theoretisch sollten wir uns Elektronen und Muonen separat anschauen, aber fuer dieses Beispiel schauen wir es uns kombiniert an
      //if(!trigE() && !trigM())
      //continue;
      istriggered = trigE() || trigM();

      //Wir haben lep_n als Auswahl, aber wir schauen uns nur bestimmte Leptonen an. Unsere Selektion ist zwar schon in den ATLAS OpenData fuer uns getan, aber es ist gut, selbst eine Selektion zu bestimmen.
      //Zuerst testen wir, ob wir ueberhaupt gute Leptonen haben
      bool leptontriggereddata = false;
      int nleps = 0;
      int index = -1;
      for(unsigned int ilep = 0; ilep<lep_n(); ++ilep){
	//ilep zeigt den Index innerhalb der lep_n branches da. Man ruft diesen Eintrag mit [index] auf.
	if(lep_pt()[ilep] < 5.*1000.)//minimaler Impuls
	  continue;
	if(abs(lep_eta()[ilep]) > 2.5)//zentral im Detektor
	  continue;
	if(!lep_isTightID()[ilep])//klare Identifizierung als Lepton
	  continue;
	if(lep_ptcone30()[ilep]/lep_pt()[ilep]>0.15)//isoliert von anderen Objekten (Track basiert)
	  continue;
	if(lep_etcone20()[ilep]/lep_pt()[ilep]>0.15)//isoliert von anderen Objekten (Kalorimeter basiert)
	  continue;
	if(lep_type()[ilep]==11 && abs(lep_eta()[ilep])>1.37 && abs(lep_eta()[ilep])<1.52)//Besonderheit fuer Elektronen/Positronen
	  continue;
	//Die selektierten Leptonen sind nun gut.
	++nleps;
	if(lep_trigMatched()[ilep])
	  leptontriggereddata = true;
	ROOT::Math::PtEtaPhiEVector lvlep = GetLorentzVector(lep_pt()[ilep]*lvconversion,lep_eta()[ilep],lep_phi()[ilep],lep_E()[ilep]*lvconversion);
	/*
	unsigned int arrayindex = nleps - 1;
	lep_px[arrayindex] = lvlep.Px();
	lep_py[arrayindex] = lvlep.Py();
	lep_pz[arrayindex] = lvlep.Pz();
	lep_energy[arrayindex]  = lvlep.E();
	lep_Q[arrayindex] = lep_charge()[ilep];
	lep_id[arrayindex] = lep_type()[ilep];
	if(nleps>=4)
	  break;
	*/
	
	if(nleps==1){
	  lep1_px = lvlep.Px()*GeVconversion;
	  lep1_py = lvlep.Py()*GeVconversion;
	  lep1_pz = lvlep.Pz()*GeVconversion;
	  lep1_E  = lvlep.E()*GeVconversion;
	  lep1_id = lep_charge()[ilep]*lep_type()[ilep];
	}
	else if(nleps==2){
	  lep2_px = lvlep.Px()*GeVconversion;
	  lep2_py = lvlep.Py()*GeVconversion;
	  lep2_pz = lvlep.Pz()*GeVconversion;
	  lep2_E  = lvlep.E()*GeVconversion;
	  lep2_id = lep_charge()[ilep]*lep_type()[ilep];
	  //lep2_charge = lep_charge()[ilep];
	  //lep2_type = lep_type()[ilep];
	}
	else if(nleps==3){
	  lep3_px = lvlep.Px()*GeVconversion;
	  lep3_py = lvlep.Py()*GeVconversion;
	  lep3_pz = lvlep.Pz()*GeVconversion;
	  lep3_E  = lvlep.E()*GeVconversion;
	  lep3_id = lep_charge()[ilep]*lep_type()[ilep];
	  // lep3_charge = lep_charge()[ilep];
	  //lep3_type = lep_type()[ilep];
	}
	else if(nleps==4){
	  lep4_px = lvlep.Px()*GeVconversion;
	  lep4_py = lvlep.Py()*GeVconversion;
	  lep4_pz = lvlep.Pz()*GeVconversion;
	  lep4_E  = lvlep.E()*GeVconversion;
	  lep4_id = lep_charge()[ilep]*lep_type()[ilep];
	  //lep4_charge = lep_charge()[ilep];
	  //lep4_type = lep_type()[ilep];
	}
	else
	  break;
	
      }//ilep
      istriggered = istriggered && leptontriggereddata;
      if(!istriggered)
	continue;
      ROOT::Math::PtEtaPhiEVector lvmet = GetLorentzVector(met_et()*lvconversion, 0,met_phi(),met_et()*lvconversion);
      //nlep = nleps;
      met_px = lvmet.Px()*GeVconversion;
      met_py = lvmet.Py()*GeVconversion;
      if(nleptonfilter>0 && nleps < nleptonfilter)
	continue;
      newtree->Fill();
	    
    }//event
  
    // Clean Up
    delete tree;
    file->Close();
  }
  if (nEventsChain != nEventsTotal) {
    cout << Form( "ERROR: number of events from files (%d) is not equal to total number of events (%d)", nEventsChain, nEventsTotal ) << endl;
  }
  newfile->cd();
  newtree->Write();
  newfile->Close();
	
  // return
  bmark->Stop("benchmark");
  cout << endl;
  cout << nEventsTotal << " Events Processed" << endl;
  cout << "------------------------------" << endl;
  cout << "CPU  Time: " << Form( "%.01f", bmark->GetCpuTime("benchmark")  ) << endl;
  cout << "Real Time: " << Form( "%.01f", bmark->GetRealTime("benchmark") ) << endl;
  cout << endl;
  delete bmark;
  return 0;
}

//Einfache Hilfsfunktion
ROOT::Math::PtEtaPhiEVector GetLorentzVector(float pt, float eta, float phi, float E){
  ROOT::Math::PtEtaPhiEVector lvtemp = ROOT::Math::PtEtaPhiEVector(pt,eta,phi,E);
  if(lvtemp.M2()<0)
    lvtemp = ROOT::Math::PxPyPzMVector(lvtemp.Px(),lvtemp.Py(),lvtemp.Pz(),5e-1);//Mass is set to 0.5MeV = M(e)
  return lvtemp;
}
//need factor 2400 or 1/0.0004

