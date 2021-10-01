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

  // Benchmark
  TBenchmark *bmark = new TBenchmark();
  bmark->Start("benchmark");

  // Example Histograms
  TDirectory *rootdir = gDirectory->GetDirectory("Rint:");

  //Am Anfang hier definieren wir unsere Histogramme, die wir fuellen wollen, also worin wir unsere Resultate darstellen
  //Im Beispiel zeige ich drei Histogramme, eines davon werden wir haeufiger betrachten.
  //Das Format ist so, dass wir zuerst den C-Variablen-Name initialisieren mit einem TH1F (1D histogram mit floating-point precision).
  //Dieses TH1F braucht 5 (4) Eingaben, zuerst der ROOT-Variablen-Name (wie ROOT das Histogramm speichert), einen beschreibenen Titel (Histogramm-Titel; x-Achsenbeschreibung; y-Achsenbeschreibung), die Anzahl von Abschnitten (nbins), sowie die Histogramm-Grenzen der x-Achse
  TH1F *hNLeps = new TH1F("hNLeps", "Example plot: Number of leptons; Number of leptons ; Events ",          5,-0.5,4.5);
  TH1F *hLepPt = new TH1F("hLepPt", "Example plot: pT of leptons; p_{T} [GeV] ; Events times N_{leptons} ", 25,   0,250);
  TH1F *hMll   = new TH1F("hMll",   "Example plot: Dilepton invariant mass; m_{ll} [GeV] ; Events ",       100,   0,500);
  hNLeps->SetDirectory(rootdir); hNLeps->Sumw2();
  hLepPt->SetDirectory(rootdir); hLepPt->Sumw2();
  hMll  ->SetDirectory(rootdir); hMll  ->Sumw2();
  
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
      int nleps = 0;
      int index1(-1), index2(-1);
      for(unsigned int ilep = 0; ilep<lep_n(); ++ilep){
	//ilep zeigt den Index innerhalb der lep_n branches da. Man ruft diesen Eintrag mit [index] auf.
	if(lep_pt()[ilep] < 25.*1000.)//minimaler Impuls
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
	if(index1<0) index1 = ilep;//kannst du denken, was wir hier machen?
	else if(index2<0) index2 = ilep;
	hLepPt->Fill(lep_pt()[ilep]/1000.,eventweight);
      }//ilep
      if(!leptontriggereddata)
	continue;
      hNLeps->Fill(nleps, eventweight);
      if(nleps==2) {
	//wir haben die Indizes fuer Mll.
	//Da diese Variable nicht sehr einfach zu berechnen ist, Habe ich hier die Berechnung aufgeschrieben. Was ich hier mache ist ein LorenzVektor aus den zwei Leptonen bauen, und die Masse mit der LorentzVector internen Funktion bestimmen.
	//Die Formel dafuer findest du z.B. hier: https://en.wikipedia.org/wiki/Invariant_mass#Example:_two-particle_collision
	//Ein Lorentzvektor ist z.B. hier beschrieben: https://de.wikipedia.org/wiki/Vierervektor
	if(lep_type()[index1] == lep_type()[index2]){
	  if(lep_charge()[index1] != lep_charge()[index2]){

	    ROOT::Math::PtEtaPhiEVector lvlep1 = GetLorentzVector(lep_pt()[index1],lep_eta()[index1],lep_phi()[index1],lep_E()[index1]);
	    ROOT::Math::PtEtaPhiEVector lvlep2 = GetLorentzVector(lep_pt()[index2],lep_eta()[index2],lep_phi()[index2],lep_E()[index2]);
	    float Mll = (lvlep1+lvlep2).M()/1000.;//go to GeV
	    hMll->Fill(Mll,eventweight);
	  }
	}
      }
      
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
  hLepPt->Write();
  hMll->Write();
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

