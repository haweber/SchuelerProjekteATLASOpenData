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
#include "../OpenTuple.h"

//Hier sind die Grunddefinitionen der Funktionen gespeichert.
map<string, TH1F*> BucheHistogramme(TDirectory *rootdir);
bool SpeichereHistogramme(string filename, map<string, TH1F*> histos, bool recreate, bool addunderflow, bool addoverflow);
ROOT::Math::PtEtaPhiEVector GetLorentzVector(float pt, float eta, float phi, float E);
bool FuelleHistogrammeMitDaten(map<string, TH1F*> histos, float weight, ROOT::Math::PtEtaPhiEVector lv1, ROOT::Math::PtEtaPhiEVector lv2);
bool Ereignisvorselektion(map<string, TH1F*> histos, float weight, ROOT::Math::PtEtaPhiEVector &lv1, ROOT::Math::PtEtaPhiEVector &lv2);
