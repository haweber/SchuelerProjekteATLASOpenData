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
#include "../OpenTuple.cc"

using namespace std;
using namespace tpl;

//Function Headers go first:
//ScanEvents: 1.) Argument: das ntuple, welches wir studieren, 2.) Name der Ausgabedatei, wo die Resultate gespeichert werden, 3.) Ist es ein Datenfile oder eine Simulation, 4.) Schnelle Suche? 5.) Nur die ersten nEvents untersuchen, -1 bedeutet alle Events, 6.) skimFilePrefix, nicht benutzt
int ScanEvents(TChain* chain, string outname, bool isdata = false, bool fast = true, int nEvents = -1, string skimFilePrefix = "test");
//GetLorentzVector: Hilfsfunktion, um einen Lorentzvektor aufzubauen. Hier braeuchten wir diese Funktion nicht, aber es zeigt, wie man so eine Funktion verwendet.
ROOT::Math::PtEtaPhiEVector GetLorentzVector(float pt, float eta, float phi, float E);

//In diesem Makro haben wir zwei Funktionen bestimmt
//Die erste ist ScanEvents - die Hauptfunktion
//Die zweite ist GetLorentzVector - eine Hilfsfunktion, die in AnalyzeOneDataset aufgerufen wird

//Die Hauptfunktion, in der wir die Analyse durchfuehren
int ScanEvents(TChain* chain, string outname, bool isdata, bool fast, int nEvents, string skimFilePrefix) {
  float _MZ = 91.18;//Z Bosonen-Masse

  // Benchmark
  TBenchmark *bmark = new TBenchmark();
  bmark->Start("benchmark");

  // Example Histograms
  TDirectory *rootdir = gDirectory->GetDirectory("Rint:");

  //Am Anfang hier definieren wir unsere Histogramme, die wir fuellen wollen, also worin wir unsere Resultate darstellen
  //Im Beispiel zeige ich drei Histogramme, eines davon werden wir haeufiger betrachten.
  //Das Format ist so, dass wir zuerst den C-Variablen-Name initialisieren mit einem TH1F (1D histogram mit floating-point precision).
  //Dieses TH1F braucht 5 (4) Eingaben, zuerst der ROOT-Variablen-Name (wie ROOT das Histogramm speichert), einen beschreibenen Titel (Histogramm-Titel; x-Achsenbeschreibung; y-Achsenbeschreibung), die Anzahl von Abschnitten (nbins), sowie die Histogramm-Grenzen der x-Achse
  TH1F *hNLeps  = new TH1F("hNLeps",  "Example plot: Number of leptons; Number of leptons ; Events ",          7,-0.5,6.5);
  TH1F *hNLepsT = new TH1F("hNLepsT", "Example plot: Number of triggering leptons; Number of triggering leptons ; Events ",          5,-0.5,4.5);
  TH1F *hLepPt  = new TH1F("hLepPt",  "Example plot: pT of leptons; p_{T} [GeV] ; Events times N_{leptons} ", 25,   0,250);
  TH1F *hMll_1  = new TH1F("hMll_1",  "Example plot: Dilepton invariant mass, leading mass; m_{ll}^{(1)} [GeV] ; Events ",       30,   0,150);
  TH1F *hMll_2  = new TH1F("hMll_2",  "Example plot: Dilepton invariant mass, subleading mass; m_{ll}^{(2)} [GeV] ; Events ",       30,   0,150);
  TH1F *hMllll  = new TH1F("hMllll",  "Example plot: 4-lepton invariant mass; m_{llll} [GeV] ; Events ",       100,   0,500);
  hNLeps ->SetDirectory(rootdir); hNLeps ->Sumw2();
  hNLepsT->SetDirectory(rootdir); hNLepsT->Sumw2();
  hLepPt ->SetDirectory(rootdir); hLepPt ->Sumw2();
  hMll_1 ->SetDirectory(rootdir); hMll_1 ->Sumw2();
  hMll_2 ->SetDirectory(rootdir); hMll_2 ->Sumw2();
  hMllll ->SetDirectory(rootdir); hMllll ->Sumw2();
  
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

    // Get File Content
    //Hier holen wir die Information um das Format
    TFile file(currentFile->GetTitle());
    TTree *tree = (TTree*)file.Get("mini");
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
      //Nun schauen wir uns die Daten/Simulation an. Da wir nur Ereignisse wollen, die von Leptonentrigger selektiert wurden, machen wir hier eine Selektion.
      //Theoretisch sollten wir uns Elektronen und Muonen separat anschauen, aber fuer dieses Beispiel schauen wir es uns kombiniert an
      if(!trigE() && !trigM())
	continue;

      //Wir haben lep_n als Auswahl, aber wir schauen uns nur bestimmte Leptonen an. Unsere Selektion ist zwar schon in den ATLAS OpenData fuer uns getan, aber es ist gut, selbst eine Selektion zu bestimmen.
      //Zuerst testen wir, ob wir ueberhaupt gute Leptonen haben
      bool leptontriggereddata = false;
      int nlepsT = 0;//triggering leptons
      int nleps = 0;//selection
      vector<int> indices; indices.clear();
      for(unsigned int ilep = 0; ilep<lep_n(); ++ilep){
	//ilep zeigt den Index innerhalb der lep_n branches da. Man ruft diesen Eintrag mit [index] auf.

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
	//Die selektierten Leptonen sind nun gut - bis auf Impuls: hier haben wir zwei Selektionen
	if(lep_pt()[ilep] < 7.*1000.)//minimaler Impuls
	  continue;
	++nleps;
	indices.push_back(ilep);
	hLepPt->Fill(lep_pt()[ilep]/1000., eventweight);//Hier haben wir noch keine Triggerselektion auf das Lepton - Daten/Simulation koennten nicht uebereinstimmen.
	if(lep_pt()[ilep] < 25.*1000.)//minimaler Impuls
	  continue;
	++nlepsT;
	if(lep_trigMatched()[ilep])
	  leptontriggereddata = true;
      }//ilep
      if(!leptontriggereddata)
	continue;
      
      hNLeps->Fill(nleps, eventweight);
      hNLepsT->Fill(nlepsT, eventweight);
      if(nleps>=4) {
	//Dies ist die Selektierung der HZZ Analyse von ATLAS bezueglich vom Impuls
	if(lep_pt()[indices[0] ] < 25.*1000.) continue;
	if(lep_pt()[indices[1] ] < 15.*1000.) continue;
	if(lep_pt()[indices[2] ] < 20.*1000.) continue;
	if(lep_pt()[indices[3] ] <  7.*1000.) continue;
	//wir haben die Indizes fuer Mllll.
	//Allerdings gibt es hier einige Selektionen: Wir wollen zwei Z-Zerfaelle, also zwei Paare e+e- oder mu+mu-. D.h. H --> e+e-e+e-, e+e-mu+mu-, mu+mu-mu+mu-
	//Da diese Variable nicht sehr einfach zu berechnen ist, Habe ich hier die Berechnung aufgeschrieben. Was ich hier mache ist ein LorenzVektor aus den zwei Leptonen bauen, und die Masse mit der LorentzVector internen Funktion bestimmen.
	//Die Formel dafuer findest du z.B. hier: https://en.wikipedia.org/wiki/Invariant_mass#Example:_two-particle_collision
	//Ein Lorentzvektor ist z.B. hier beschrieben: https://de.wikipedia.org/wiki/Vierervektor
	ROOT::Math::PtEtaPhiEVector lvZ1, lvZ2;
	//diese Zeile hilft mir schneller zu programmieren
	int i1 = indices[0]; int i2 = indices[1]; int i3 = indices[2]; int i4 = indices[3];
	ROOT::Math::PtEtaPhiEVector lvlep1 = GetLorentzVector(lep_pt()[i1],lep_eta()[i1],lep_phi()[i1],lep_E()[i1]);
	ROOT::Math::PtEtaPhiEVector lvlep2 = GetLorentzVector(lep_pt()[i2],lep_eta()[i2],lep_phi()[i2],lep_E()[i2]);
	ROOT::Math::PtEtaPhiEVector lvlep3 = GetLorentzVector(lep_pt()[i3],lep_eta()[i3],lep_phi()[i3],lep_E()[i3]);
	ROOT::Math::PtEtaPhiEVector lvlep4 = GetLorentzVector(lep_pt()[i4],lep_eta()[i4],lep_phi()[i4],lep_E()[i4]);
	//dM ist Abstand zur Z-Bosonenmasse
    float dM = 99999.;
	if(((lep_type()[i1]==lep_type()[i2])&&(lep_charge()[i1] != lep_charge()[i2])) && ((lep_type()[i3]==lep_type()[i4])&&(lep_charge()[i3] != lep_charge()[i4])) ){
	  float M1 = (lvlep1+lvlep2).M()/1000.;
	  float M2 = (lvlep3+lvlep4).M()/1000.;
	  if(abs(M1-_MZ)<abs(M2-_MZ)){
	    //M1 ist die Masse naeher an der Z-Masse
	    if(abs(M1-_MZ)<dM){
	      //M1 is naeher an der Z-Masse als davor getestete Kombinationen
	      lvZ1 = (lvlep1+lvlep2);
	      lvZ2 = (lvlep3+lvlep4);
	      dM = abs(M1-_MZ);
	    }
	  }
	  else {
	    if(abs(M2-_MZ)<dM){
	      lvZ1 = (lvlep3+lvlep4);
	      lvZ2 = (lvlep1+lvlep2);
	      dM = abs(M2-_MZ);
	    }
	  }
	}//Habe Kombination (12) (34) getestet.
	if(((lep_type()[i1]==lep_type()[i3])&&(lep_charge()[i1] != lep_charge()[i3])) && ((lep_type()[i2]==lep_type()[i4])&&(lep_charge()[i2] != lep_charge()[i4])) ){
	  float M1 = (lvlep1+lvlep3).M()/1000.;
	  float M2 = (lvlep2+lvlep4).M()/1000.;
	  if(abs(M1-_MZ)<abs(M2-_MZ)){
	    //M1 ist die Masse naeher an der Z-Masse
	    if(abs(M1-_MZ)<dM){
	      //M1 is naeher an der Z-Masse als davor getestete Kombinationen
	      lvZ1 = (lvlep1+lvlep3);
	      lvZ2 = (lvlep2+lvlep4);
	      dM = abs(M1-_MZ);
	    }
	  }
	  else {
	    if(abs(M2-_MZ)<dM){
	      lvZ1 = (lvlep2+lvlep4);
	      lvZ2 = (lvlep1+lvlep3);
	      dM = abs(M2-_MZ);
	    }
	  }
	}//Habe Kombination (13) (24) getestet.	
	if(((lep_type()[i1]==lep_type()[i4])&&(lep_charge()[i1] != lep_charge()[i4])) && ((lep_type()[i2]==lep_type()[i3])&&(lep_charge()[i2] != lep_charge()[i3])) ){
	  float M1 = (lvlep1+lvlep4).M()/1000.;
	  float M2 = (lvlep2+lvlep3).M()/1000.;
	  if(abs(M1-_MZ)<abs(M2-_MZ)){
	    //M1 ist die Masse naeher an der Z-Masse
	    if(abs(M1-_MZ)<dM){
	      //M1 is naeher an der Z-Masse als davor getestete Kombinationen
	      lvZ1 = (lvlep1+lvlep4);
	      lvZ2 = (lvlep2+lvlep3);
	      dM = abs(M1-_MZ);
	    }
	  }
	  else {
	    if(abs(M2-_MZ)<dM){
	      lvZ1 = (lvlep2+lvlep3);
	      lvZ2 = (lvlep1+lvlep4);
	      dM = abs(M2-_MZ);
	    }
	  }
	}//Habe Kombination (14) (23) getestet.

	//Jetzt haben wir die zwei Z Bosonen, falls dM geaendert wurde.
	if(dM<99000.){
	  hMll_1->Fill(lvZ1.M()/1000., eventweight);
	  hMll_2->Fill(lvZ2.M()/1000., eventweight);
	  hMllll->Fill((lvZ1+lvZ2).M()/1000., eventweight);
	}

      }//nleps >=4      
    }//event
  
    // Clean Up
    delete tree;
    file.Close();
  }
  if (nEventsChain != nEventsTotal) {
    cout << Form( "ERROR: number of events from files (%d) is not equal to total number of events (%d)", nEventsChain, nEventsTotal ) << endl;
  }
  
  // Hier sind wir fast am Ende - jetzt speichern wir die Histogramme ab.
  std::cout << "Save results in " << outname << std::endl;
  //Nun sind wir aus der Ereignis(Event) Schleife, speichern wir unsere Resultate ab
  //Achtung, "recreate" sagt, dass die alte Datei geloescht und ueberschrieben werden soll.
  TFile *fout = new TFile(outname.c_str(),"recreate");
  hNLeps->Write();
  hNLepsT->Write();
  hLepPt->Write();
  hMll_1->Write();
  hMll_2->Write();
  hMllll->Write();
  fout->Close();
	
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
  return lvtemp;
}
//need factor 2400 or 1/0.0004

