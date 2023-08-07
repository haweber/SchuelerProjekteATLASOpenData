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

#include "EreignisAnalyse.h"

using namespace std;
using namespace tpl;


//Die Hauptfunktion, in der wir die Analyse durchfuehren
int ScanEvents(TChain* chain, string outname, bool isdata = false, bool fast = true, int nEvents = -1, string skimFilePrefix = "test"){
//int ScanEvents(TChain* chain, string outname, bool isdata, bool fast, int nEvents, string skimFilePrefix) {

  // Benchmark
  TBenchmark *bmark = new TBenchmark();
  bmark->Start("benchmark");

  // Example Histograms
  TDirectory *rootdir = gDirectory->GetDirectory("Rint:");

  //Am Anfang hier definieren wir unsere Histogramme, die wir fuellen wollen, also worin wir unsere Resultate darstellen
  //Dies wird in EreignisAnalyse.C durchgefuehrt.
  map<string, TH1F*> histos =  BucheHistogramme(rootdir);
  
  // Schaue alle Dateien an,
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
    //TFile file(currentFile->GetTitle());
    TFile *file = TFile::Open(currentFile->GetTitle());
    //TTree *tree = (TTree*)file.Get("mini");
    TTree *tree = (TTree*)file->Get("mini");
    if (fast) TTreeCache::SetLearnEntries(10);
    if (fast) tree->SetCacheSize(128*1024*1024);
    opentuple.Init(tree);
    std::cout << "Looping over file " << currentFile->GetTitle() << std::endl;

    //Schaue, wie viele Ereignisse pro Datei gespeichert ist
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
      //Diese Selektion/Auswahl findet in EreignisAnalyse.C statt.
      //Theoretisch sollten wir uns Elektronen und Muonen separat anschauen, aber fuer dieses Beispiel schauen wir es uns kombiniert an
      ROOT::Math::PtEtaPhiEVector lvlep1 = GetLorentzVector(0.,0.,0.,0);
      ROOT::Math::PtEtaPhiEVector lvlep2 = GetLorentzVector(0.,0.,0.,0);
      bool passedevent = Ereignisvorselektion(histos, eventweight, lvlep1, lvlep2);

      //Das !-Zeichen, bedeutet, dass passedevent nicht wahr ist, also falsch.
      //Falls das Ereignis als falsch gekennzeichnet wurde, enthaelt es kein Z-Teilchen - daher wollen wir es nicht weiter betrachten --> continue;
      if(!passedevent)
	continue;

      //Wenn wir bis hierhin gekommen sind, haben wir ein Ereignis gefunden, dass moeglicherweise ein Z-Teilchen sein koennte. Jetzt wollen wir diese Ereignisse studieren.
      //Die Programmierung dieser Studie finden wir wiederum in EreignisAnalyse.C
      FuelleHistogrammeMitDaten(histos, eventweight, lvlep1, lvlep2);

      //Das ist alles was wir mit dem Ereignis machen wollten - jetzt schliessen wir die Ereignisschleife, d.h. wir gehen zum naechsten Ereignis, usw. bis wir alle Ereignisse uns angeschaut haben.
    }//event
  
    // Clean Up
    delete tree;
    //file.Close();
    file->Close();
  }
  if (nEventsChain != nEventsTotal) {
    cout << Form( "ERROR: number of events from files (%d) is not equal to total number of events (%d)", nEventsChain, nEventsTotal ) << endl;
  }
  
  // Hier sind wir fast am Ende - jetzt speichern wir die Histogramme ab.
  std::cout << "Save results in " << outname << std::endl;
  //Nun sind wir aus der Ereignis(Event) Schleife, speichern wir unsere Resultate ab
  //Achtung, "recreate" sagt, dass die alte Datei geloescht und eine neue Datei mit dem gleichen Namen abgespeichert werden soll.
  SpeichereHistogramme(outname, histos, true, false, false);

	
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


