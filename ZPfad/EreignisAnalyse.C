
//Hier sind die Grunddefinitionen der Funktionen gespeichert.
#include "EreignisAnalyse.h"

using namespace std;
using namespace tpl;

//Nur die ersten beiden Funktionen (BucheHistogramme, FuelleHistogrammeMitDaten) muessen programmiert werden.

//Die erste Funktion bucht sogenannte Histogramme. Histogramme sind Objekte, die Auflisten, wie viele Ereignisse bestimmte eigenschaften haben - man kann es sich als ein Bild wie y = f(x_ vorstellen ... siehe Beispiele
//Wenn Du Dir eine andere Groesse anschauen willst, so musst Du ein entsprechendes Histogramm definieren.
//Das Format ist so, dass wir zuerst den C-Variablen-Name initialisieren mit einem TH1F (1D histogram mit floating-point precision).
//Dieses TH1F braucht 5 (4) Eingaben, zuerst der ROOT-Variablen-Name (wie ROOT das Histogramm speichert), einen beschreibenen Titel (Histogramm-Titel; x-Achsenbeschreibung; y-Achsenbeschreibung), die Anzahl von Abschnitten (nbins), sowie die Histogramm-Grenzen der x-Achse
map<string, TH1F*> BucheHistogramme(TDirectory *rootdir){

  map<string, TH1F*> histos;
  string mapname;

  //Wir wollen wissen, wie viele sogenannte Leptonen es pro Ereignis gibt. Wir definieren ein Histogramm (TH1F) mit dem Namen hNLeps.
  //Dann schreiben wir auf, was das Histogramm zeigt. Das ist im "Example plot zu sehen, naemlich Number of leptons. Das was hinter den ";" steht ist die Beschriftung der Achsen.
  // Schliesslich geben wir an, wie  das Histogramm unterteilt wird und in welchem Bereich Werte sein duerfen. Hier gibt es 5 Abschnitte im Bereich -0.5 bis 4.5.
  mapname = "hNLeps";
  if(histos.count(mapname) == 0 ) histos[mapname] = new TH1F(mapname.c_str(), "Example plot: Number of leptons; Number of leptons ; Events ",          5,-0.5,4.5);
  //In diesem Histogramm wollen wir den transversalen Impuls der Leptonen darstellen. Unser Histogramm ist in 25 Bereiche unterteilt im Bereich von 0 bis 250 GeV.
  //Beispielsweise alle Leptonen deren transveraler Impuls zwischen 30 und 40 GeV werden im 4. Bereich zusammengezaehlt.
  mapname = "hLepPt";
  if(histos.count(mapname) == 0 ) histos[mapname] = new TH1F(mapname.c_str(), "Example plot: pT of leptons; p_{T} [GeV] ; Events times N_{leptons} ", 25,   0,250);
  //In diesem Histogramm wollen wir den die sogenannte invariante Masse zweier Leptonen darstellen. Diese Groesse entspricht fuer Ereignisse, bei denen ein Z-Teilchen produziert wurdeder Masse des Z-Teilchens.
  //Unser Histogramm ist in 100 Bereiche unterteilt im Bereich von 0 bis 500 GeV. Beispielsweise werden im ersten Bereich alle Ereignisse gezaehlt, bei denen die Masse zwischen 0 und 5 GeV liegt. Der 100. Bereich stellt die Summe aller Ereignisse da, bei denen die Masse zwischen 495 und 500 GeV liegt.
  mapname = "hMll";
  if(histos.count(mapname) == 0 ) histos[mapname] = new TH1F(mapname.c_str(),  "Example plot: Dilepton invariant mass; m_{ll} [GeV] ; Events ",       100,   0,500);

  for(map<string,TH1F*>::iterator h=histos.begin(); h!=histos.end();++h){
    h->second->Sumw2(); h->second->SetDirectory(rootdir);
  }
  return histos;
}


//Die zweite Funktion wird fuer alle Ereignisse mit zwei Leptonen aufgerufen. Hier werden die Daten, die man aus den Ereignissen ablesen kann, in die Histogramme abgelegt.
//Wenn Du dir eine neue Groesse anschauen willst, so musst du natuerlich die entsprechenden Daten ebenfalls in einem Histogramm ablegen.
//Diese Funktion wird nur aufgerufen, wenn man ein entweder ein Elektron-Positron oder ein Muon-Antimuon-Paar gefunden hat. Die kinetischen Eigenschaften der beiden Teilchen in dem Paar sind in lv1 und lv2 abgespeichert.
//In weight ist eine Gewichtung abgespeichert, histos ist die Ansammlung aller Histogramme.
bool FuelleHistogrammeMitDaten(map<string, TH1F*> histos, float weight, ROOT::Math::PtEtaPhiEVector lv1, ROOT::Math::PtEtaPhiEVector lv2){

  //Wie wir in der Masterclass-Aufgabe gelernt hatten und uns mithilfe der Ereignis-Displays angeschaut hatten, kann man die Masse eines Z-Bosons aus den kinetischen Eigenschaften der beiden Leptonen (dem Elektron-Positron- oder dem Muon-Antimuon-Paar) ablesen.
  //Die ROOT-Analysesoftware kann diese Berechnung fuer dich machen.
  //Wir nennen die Variable Mll, die ROOT-Berechnung ist das .M(),
    //Das /1000. ist aufgrund einer Einheitsumberechnung notwendig, z.B. wenn du eine Groesse in Meter gegeben hast, aber eine Antwort in Kilometer haben moechtest, so musst du die Groesse durch 1000. teilen. Das gleiche passiert hier.
  float Mll = (lv1+lv2).M()/1000.;
  //Hier fuellen wir ein Histogramm: Der Name ist "hMll" und die betrachtete Variable ist Mll.
    // Das weight ist noetig, damit das Histogramm weiss, wie stark die Simulation gewichtet ist. Stelle es dir so vor: Von der Theorie erwartest du eine Verteilung von 100 Ereignissen. Um die Verteilung mit einer hoeheren Genauigkeit zu modellieren, simulierst du 1000 Ereignisse. Damit die 1000 Ereignissen den erwarteten 100 Ereignissen entspricht, muss jedes Simulationsereignis mit einem Gewicht von 1/10 = 0.1 gewertet werden.
  histos["hMll"]->Fill(Mll,weight);


  //Wir sagen dem Programm, dass wir erfolgreich die Histogramme gefuellt haben.
  return true;
}



















//Vorselektion: Wir suchen nach Ereignissen, die entweder ein Elektron-Positron oder ein Muon-Antimuon-Paar enthalten.
//Hier musst du eigentlich nichts programmieren.
bool Ereignisvorselektion(map<string, TH1F*> histos, float weight, ROOT::Math::PtEtaPhiEVector &lv1, ROOT::Math::PtEtaPhiEVector &lv2){

  //Theoretisch sollten wir uns Elektronen und Muonen separat anschauen, aber fuer dieses Beispiel schauen wir es uns kombiniert an
  if(!trigE() && !trigM())
    return false;

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
    //Hier fuellen wir ein Beispielhistogramm: Das Histogramm mit dem Namen "hLepPt" wird gefuellt und zwar mit dem lep_pt (leptonen-Impuls_transversal, wobei p fuer Impuls steht)
    //Das /1000. ist aufgrund einer Einheitsumberechnung notwendig, z.B. wenn du eine Groesse in Meter gegeben hast, aber eine Antwort in Kilometer haben moechtest, so musst du die Groesse durch 1000. teilen.
    // Das weight ist noetig, damit das Histogramm weiss, wie stark die Simulation gewichtet ist. Stelle es dir so vor: Von der Theorie erwartest du eine Verteilung von 100 Ereignissen. Um die Verteilung mit einer hoeheren Genauigkeit zu modellieren, simulierst du 1000 Ereignisse. Damit die 1000 Ereignissen den erwarteten 100 Ereignissen entspricht, muss jedes Simulationsereignis mit einem Gewicht von 1/10 = 0.1 gewertet werden.
    histos["hLepPt"]->Fill(lep_pt()[ilep]/1000.,weight);
  }//ilep
  if(!leptontriggereddata)
    return false;
  //Mit dem oberen Beispiel von "hLepPt", kannst du erkennen, was hier gemacht wird?
  histos["hNLeps"]->Fill(nleps, weight);
  if(nleps==2) {
    //wir haben die Indizes fuer Mll.
    //Da diese Variable nicht sehr einfach zu berechnen ist, Habe ich hier die Berechnung aufgeschrieben. Was ich hier mache ist ein LorenzVektor aus den zwei Leptonen bauen, und die Masse mit der LorentzVector internen Funktion bestimmen.
    //Die Formel dafuer findest du z.B. hier: https://en.wikipedia.org/wiki/Invariant_mass#Example:_two-particle_collision
    //Ein Lorentzvektor ist z.B. hier beschrieben: https://de.wikipedia.org/wiki/Vierervektor
    if(lep_type()[index1] == lep_type()[index2]){
      if(lep_charge()[index1] != lep_charge()[index2]){

	//Nur wenn wir diese zwei Variablen berechnen koennen, hat man eine Chance, ein Z-Teilchen zu finden.
	//Also sind nur diese Ereignisse anzuschauen. Daher werden diese Ereignisse mit wahr gekennzeichnet (return true;)
	lv1 = GetLorentzVector(lep_pt()[index1],lep_eta()[index1],lep_phi()[index1],lep_E()[index1]);
	lv2 = GetLorentzVector(lep_pt()[index2],lep_eta()[index2],lep_phi()[index2],lep_E()[index2]);
	return true;
      }
    }
  }
  //Falls das Ereignis nicht als wahr gekennzeichnet wurde, muss es falsch sein, d.h. es kann kein Z-Teilchen enthalten --> return false;
  return false;

}


// Diese Funktion speichert die erstellten Histogramme in Dateien ab, sodass wir sie spaeter uns anschauen koennen. Dies laeuft voellig automatisch.
bool SpeichereHistogramme(string filename, map<string, TH1F*> histos, bool recreate, bool addunderflow, bool addoverflow){
  for(map<string,TH1F*>::iterator h=histos.begin(); h!=histos.end();++h){
    //add overflow
    if(addoverflow){
      h->second->SetBinContent(h->second->GetNbinsX(),          h->second->GetBinContent(h->second->GetNbinsX() )   +    h->second->GetBinContent(h->second->GetNbinsX()+1) );
      h->second->SetBinError(  h->second->GetNbinsX(), sqrt(pow(h->second->GetBinError(  h->second->GetNbinsX() ),2)+pow(h->second->GetBinError(  h->second->GetNbinsX()+1),2) ) );
    }
    //add underflow
    if(addunderflow){
      h->second->SetBinContent(1,          h->second->GetBinContent(1)   +    h->second->GetBinContent(0) );
      h->second->SetBinError(  1, sqrt(pow(h->second->GetBinError(  1),2)+pow(h->second->GetBinError(  0),2) ) );
    }
  }
  
  TFile *f;
  if(recreate) f = new TFile(filename.c_str(),"recreate");
  else f = new TFile(filename.c_str(),"UPDATE");
  f->cd();
  for(map<string,TH1F*>::iterator h=histos.begin(); h!=histos.end();++h){
    h->second->Write(h->first.c_str(),TObject::kOverwrite);
  }
  f->Close();
  cout << "Speichere Histogramme in Datei " << f->GetName() << endl;
  return true;
}

//Einfache Hilfsfunktion
ROOT::Math::PtEtaPhiEVector GetLorentzVector(float pt, float eta, float phi, float E){
  ROOT::Math::PtEtaPhiEVector lvtemp = ROOT::Math::PtEtaPhiEVector(pt,eta,phi,E);
  return lvtemp;
}
