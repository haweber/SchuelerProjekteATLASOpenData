#include "OpenTuple.h"
OpenTuple opentuple;

void OpenTuple::Init(TTree *tree) {

  tree->SetMakeClass(1);

  runNumber_branch = tree->GetBranch("runNumber");
  if (runNumber_branch) runNumber_branch->SetAddress(&runNumber_);
  eventNumber_branch = tree->GetBranch("eventNumber");
  if (eventNumber_branch) eventNumber_branch->SetAddress(&eventNumber_);
  channelNumber_branch = tree->GetBranch("channelNumber");
  if (channelNumber_branch) channelNumber_branch->SetAddress(&channelNumber_);
  mcWeight_branch = tree->GetBranch("mcWeight");
  if (mcWeight_branch) mcWeight_branch->SetAddress(&mcWeight_);
  scaleFactor_PILEUP_branch = tree->GetBranch("scaleFactor_PILEUP");
  if (scaleFactor_PILEUP_branch) scaleFactor_PILEUP_branch->SetAddress(&scaleFactor_PILEUP_);
  scaleFactor_ELE_branch = tree->GetBranch("scaleFactor_ELE");
  if (scaleFactor_ELE_branch) scaleFactor_ELE_branch->SetAddress(&scaleFactor_ELE_);
  scaleFactor_MUON_branch = tree->GetBranch("scaleFactor_MUON");
  if (scaleFactor_MUON_branch) scaleFactor_MUON_branch->SetAddress(&scaleFactor_MUON_);
  scaleFactor_PHOTON_branch = tree->GetBranch("scaleFactor_PHOTON");
  if (scaleFactor_PHOTON_branch) scaleFactor_PHOTON_branch->SetAddress(&scaleFactor_PHOTON_);
  scaleFactor_TAU_branch = tree->GetBranch("scaleFactor_TAU");
  if (scaleFactor_TAU_branch) scaleFactor_TAU_branch->SetAddress(&scaleFactor_TAU_);
  scaleFactor_BTAG_branch = tree->GetBranch("scaleFactor_BTAG");
  if (scaleFactor_BTAG_branch) scaleFactor_BTAG_branch->SetAddress(&scaleFactor_BTAG_);
  scaleFactor_LepTRIGGER_branch = tree->GetBranch("scaleFactor_LepTRIGGER");
  if (scaleFactor_LepTRIGGER_branch) scaleFactor_LepTRIGGER_branch->SetAddress(&scaleFactor_LepTRIGGER_);
  scaleFactor_PhotonTRIGGER_branch = tree->GetBranch("scaleFactor_PhotonTRIGGER");
  if (scaleFactor_PhotonTRIGGER_branch) scaleFactor_PhotonTRIGGER_branch->SetAddress(&scaleFactor_PhotonTRIGGER_);
  trigE_branch = tree->GetBranch("trigE");
  if (trigE_branch) trigE_branch->SetAddress(&trigE_);
  trigM_branch = tree->GetBranch("trigM");
  if (trigM_branch) trigM_branch->SetAddress(&trigM_);
  trigP_branch = tree->GetBranch("trigP");
  if (trigP_branch) trigP_branch->SetAddress(&trigP_);
  lep_n_branch = tree->GetBranch("lep_n");
  if (lep_n_branch) lep_n_branch->SetAddress(&lep_n_);
  lep_truthMatched_branch = tree->GetBranch("lep_truthMatched");
  if (lep_truthMatched_branch) lep_truthMatched_branch->SetAddress(&lep_truthMatched_);
  lep_trigMatched_branch = tree->GetBranch("lep_trigMatched");
  if (lep_trigMatched_branch) lep_trigMatched_branch->SetAddress(&lep_trigMatched_);
  lep_pt_branch = tree->GetBranch("lep_pt");
  if (lep_pt_branch) lep_pt_branch->SetAddress(&lep_pt_);
  lep_eta_branch = tree->GetBranch("lep_eta");
  if (lep_eta_branch) lep_eta_branch->SetAddress(&lep_eta_);
  lep_phi_branch = tree->GetBranch("lep_phi");
  if (lep_phi_branch) lep_phi_branch->SetAddress(&lep_phi_);
  lep_E_branch = tree->GetBranch("lep_E");
  if (lep_E_branch) lep_E_branch->SetAddress(&lep_E_);
  lep_z0_branch = tree->GetBranch("lep_z0");
  if (lep_z0_branch) lep_z0_branch->SetAddress(&lep_z0_);
  lep_charge_branch = tree->GetBranch("lep_charge");
  if (lep_charge_branch) lep_charge_branch->SetAddress(&lep_charge_);
  lep_type_branch = tree->GetBranch("lep_type");
  if (lep_type_branch) lep_type_branch->SetAddress(&lep_type_);
  lep_isTightID_branch = tree->GetBranch("lep_isTightID");
  if (lep_isTightID_branch) lep_isTightID_branch->SetAddress(&lep_isTightID_);
  lep_ptcone30_branch = tree->GetBranch("lep_ptcone30");
  if (lep_ptcone30_branch) lep_ptcone30_branch->SetAddress(&lep_ptcone30_);
  lep_etcone20_branch = tree->GetBranch("lep_etcone20");
  if (lep_etcone20_branch) lep_etcone20_branch->SetAddress(&lep_etcone20_);
  lep_trackd0pvunbiased_branch = tree->GetBranch("lep_trackd0pvunbiased");
  if (lep_trackd0pvunbiased_branch) lep_trackd0pvunbiased_branch->SetAddress(&lep_trackd0pvunbiased_);
  lep_tracksigd0pvunbiased_branch = tree->GetBranch("lep_tracksigd0pvunbiased");
  if (lep_tracksigd0pvunbiased_branch) lep_tracksigd0pvunbiased_branch->SetAddress(&lep_tracksigd0pvunbiased_);
  met_et_branch = tree->GetBranch("met_et");
  if (met_et_branch) met_et_branch->SetAddress(&met_et_);
  met_phi_branch = tree->GetBranch("met_phi");
  if (met_phi_branch) met_phi_branch->SetAddress(&met_phi_);
  jet_n_branch = tree->GetBranch("jet_n");
  if (jet_n_branch) jet_n_branch->SetAddress(&jet_n_);
  jet_pt_branch = tree->GetBranch("jet_pt");
  if (jet_pt_branch) jet_pt_branch->SetAddress(&jet_pt_);
  jet_eta_branch = tree->GetBranch("jet_eta");
  if (jet_eta_branch) jet_eta_branch->SetAddress(&jet_eta_);
  jet_phi_branch = tree->GetBranch("jet_phi");
  if (jet_phi_branch) jet_phi_branch->SetAddress(&jet_phi_);
  jet_E_branch = tree->GetBranch("jet_E");
  if (jet_E_branch) jet_E_branch->SetAddress(&jet_E_);
  jet_jvt_branch = tree->GetBranch("jet_jvt");
  if (jet_jvt_branch) jet_jvt_branch->SetAddress(&jet_jvt_);
  jet_trueflav_branch = tree->GetBranch("jet_trueflav");
  if (jet_trueflav_branch) jet_trueflav_branch->SetAddress(&jet_trueflav_);
  jet_truthMatched_branch = tree->GetBranch("jet_truthMatched");
  if (jet_truthMatched_branch) jet_truthMatched_branch->SetAddress(&jet_truthMatched_);
  jet_MV2c10_branch = tree->GetBranch("jet_MV2c10");
  if (jet_MV2c10_branch) jet_MV2c10_branch->SetAddress(&jet_MV2c10_);
  photon_n_branch = tree->GetBranch("photon_n");
  if (photon_n_branch) photon_n_branch->SetAddress(&photon_n_);
  photon_truthMatched_branch = tree->GetBranch("photon_truthMatched");
  if (photon_truthMatched_branch) photon_truthMatched_branch->SetAddress(&photon_truthMatched_);
  photon_trigMatched_branch = tree->GetBranch("photon_trigMatched");
  if (photon_trigMatched_branch) photon_trigMatched_branch->SetAddress(&photon_trigMatched_);
  photon_pt_branch = tree->GetBranch("photon_pt");
  if (photon_pt_branch) photon_pt_branch->SetAddress(&photon_pt_);
  photon_eta_branch = tree->GetBranch("photon_eta");
  if (photon_eta_branch) photon_eta_branch->SetAddress(&photon_eta_);
  photon_phi_branch = tree->GetBranch("photon_phi");
  if (photon_phi_branch) photon_phi_branch->SetAddress(&photon_phi_);
  photon_E_branch = tree->GetBranch("photon_E");
  if (photon_E_branch) photon_E_branch->SetAddress(&photon_E_);
  photon_isTightID_branch = tree->GetBranch("photon_isTightID");
  if (photon_isTightID_branch) photon_isTightID_branch->SetAddress(&photon_isTightID_);
  photon_ptcone30_branch = tree->GetBranch("photon_ptcone30");
  if (photon_ptcone30_branch) photon_ptcone30_branch->SetAddress(&photon_ptcone30_);
  photon_etcone20_branch = tree->GetBranch("photon_etcone20");
  if (photon_etcone20_branch) photon_etcone20_branch->SetAddress(&photon_etcone20_);
  photon_convType_branch = tree->GetBranch("photon_convType");
  if (photon_convType_branch) photon_convType_branch->SetAddress(&photon_convType_);
  tau_n_branch = tree->GetBranch("tau_n");
  if (tau_n_branch) tau_n_branch->SetAddress(&tau_n_);
  tau_pt_branch = tree->GetBranch("tau_pt");
  if (tau_pt_branch) tau_pt_branch->SetAddress(&tau_pt_);
  tau_eta_branch = tree->GetBranch("tau_eta");
  if (tau_eta_branch) tau_eta_branch->SetAddress(&tau_eta_);
  tau_phi_branch = tree->GetBranch("tau_phi");
  if (tau_phi_branch) tau_phi_branch->SetAddress(&tau_phi_);
  tau_E_branch = tree->GetBranch("tau_E");
  if (tau_E_branch) tau_E_branch->SetAddress(&tau_E_);
  tau_isTightID_branch = tree->GetBranch("tau_isTightID");
  if (tau_isTightID_branch) tau_isTightID_branch->SetAddress(&tau_isTightID_);
  tau_truthMatched_branch = tree->GetBranch("tau_truthMatched");
  if (tau_truthMatched_branch) tau_truthMatched_branch->SetAddress(&tau_truthMatched_);
  tau_trigMatched_branch = tree->GetBranch("tau_trigMatched");
  if (tau_trigMatched_branch) tau_trigMatched_branch->SetAddress(&tau_trigMatched_);
  tau_nTracks_branch = tree->GetBranch("tau_nTracks");
  if (tau_nTracks_branch) tau_nTracks_branch->SetAddress(&tau_nTracks_);
  tau_BDTid_branch = tree->GetBranch("tau_BDTid");
  if (tau_BDTid_branch) tau_BDTid_branch->SetAddress(&tau_BDTid_);
  ditau_m_branch = tree->GetBranch("ditau_m");
  if (ditau_m_branch) ditau_m_branch->SetAddress(&ditau_m_);
  lep_pt_syst_branch = tree->GetBranch("lep_pt_syst");
  if (lep_pt_syst_branch) lep_pt_syst_branch->SetAddress(&lep_pt_syst_);
  met_et_syst_branch = tree->GetBranch("met_et_syst");
  if (met_et_syst_branch) met_et_syst_branch->SetAddress(&met_et_syst_);
  jet_pt_syst_branch = tree->GetBranch("jet_pt_syst");
  if (jet_pt_syst_branch) jet_pt_syst_branch->SetAddress(&jet_pt_syst_);
  photon_pt_syst_branch = tree->GetBranch("photon_pt_syst");
  if (photon_pt_syst_branch) photon_pt_syst_branch->SetAddress(&photon_pt_syst_);
  tau_pt_syst_branch = tree->GetBranch("tau_pt_syst");
  if (tau_pt_syst_branch) tau_pt_syst_branch->SetAddress(&tau_pt_syst_);
  XSection_branch = tree->GetBranch("XSection");
  if (XSection_branch) XSection_branch->SetAddress(&XSection_);
  SumWeights_branch = tree->GetBranch("SumWeights");
  if (SumWeights_branch) SumWeights_branch->SetAddress(&SumWeights_);
  largeRjet_n_branch = tree->GetBranch("largeRjet_n");
  if (largeRjet_n_branch) largeRjet_n_branch->SetAddress(&largeRjet_n_);
  largeRjet_pt_branch = tree->GetBranch("largeRjet_pt");
  if (largeRjet_pt_branch) largeRjet_pt_branch->SetAddress(&largeRjet_pt_);
  largeRjet_eta_branch = tree->GetBranch("largeRjet_eta");
  if (largeRjet_eta_branch) largeRjet_eta_branch->SetAddress(&largeRjet_eta_);
  largeRjet_phi_branch = tree->GetBranch("largeRjet_phi");
  if (largeRjet_phi_branch) largeRjet_phi_branch->SetAddress(&largeRjet_phi_);
  largeRjet_E_branch = tree->GetBranch("largeRjet_E");
  if (largeRjet_E_branch) largeRjet_E_branch->SetAddress(&largeRjet_E_);
  largeRjet_m_branch = tree->GetBranch("largeRjet_m");
  if (largeRjet_m_branch) largeRjet_m_branch->SetAddress(&largeRjet_m_);
  largeRjet_truthMatched_branch = tree->GetBranch("largeRjet_truthMatched");
  if (largeRjet_truthMatched_branch) largeRjet_truthMatched_branch->SetAddress(&largeRjet_truthMatched_);
  largeRjet_D2_branch = tree->GetBranch("largeRjet_D2");
  if (largeRjet_D2_branch) largeRjet_D2_branch->SetAddress(&largeRjet_D2_);
  largeRjet_tau32_branch = tree->GetBranch("largeRjet_tau32");
  if (largeRjet_tau32_branch) largeRjet_tau32_branch->SetAddress(&largeRjet_tau32_);
  largeRjet_pt_syst_branch = tree->GetBranch("largeRjet_pt_syst");
  if (largeRjet_pt_syst_branch) largeRjet_pt_syst_branch->SetAddress(&largeRjet_pt_syst_);
  tau_charge_branch = tree->GetBranch("tau_charge");
  if (tau_charge_branch) tau_charge_branch->SetAddress(&tau_charge_);

  tree->SetMakeClass(0);
}

void OpenTuple::GetEntry(unsigned int idx) {
  // this only marks branches as not loaded, saving a lot of time
  index = idx;
  runNumber_isLoaded = false;
  eventNumber_isLoaded = false;
  channelNumber_isLoaded = false;
  mcWeight_isLoaded = false;
  scaleFactor_PILEUP_isLoaded = false;
  scaleFactor_ELE_isLoaded = false;
  scaleFactor_MUON_isLoaded = false;
  scaleFactor_PHOTON_isLoaded = false;
  scaleFactor_TAU_isLoaded = false;
  scaleFactor_BTAG_isLoaded = false;
  scaleFactor_LepTRIGGER_isLoaded = false;
  scaleFactor_PhotonTRIGGER_isLoaded = false;
  trigE_isLoaded = false;
  trigM_isLoaded = false;
  trigP_isLoaded = false;
  lep_n_isLoaded = false;
  lep_truthMatched_isLoaded = false;
  lep_trigMatched_isLoaded = false;
  lep_pt_isLoaded = false;
  lep_eta_isLoaded = false;
  lep_phi_isLoaded = false;
  lep_E_isLoaded = false;
  lep_z0_isLoaded = false;
  lep_charge_isLoaded = false;
  lep_type_isLoaded = false;
  lep_isTightID_isLoaded = false;
  lep_ptcone30_isLoaded = false;
  lep_etcone20_isLoaded = false;
  lep_trackd0pvunbiased_isLoaded = false;
  lep_tracksigd0pvunbiased_isLoaded = false;
  met_et_isLoaded = false;
  met_phi_isLoaded = false;
  jet_n_isLoaded = false;
  jet_pt_isLoaded = false;
  jet_eta_isLoaded = false;
  jet_phi_isLoaded = false;
  jet_E_isLoaded = false;
  jet_jvt_isLoaded = false;
  jet_trueflav_isLoaded = false;
  jet_truthMatched_isLoaded = false;
  jet_MV2c10_isLoaded = false;
  photon_n_isLoaded = false;
  photon_truthMatched_isLoaded = false;
  photon_trigMatched_isLoaded = false;
  photon_pt_isLoaded = false;
  photon_eta_isLoaded = false;
  photon_phi_isLoaded = false;
  photon_E_isLoaded = false;
  photon_isTightID_isLoaded = false;
  photon_ptcone30_isLoaded = false;
  photon_etcone20_isLoaded = false;
  photon_convType_isLoaded = false;
  tau_n_isLoaded = false;
  tau_pt_isLoaded = false;
  tau_eta_isLoaded = false;
  tau_phi_isLoaded = false;
  tau_E_isLoaded = false;
  tau_isTightID_isLoaded = false;
  tau_truthMatched_isLoaded = false;
  tau_trigMatched_isLoaded = false;
  tau_nTracks_isLoaded = false;
  tau_BDTid_isLoaded = false;
  ditau_m_isLoaded = false;
  lep_pt_syst_isLoaded = false;
  met_et_syst_isLoaded = false;
  jet_pt_syst_isLoaded = false;
  photon_pt_syst_isLoaded = false;
  tau_pt_syst_isLoaded = false;
  XSection_isLoaded = false;
  SumWeights_isLoaded = false;
  largeRjet_n_isLoaded = false;
  largeRjet_pt_isLoaded = false;
  largeRjet_eta_isLoaded = false;
  largeRjet_phi_isLoaded = false;
  largeRjet_E_isLoaded = false;
  largeRjet_m_isLoaded = false;
  largeRjet_truthMatched_isLoaded = false;
  largeRjet_D2_isLoaded = false;
  largeRjet_tau32_isLoaded = false;
  largeRjet_pt_syst_isLoaded = false;
  tau_charge_isLoaded = false;
}

void OpenTuple::LoadAllBranches() {
  // load all branches
  if (runNumber_branch != 0) runNumber();
  if (eventNumber_branch != 0) eventNumber();
  if (channelNumber_branch != 0) channelNumber();
  if (mcWeight_branch != 0) mcWeight();
  if (scaleFactor_PILEUP_branch != 0) scaleFactor_PILEUP();
  if (scaleFactor_ELE_branch != 0) scaleFactor_ELE();
  if (scaleFactor_MUON_branch != 0) scaleFactor_MUON();
  if (scaleFactor_PHOTON_branch != 0) scaleFactor_PHOTON();
  if (scaleFactor_TAU_branch != 0) scaleFactor_TAU();
  if (scaleFactor_BTAG_branch != 0) scaleFactor_BTAG();
  if (scaleFactor_LepTRIGGER_branch != 0) scaleFactor_LepTRIGGER();
  if (scaleFactor_PhotonTRIGGER_branch != 0) scaleFactor_PhotonTRIGGER();
  if (trigE_branch != 0) trigE();
  if (trigM_branch != 0) trigM();
  if (trigP_branch != 0) trigP();
  if (lep_n_branch != 0) lep_n();
  if (lep_truthMatched_branch != 0) lep_truthMatched();
  if (lep_trigMatched_branch != 0) lep_trigMatched();
  if (lep_pt_branch != 0) lep_pt();
  if (lep_eta_branch != 0) lep_eta();
  if (lep_phi_branch != 0) lep_phi();
  if (lep_E_branch != 0) lep_E();
  if (lep_z0_branch != 0) lep_z0();
  if (lep_charge_branch != 0) lep_charge();
  if (lep_type_branch != 0) lep_type();
  if (lep_isTightID_branch != 0) lep_isTightID();
  if (lep_ptcone30_branch != 0) lep_ptcone30();
  if (lep_etcone20_branch != 0) lep_etcone20();
  if (lep_trackd0pvunbiased_branch != 0) lep_trackd0pvunbiased();
  if (lep_tracksigd0pvunbiased_branch != 0) lep_tracksigd0pvunbiased();
  if (met_et_branch != 0) met_et();
  if (met_phi_branch != 0) met_phi();
  if (jet_n_branch != 0) jet_n();
  if (jet_pt_branch != 0) jet_pt();
  if (jet_eta_branch != 0) jet_eta();
  if (jet_phi_branch != 0) jet_phi();
  if (jet_E_branch != 0) jet_E();
  if (jet_jvt_branch != 0) jet_jvt();
  if (jet_trueflav_branch != 0) jet_trueflav();
  if (jet_truthMatched_branch != 0) jet_truthMatched();
  if (jet_MV2c10_branch != 0) jet_MV2c10();
  if (photon_n_branch != 0) photon_n();
  if (photon_truthMatched_branch != 0) photon_truthMatched();
  if (photon_trigMatched_branch != 0) photon_trigMatched();
  if (photon_pt_branch != 0) photon_pt();
  if (photon_eta_branch != 0) photon_eta();
  if (photon_phi_branch != 0) photon_phi();
  if (photon_E_branch != 0) photon_E();
  if (photon_isTightID_branch != 0) photon_isTightID();
  if (photon_ptcone30_branch != 0) photon_ptcone30();
  if (photon_etcone20_branch != 0) photon_etcone20();
  if (photon_convType_branch != 0) photon_convType();
  if (tau_n_branch != 0) tau_n();
  if (tau_pt_branch != 0) tau_pt();
  if (tau_eta_branch != 0) tau_eta();
  if (tau_phi_branch != 0) tau_phi();
  if (tau_E_branch != 0) tau_E();
  if (tau_isTightID_branch != 0) tau_isTightID();
  if (tau_truthMatched_branch != 0) tau_truthMatched();
  if (tau_trigMatched_branch != 0) tau_trigMatched();
  if (tau_nTracks_branch != 0) tau_nTracks();
  if (tau_BDTid_branch != 0) tau_BDTid();
  if (ditau_m_branch != 0) ditau_m();
  if (lep_pt_syst_branch != 0) lep_pt_syst();
  if (met_et_syst_branch != 0) met_et_syst();
  if (jet_pt_syst_branch != 0) jet_pt_syst();
  if (photon_pt_syst_branch != 0) photon_pt_syst();
  if (tau_pt_syst_branch != 0) tau_pt_syst();
  if (XSection_branch != 0) XSection();
  if (SumWeights_branch != 0) SumWeights();
  if (largeRjet_n_branch != 0) largeRjet_n();
  if (largeRjet_pt_branch != 0) largeRjet_pt();
  if (largeRjet_eta_branch != 0) largeRjet_eta();
  if (largeRjet_phi_branch != 0) largeRjet_phi();
  if (largeRjet_E_branch != 0) largeRjet_E();
  if (largeRjet_m_branch != 0) largeRjet_m();
  if (largeRjet_truthMatched_branch != 0) largeRjet_truthMatched();
  if (largeRjet_D2_branch != 0) largeRjet_D2();
  if (largeRjet_tau32_branch != 0) largeRjet_tau32();
  if (largeRjet_pt_syst_branch != 0) largeRjet_pt_syst();
  if (tau_charge_branch != 0) tau_charge();
}

const int &OpenTuple::runNumber() {
  if (not runNumber_isLoaded) {
    if (runNumber_branch != 0) {
      runNumber_branch->GetEntry(index);
    } else {
      printf("branch runNumber_branch does not exist!\n");
      exit(1);
    }
    runNumber_isLoaded = true;
  }
  return runNumber_;
}

const int &OpenTuple::eventNumber() {
  if (not eventNumber_isLoaded) {
    if (eventNumber_branch != 0) {
      eventNumber_branch->GetEntry(index);
    } else {
      printf("branch eventNumber_branch does not exist!\n");
      exit(1);
    }
    eventNumber_isLoaded = true;
  }
  return eventNumber_;
}

const int &OpenTuple::channelNumber() {
  if (not channelNumber_isLoaded) {
    if (channelNumber_branch != 0) {
      channelNumber_branch->GetEntry(index);
    } else {
      printf("branch channelNumber_branch does not exist!\n");
      exit(1);
    }
    channelNumber_isLoaded = true;
  }
  return channelNumber_;
}

const float &OpenTuple::mcWeight() {
  if (not mcWeight_isLoaded) {
    if (mcWeight_branch != 0) {
      mcWeight_branch->GetEntry(index);
    } else {
      printf("branch mcWeight_branch does not exist!\n");
      exit(1);
    }
    mcWeight_isLoaded = true;
  }
  return mcWeight_;
}

const float &OpenTuple::scaleFactor_PILEUP() {
  if (not scaleFactor_PILEUP_isLoaded) {
    if (scaleFactor_PILEUP_branch != 0) {
      scaleFactor_PILEUP_branch->GetEntry(index);
    } else {
      printf("branch scaleFactor_PILEUP_branch does not exist!\n");
      exit(1);
    }
    scaleFactor_PILEUP_isLoaded = true;
  }
  return scaleFactor_PILEUP_;
}

const float &OpenTuple::scaleFactor_ELE() {
  if (not scaleFactor_ELE_isLoaded) {
    if (scaleFactor_ELE_branch != 0) {
      scaleFactor_ELE_branch->GetEntry(index);
    } else {
      printf("branch scaleFactor_ELE_branch does not exist!\n");
      exit(1);
    }
    scaleFactor_ELE_isLoaded = true;
  }
  return scaleFactor_ELE_;
}

const float &OpenTuple::scaleFactor_MUON() {
  if (not scaleFactor_MUON_isLoaded) {
    if (scaleFactor_MUON_branch != 0) {
      scaleFactor_MUON_branch->GetEntry(index);
    } else {
      printf("branch scaleFactor_MUON_branch does not exist!\n");
      exit(1);
    }
    scaleFactor_MUON_isLoaded = true;
  }
  return scaleFactor_MUON_;
}

const float &OpenTuple::scaleFactor_PHOTON() {
  if (not scaleFactor_PHOTON_isLoaded) {
    if (scaleFactor_PHOTON_branch != 0) {
      scaleFactor_PHOTON_branch->GetEntry(index);
    } else {
      printf("branch scaleFactor_PHOTON_branch does not exist!\n");
      exit(1);
    }
    scaleFactor_PHOTON_isLoaded = true;
  }
  return scaleFactor_PHOTON_;
}

const float &OpenTuple::scaleFactor_TAU() {
  if (not scaleFactor_TAU_isLoaded) {
    if (scaleFactor_TAU_branch != 0) {
      scaleFactor_TAU_branch->GetEntry(index);
    } else {
      printf("branch scaleFactor_TAU_branch does not exist!\n");
      exit(1);
    }
    scaleFactor_TAU_isLoaded = true;
  }
  return scaleFactor_TAU_;
}

const float &OpenTuple::scaleFactor_BTAG() {
  if (not scaleFactor_BTAG_isLoaded) {
    if (scaleFactor_BTAG_branch != 0) {
      scaleFactor_BTAG_branch->GetEntry(index);
    } else {
      printf("branch scaleFactor_BTAG_branch does not exist!\n");
      exit(1);
    }
    scaleFactor_BTAG_isLoaded = true;
  }
  return scaleFactor_BTAG_;
}

const float &OpenTuple::scaleFactor_LepTRIGGER() {
  if (not scaleFactor_LepTRIGGER_isLoaded) {
    if (scaleFactor_LepTRIGGER_branch != 0) {
      scaleFactor_LepTRIGGER_branch->GetEntry(index);
    } else {
      printf("branch scaleFactor_LepTRIGGER_branch does not exist!\n");
      exit(1);
    }
    scaleFactor_LepTRIGGER_isLoaded = true;
  }
  return scaleFactor_LepTRIGGER_;
}

const float &OpenTuple::scaleFactor_PhotonTRIGGER() {
  if (not scaleFactor_PhotonTRIGGER_isLoaded) {
    if (scaleFactor_PhotonTRIGGER_branch != 0) {
      scaleFactor_PhotonTRIGGER_branch->GetEntry(index);
    } else {
      printf("branch scaleFactor_PhotonTRIGGER_branch does not exist!\n");
      exit(1);
    }
    scaleFactor_PhotonTRIGGER_isLoaded = true;
  }
  return scaleFactor_PhotonTRIGGER_;
}

const bool &OpenTuple::trigE() {
  if (not trigE_isLoaded) {
    if (trigE_branch != 0) {
      trigE_branch->GetEntry(index);
    } else {
      printf("branch trigE_branch does not exist!\n");
      exit(1);
    }
    trigE_isLoaded = true;
  }
  return trigE_;
}

const bool &OpenTuple::trigM() {
  if (not trigM_isLoaded) {
    if (trigM_branch != 0) {
      trigM_branch->GetEntry(index);
    } else {
      printf("branch trigM_branch does not exist!\n");
      exit(1);
    }
    trigM_isLoaded = true;
  }
  return trigM_;
}

const bool &OpenTuple::trigP() {
  if (not trigP_isLoaded) {
    if (trigP_branch != 0) {
      trigP_branch->GetEntry(index);
    } else {
      printf("branch trigP_branch does not exist!\n");
      exit(1);
    }
    trigP_isLoaded = true;
  }
  return trigP_;
}

const unsigned int &OpenTuple::lep_n() {
  if (not lep_n_isLoaded) {
    if (lep_n_branch != 0) {
      lep_n_branch->GetEntry(index);
    } else {
      printf("branch lep_n_branch does not exist!\n");
      exit(1);
    }
    lep_n_isLoaded = true;
  }
  return lep_n_;
}

const vector<bool> &OpenTuple::lep_truthMatched() {
  if (not lep_truthMatched_isLoaded) {
    if (lep_truthMatched_branch != 0) {
      lep_truthMatched_branch->GetEntry(index);
    } else {
      printf("branch lep_truthMatched_branch does not exist!\n");
      exit(1);
    }
    lep_truthMatched_isLoaded = true;
  }
  return *lep_truthMatched_;
}

const vector<bool> &OpenTuple::lep_trigMatched() {
  if (not lep_trigMatched_isLoaded) {
    if (lep_trigMatched_branch != 0) {
      lep_trigMatched_branch->GetEntry(index);
    } else {
      printf("branch lep_trigMatched_branch does not exist!\n");
      exit(1);
    }
    lep_trigMatched_isLoaded = true;
  }
  return *lep_trigMatched_;
}

const vector<float> &OpenTuple::lep_pt() {
  if (not lep_pt_isLoaded) {
    if (lep_pt_branch != 0) {
      lep_pt_branch->GetEntry(index);
    } else {
      printf("branch lep_pt_branch does not exist!\n");
      exit(1);
    }
    lep_pt_isLoaded = true;
  }
  return *lep_pt_;
}

const vector<float> &OpenTuple::lep_eta() {
  if (not lep_eta_isLoaded) {
    if (lep_eta_branch != 0) {
      lep_eta_branch->GetEntry(index);
    } else {
      printf("branch lep_eta_branch does not exist!\n");
      exit(1);
    }
    lep_eta_isLoaded = true;
  }
  return *lep_eta_;
}

const vector<float> &OpenTuple::lep_phi() {
  if (not lep_phi_isLoaded) {
    if (lep_phi_branch != 0) {
      lep_phi_branch->GetEntry(index);
    } else {
      printf("branch lep_phi_branch does not exist!\n");
      exit(1);
    }
    lep_phi_isLoaded = true;
  }
  return *lep_phi_;
}

const vector<float> &OpenTuple::lep_E() {
  if (not lep_E_isLoaded) {
    if (lep_E_branch != 0) {
      lep_E_branch->GetEntry(index);
    } else {
      printf("branch lep_E_branch does not exist!\n");
      exit(1);
    }
    lep_E_isLoaded = true;
  }
  return *lep_E_;
}

const vector<float> &OpenTuple::lep_z0() {
  if (not lep_z0_isLoaded) {
    if (lep_z0_branch != 0) {
      lep_z0_branch->GetEntry(index);
    } else {
      printf("branch lep_z0_branch does not exist!\n");
      exit(1);
    }
    lep_z0_isLoaded = true;
  }
  return *lep_z0_;
}

const vector<int> &OpenTuple::lep_charge() {
  if (not lep_charge_isLoaded) {
    if (lep_charge_branch != 0) {
      lep_charge_branch->GetEntry(index);
    } else {
      printf("branch lep_charge_branch does not exist!\n");
      exit(1);
    }
    lep_charge_isLoaded = true;
  }
  return *lep_charge_;
}

const vector<unsigned int> &OpenTuple::lep_type() {
  if (not lep_type_isLoaded) {
    if (lep_type_branch != 0) {
      lep_type_branch->GetEntry(index);
    } else {
      printf("branch lep_type_branch does not exist!\n");
      exit(1);
    }
    lep_type_isLoaded = true;
  }
  return *lep_type_;
}

const vector<bool> &OpenTuple::lep_isTightID() {
  if (not lep_isTightID_isLoaded) {
    if (lep_isTightID_branch != 0) {
      lep_isTightID_branch->GetEntry(index);
    } else {
      printf("branch lep_isTightID_branch does not exist!\n");
      exit(1);
    }
    lep_isTightID_isLoaded = true;
  }
  return *lep_isTightID_;
}

const vector<float> &OpenTuple::lep_ptcone30() {
  if (not lep_ptcone30_isLoaded) {
    if (lep_ptcone30_branch != 0) {
      lep_ptcone30_branch->GetEntry(index);
    } else {
      printf("branch lep_ptcone30_branch does not exist!\n");
      exit(1);
    }
    lep_ptcone30_isLoaded = true;
  }
  return *lep_ptcone30_;
}

const vector<float> &OpenTuple::lep_etcone20() {
  if (not lep_etcone20_isLoaded) {
    if (lep_etcone20_branch != 0) {
      lep_etcone20_branch->GetEntry(index);
    } else {
      printf("branch lep_etcone20_branch does not exist!\n");
      exit(1);
    }
    lep_etcone20_isLoaded = true;
  }
  return *lep_etcone20_;
}

const vector<float> &OpenTuple::lep_trackd0pvunbiased() {
  if (not lep_trackd0pvunbiased_isLoaded) {
    if (lep_trackd0pvunbiased_branch != 0) {
      lep_trackd0pvunbiased_branch->GetEntry(index);
    } else {
      printf("branch lep_trackd0pvunbiased_branch does not exist!\n");
      exit(1);
    }
    lep_trackd0pvunbiased_isLoaded = true;
  }
  return *lep_trackd0pvunbiased_;
}

const vector<float> &OpenTuple::lep_tracksigd0pvunbiased() {
  if (not lep_tracksigd0pvunbiased_isLoaded) {
    if (lep_tracksigd0pvunbiased_branch != 0) {
      lep_tracksigd0pvunbiased_branch->GetEntry(index);
    } else {
      printf("branch lep_tracksigd0pvunbiased_branch does not exist!\n");
      exit(1);
    }
    lep_tracksigd0pvunbiased_isLoaded = true;
  }
  return *lep_tracksigd0pvunbiased_;
}

const float &OpenTuple::met_et() {
  if (not met_et_isLoaded) {
    if (met_et_branch != 0) {
      met_et_branch->GetEntry(index);
    } else {
      printf("branch met_et_branch does not exist!\n");
      exit(1);
    }
    met_et_isLoaded = true;
  }
  return met_et_;
}

const float &OpenTuple::met_phi() {
  if (not met_phi_isLoaded) {
    if (met_phi_branch != 0) {
      met_phi_branch->GetEntry(index);
    } else {
      printf("branch met_phi_branch does not exist!\n");
      exit(1);
    }
    met_phi_isLoaded = true;
  }
  return met_phi_;
}

const unsigned int &OpenTuple::jet_n() {
  if (not jet_n_isLoaded) {
    if (jet_n_branch != 0) {
      jet_n_branch->GetEntry(index);
    } else {
      printf("branch jet_n_branch does not exist!\n");
      exit(1);
    }
    jet_n_isLoaded = true;
  }
  return jet_n_;
}

const vector<float> &OpenTuple::jet_pt() {
  if (not jet_pt_isLoaded) {
    if (jet_pt_branch != 0) {
      jet_pt_branch->GetEntry(index);
    } else {
      printf("branch jet_pt_branch does not exist!\n");
      exit(1);
    }
    jet_pt_isLoaded = true;
  }
  return *jet_pt_;
}

const vector<float> &OpenTuple::jet_eta() {
  if (not jet_eta_isLoaded) {
    if (jet_eta_branch != 0) {
      jet_eta_branch->GetEntry(index);
    } else {
      printf("branch jet_eta_branch does not exist!\n");
      exit(1);
    }
    jet_eta_isLoaded = true;
  }
  return *jet_eta_;
}

const vector<float> &OpenTuple::jet_phi() {
  if (not jet_phi_isLoaded) {
    if (jet_phi_branch != 0) {
      jet_phi_branch->GetEntry(index);
    } else {
      printf("branch jet_phi_branch does not exist!\n");
      exit(1);
    }
    jet_phi_isLoaded = true;
  }
  return *jet_phi_;
}

const vector<float> &OpenTuple::jet_E() {
  if (not jet_E_isLoaded) {
    if (jet_E_branch != 0) {
      jet_E_branch->GetEntry(index);
    } else {
      printf("branch jet_E_branch does not exist!\n");
      exit(1);
    }
    jet_E_isLoaded = true;
  }
  return *jet_E_;
}

const vector<float> &OpenTuple::jet_jvt() {
  if (not jet_jvt_isLoaded) {
    if (jet_jvt_branch != 0) {
      jet_jvt_branch->GetEntry(index);
    } else {
      printf("branch jet_jvt_branch does not exist!\n");
      exit(1);
    }
    jet_jvt_isLoaded = true;
  }
  return *jet_jvt_;
}

const vector<int> &OpenTuple::jet_trueflav() {
  if (not jet_trueflav_isLoaded) {
    if (jet_trueflav_branch != 0) {
      jet_trueflav_branch->GetEntry(index);
    } else {
      printf("branch jet_trueflav_branch does not exist!\n");
      exit(1);
    }
    jet_trueflav_isLoaded = true;
  }
  return *jet_trueflav_;
}

const vector<bool> &OpenTuple::jet_truthMatched() {
  if (not jet_truthMatched_isLoaded) {
    if (jet_truthMatched_branch != 0) {
      jet_truthMatched_branch->GetEntry(index);
    } else {
      printf("branch jet_truthMatched_branch does not exist!\n");
      exit(1);
    }
    jet_truthMatched_isLoaded = true;
  }
  return *jet_truthMatched_;
}

const vector<float> &OpenTuple::jet_MV2c10() {
  if (not jet_MV2c10_isLoaded) {
    if (jet_MV2c10_branch != 0) {
      jet_MV2c10_branch->GetEntry(index);
    } else {
      printf("branch jet_MV2c10_branch does not exist!\n");
      exit(1);
    }
    jet_MV2c10_isLoaded = true;
  }
  return *jet_MV2c10_;
}

const unsigned int &OpenTuple::photon_n() {
  if (not photon_n_isLoaded) {
    if (photon_n_branch != 0) {
      photon_n_branch->GetEntry(index);
    } else {
      printf("branch photon_n_branch does not exist!\n");
      exit(1);
    }
    photon_n_isLoaded = true;
  }
  return photon_n_;
}

const vector<bool> &OpenTuple::photon_truthMatched() {
  if (not photon_truthMatched_isLoaded) {
    if (photon_truthMatched_branch != 0) {
      photon_truthMatched_branch->GetEntry(index);
    } else {
      printf("branch photon_truthMatched_branch does not exist!\n");
      exit(1);
    }
    photon_truthMatched_isLoaded = true;
  }
  return *photon_truthMatched_;
}

const vector<bool> &OpenTuple::photon_trigMatched() {
  if (not photon_trigMatched_isLoaded) {
    if (photon_trigMatched_branch != 0) {
      photon_trigMatched_branch->GetEntry(index);
    } else {
      printf("branch photon_trigMatched_branch does not exist!\n");
      exit(1);
    }
    photon_trigMatched_isLoaded = true;
  }
  return *photon_trigMatched_;
}

const vector<float> &OpenTuple::photon_pt() {
  if (not photon_pt_isLoaded) {
    if (photon_pt_branch != 0) {
      photon_pt_branch->GetEntry(index);
    } else {
      printf("branch photon_pt_branch does not exist!\n");
      exit(1);
    }
    photon_pt_isLoaded = true;
  }
  return *photon_pt_;
}

const vector<float> &OpenTuple::photon_eta() {
  if (not photon_eta_isLoaded) {
    if (photon_eta_branch != 0) {
      photon_eta_branch->GetEntry(index);
    } else {
      printf("branch photon_eta_branch does not exist!\n");
      exit(1);
    }
    photon_eta_isLoaded = true;
  }
  return *photon_eta_;
}

const vector<float> &OpenTuple::photon_phi() {
  if (not photon_phi_isLoaded) {
    if (photon_phi_branch != 0) {
      photon_phi_branch->GetEntry(index);
    } else {
      printf("branch photon_phi_branch does not exist!\n");
      exit(1);
    }
    photon_phi_isLoaded = true;
  }
  return *photon_phi_;
}

const vector<float> &OpenTuple::photon_E() {
  if (not photon_E_isLoaded) {
    if (photon_E_branch != 0) {
      photon_E_branch->GetEntry(index);
    } else {
      printf("branch photon_E_branch does not exist!\n");
      exit(1);
    }
    photon_E_isLoaded = true;
  }
  return *photon_E_;
}

const vector<bool> &OpenTuple::photon_isTightID() {
  if (not photon_isTightID_isLoaded) {
    if (photon_isTightID_branch != 0) {
      photon_isTightID_branch->GetEntry(index);
    } else {
      printf("branch photon_isTightID_branch does not exist!\n");
      exit(1);
    }
    photon_isTightID_isLoaded = true;
  }
  return *photon_isTightID_;
}

const vector<float> &OpenTuple::photon_ptcone30() {
  if (not photon_ptcone30_isLoaded) {
    if (photon_ptcone30_branch != 0) {
      photon_ptcone30_branch->GetEntry(index);
    } else {
      printf("branch photon_ptcone30_branch does not exist!\n");
      exit(1);
    }
    photon_ptcone30_isLoaded = true;
  }
  return *photon_ptcone30_;
}

const vector<float> &OpenTuple::photon_etcone20() {
  if (not photon_etcone20_isLoaded) {
    if (photon_etcone20_branch != 0) {
      photon_etcone20_branch->GetEntry(index);
    } else {
      printf("branch photon_etcone20_branch does not exist!\n");
      exit(1);
    }
    photon_etcone20_isLoaded = true;
  }
  return *photon_etcone20_;
}

const vector<int> &OpenTuple::photon_convType() {
  if (not photon_convType_isLoaded) {
    if (photon_convType_branch != 0) {
      photon_convType_branch->GetEntry(index);
    } else {
      printf("branch photon_convType_branch does not exist!\n");
      exit(1);
    }
    photon_convType_isLoaded = true;
  }
  return *photon_convType_;
}

const unsigned int &OpenTuple::tau_n() {
  if (not tau_n_isLoaded) {
    if (tau_n_branch != 0) {
      tau_n_branch->GetEntry(index);
    } else {
      printf("branch tau_n_branch does not exist!\n");
      exit(1);
    }
    tau_n_isLoaded = true;
  }
  return tau_n_;
}

const vector<float> &OpenTuple::tau_pt() {
  if (not tau_pt_isLoaded) {
    if (tau_pt_branch != 0) {
      tau_pt_branch->GetEntry(index);
    } else {
      printf("branch tau_pt_branch does not exist!\n");
      exit(1);
    }
    tau_pt_isLoaded = true;
  }
  return *tau_pt_;
}

const vector<float> &OpenTuple::tau_eta() {
  if (not tau_eta_isLoaded) {
    if (tau_eta_branch != 0) {
      tau_eta_branch->GetEntry(index);
    } else {
      printf("branch tau_eta_branch does not exist!\n");
      exit(1);
    }
    tau_eta_isLoaded = true;
  }
  return *tau_eta_;
}

const vector<float> &OpenTuple::tau_phi() {
  if (not tau_phi_isLoaded) {
    if (tau_phi_branch != 0) {
      tau_phi_branch->GetEntry(index);
    } else {
      printf("branch tau_phi_branch does not exist!\n");
      exit(1);
    }
    tau_phi_isLoaded = true;
  }
  return *tau_phi_;
}

const vector<float> &OpenTuple::tau_E() {
  if (not tau_E_isLoaded) {
    if (tau_E_branch != 0) {
      tau_E_branch->GetEntry(index);
    } else {
      printf("branch tau_E_branch does not exist!\n");
      exit(1);
    }
    tau_E_isLoaded = true;
  }
  return *tau_E_;
}

const vector<bool> &OpenTuple::tau_isTightID() {
  if (not tau_isTightID_isLoaded) {
    if (tau_isTightID_branch != 0) {
      tau_isTightID_branch->GetEntry(index);
    } else {
      printf("branch tau_isTightID_branch does not exist!\n");
      exit(1);
    }
    tau_isTightID_isLoaded = true;
  }
  return *tau_isTightID_;
}

const vector<bool> &OpenTuple::tau_truthMatched() {
  if (not tau_truthMatched_isLoaded) {
    if (tau_truthMatched_branch != 0) {
      tau_truthMatched_branch->GetEntry(index);
    } else {
      printf("branch tau_truthMatched_branch does not exist!\n");
      exit(1);
    }
    tau_truthMatched_isLoaded = true;
  }
  return *tau_truthMatched_;
}

const vector<bool> &OpenTuple::tau_trigMatched() {
  if (not tau_trigMatched_isLoaded) {
    if (tau_trigMatched_branch != 0) {
      tau_trigMatched_branch->GetEntry(index);
    } else {
      printf("branch tau_trigMatched_branch does not exist!\n");
      exit(1);
    }
    tau_trigMatched_isLoaded = true;
  }
  return *tau_trigMatched_;
}

const vector<int> &OpenTuple::tau_nTracks() {
  if (not tau_nTracks_isLoaded) {
    if (tau_nTracks_branch != 0) {
      tau_nTracks_branch->GetEntry(index);
    } else {
      printf("branch tau_nTracks_branch does not exist!\n");
      exit(1);
    }
    tau_nTracks_isLoaded = true;
  }
  return *tau_nTracks_;
}

const vector<float> &OpenTuple::tau_BDTid() {
  if (not tau_BDTid_isLoaded) {
    if (tau_BDTid_branch != 0) {
      tau_BDTid_branch->GetEntry(index);
    } else {
      printf("branch tau_BDTid_branch does not exist!\n");
      exit(1);
    }
    tau_BDTid_isLoaded = true;
  }
  return *tau_BDTid_;
}

const float &OpenTuple::ditau_m() {
  if (not ditau_m_isLoaded) {
    if (ditau_m_branch != 0) {
      ditau_m_branch->GetEntry(index);
    } else {
      printf("branch ditau_m_branch does not exist!\n");
      exit(1);
    }
    ditau_m_isLoaded = true;
  }
  return ditau_m_;
}

const vector<float> &OpenTuple::lep_pt_syst() {
  if (not lep_pt_syst_isLoaded) {
    if (lep_pt_syst_branch != 0) {
      lep_pt_syst_branch->GetEntry(index);
    } else {
      printf("branch lep_pt_syst_branch does not exist!\n");
      exit(1);
    }
    lep_pt_syst_isLoaded = true;
  }
  return *lep_pt_syst_;
}

const float &OpenTuple::met_et_syst() {
  if (not met_et_syst_isLoaded) {
    if (met_et_syst_branch != 0) {
      met_et_syst_branch->GetEntry(index);
    } else {
      printf("branch met_et_syst_branch does not exist!\n");
      exit(1);
    }
    met_et_syst_isLoaded = true;
  }
  return met_et_syst_;
}

const vector<float> &OpenTuple::jet_pt_syst() {
  if (not jet_pt_syst_isLoaded) {
    if (jet_pt_syst_branch != 0) {
      jet_pt_syst_branch->GetEntry(index);
    } else {
      printf("branch jet_pt_syst_branch does not exist!\n");
      exit(1);
    }
    jet_pt_syst_isLoaded = true;
  }
  return *jet_pt_syst_;
}

const vector<float> &OpenTuple::photon_pt_syst() {
  if (not photon_pt_syst_isLoaded) {
    if (photon_pt_syst_branch != 0) {
      photon_pt_syst_branch->GetEntry(index);
    } else {
      printf("branch photon_pt_syst_branch does not exist!\n");
      exit(1);
    }
    photon_pt_syst_isLoaded = true;
  }
  return *photon_pt_syst_;
}

const vector<float> &OpenTuple::tau_pt_syst() {
  if (not tau_pt_syst_isLoaded) {
    if (tau_pt_syst_branch != 0) {
      tau_pt_syst_branch->GetEntry(index);
    } else {
      printf("branch tau_pt_syst_branch does not exist!\n");
      exit(1);
    }
    tau_pt_syst_isLoaded = true;
  }
  return *tau_pt_syst_;
}

const float &OpenTuple::XSection() {
  if (not XSection_isLoaded) {
    if (XSection_branch != 0) {
      XSection_branch->GetEntry(index);
    } else {
      printf("branch XSection_branch does not exist!\n");
      exit(1);
    }
    XSection_isLoaded = true;
  }
  return XSection_;
}

const float &OpenTuple::SumWeights() {
  if (not SumWeights_isLoaded) {
    if (SumWeights_branch != 0) {
      SumWeights_branch->GetEntry(index);
    } else {
      printf("branch SumWeights_branch does not exist!\n");
      exit(1);
    }
    SumWeights_isLoaded = true;
  }
  return SumWeights_;
}

const unsigned int &OpenTuple::largeRjet_n() {
  if (not largeRjet_n_isLoaded) {
    if (largeRjet_n_branch != 0) {
      largeRjet_n_branch->GetEntry(index);
    } else {
      printf("branch largeRjet_n_branch does not exist!\n");
      exit(1);
    }
    largeRjet_n_isLoaded = true;
  }
  return largeRjet_n_;
}

const vector<float> &OpenTuple::largeRjet_pt() {
  if (not largeRjet_pt_isLoaded) {
    if (largeRjet_pt_branch != 0) {
      largeRjet_pt_branch->GetEntry(index);
    } else {
      printf("branch largeRjet_pt_branch does not exist!\n");
      exit(1);
    }
    largeRjet_pt_isLoaded = true;
  }
  return *largeRjet_pt_;
}

const vector<float> &OpenTuple::largeRjet_eta() {
  if (not largeRjet_eta_isLoaded) {
    if (largeRjet_eta_branch != 0) {
      largeRjet_eta_branch->GetEntry(index);
    } else {
      printf("branch largeRjet_eta_branch does not exist!\n");
      exit(1);
    }
    largeRjet_eta_isLoaded = true;
  }
  return *largeRjet_eta_;
}

const vector<float> &OpenTuple::largeRjet_phi() {
  if (not largeRjet_phi_isLoaded) {
    if (largeRjet_phi_branch != 0) {
      largeRjet_phi_branch->GetEntry(index);
    } else {
      printf("branch largeRjet_phi_branch does not exist!\n");
      exit(1);
    }
    largeRjet_phi_isLoaded = true;
  }
  return *largeRjet_phi_;
}

const vector<float> &OpenTuple::largeRjet_E() {
  if (not largeRjet_E_isLoaded) {
    if (largeRjet_E_branch != 0) {
      largeRjet_E_branch->GetEntry(index);
    } else {
      printf("branch largeRjet_E_branch does not exist!\n");
      exit(1);
    }
    largeRjet_E_isLoaded = true;
  }
  return *largeRjet_E_;
}

const vector<float> &OpenTuple::largeRjet_m() {
  if (not largeRjet_m_isLoaded) {
    if (largeRjet_m_branch != 0) {
      largeRjet_m_branch->GetEntry(index);
    } else {
      printf("branch largeRjet_m_branch does not exist!\n");
      exit(1);
    }
    largeRjet_m_isLoaded = true;
  }
  return *largeRjet_m_;
}

const vector<float> &OpenTuple::largeRjet_truthMatched() {
  if (not largeRjet_truthMatched_isLoaded) {
    if (largeRjet_truthMatched_branch != 0) {
      largeRjet_truthMatched_branch->GetEntry(index);
    } else {
      printf("branch largeRjet_truthMatched_branch does not exist!\n");
      exit(1);
    }
    largeRjet_truthMatched_isLoaded = true;
  }
  return *largeRjet_truthMatched_;
}

const vector<float> &OpenTuple::largeRjet_D2() {
  if (not largeRjet_D2_isLoaded) {
    if (largeRjet_D2_branch != 0) {
      largeRjet_D2_branch->GetEntry(index);
    } else {
      printf("branch largeRjet_D2_branch does not exist!\n");
      exit(1);
    }
    largeRjet_D2_isLoaded = true;
  }
  return *largeRjet_D2_;
}

const vector<float> &OpenTuple::largeRjet_tau32() {
  if (not largeRjet_tau32_isLoaded) {
    if (largeRjet_tau32_branch != 0) {
      largeRjet_tau32_branch->GetEntry(index);
    } else {
      printf("branch largeRjet_tau32_branch does not exist!\n");
      exit(1);
    }
    largeRjet_tau32_isLoaded = true;
  }
  return *largeRjet_tau32_;
}

const vector<float> &OpenTuple::largeRjet_pt_syst() {
  if (not largeRjet_pt_syst_isLoaded) {
    if (largeRjet_pt_syst_branch != 0) {
      largeRjet_pt_syst_branch->GetEntry(index);
    } else {
      printf("branch largeRjet_pt_syst_branch does not exist!\n");
      exit(1);
    }
    largeRjet_pt_syst_isLoaded = true;
  }
  return *largeRjet_pt_syst_;
}

const vector<int> &OpenTuple::tau_charge() {
  if (not tau_charge_isLoaded) {
    if (tau_charge_branch != 0) {
      tau_charge_branch->GetEntry(index);
    } else {
      printf("branch tau_charge_branch does not exist!\n");
      exit(1);
    }
    tau_charge_isLoaded = true;
  }
  return *tau_charge_;
}


void OpenTuple::progress( int nEventsTotal, int nEventsChain ){
  int period = 1000;
  if (nEventsTotal%1000 == 0) {
    // xterm magic from L. Vacavant and A. Cerri
    if (isatty(1)) {
      if ((nEventsChain - nEventsTotal) > period) {
        float frac = (float)nEventsTotal/(nEventsChain*0.01);
        printf("\015\033[32m ---> \033[1m\033[31m%4.1f%%"
             "\033[0m\033[32m <---\033[0m\015", frac);
        fflush(stdout);
      }
      else {
        printf("\015\033[32m ---> \033[1m\033[31m%4.1f%%"
               "\033[0m\033[32m <---\033[0m\015", 100.);
        cout << endl;
      }
    }
  }
}

namespace tpl {

const int &runNumber() { return opentuple.runNumber(); }
const int &eventNumber() { return opentuple.eventNumber(); }
const int &channelNumber() { return opentuple.channelNumber(); }
const float &mcWeight() { return opentuple.mcWeight(); }
const float &scaleFactor_PILEUP() { return opentuple.scaleFactor_PILEUP(); }
const float &scaleFactor_ELE() { return opentuple.scaleFactor_ELE(); }
const float &scaleFactor_MUON() { return opentuple.scaleFactor_MUON(); }
const float &scaleFactor_PHOTON() { return opentuple.scaleFactor_PHOTON(); }
const float &scaleFactor_TAU() { return opentuple.scaleFactor_TAU(); }
const float &scaleFactor_BTAG() { return opentuple.scaleFactor_BTAG(); }
const float &scaleFactor_LepTRIGGER() { return opentuple.scaleFactor_LepTRIGGER(); }
const float &scaleFactor_PhotonTRIGGER() { return opentuple.scaleFactor_PhotonTRIGGER(); }
const bool &trigE() { return opentuple.trigE(); }
const bool &trigM() { return opentuple.trigM(); }
const bool &trigP() { return opentuple.trigP(); }
const unsigned int &lep_n() { return opentuple.lep_n(); }
const vector<bool> &lep_truthMatched() { return opentuple.lep_truthMatched(); }
const vector<bool> &lep_trigMatched() { return opentuple.lep_trigMatched(); }
const vector<float> &lep_pt() { return opentuple.lep_pt(); }
const vector<float> &lep_eta() { return opentuple.lep_eta(); }
const vector<float> &lep_phi() { return opentuple.lep_phi(); }
const vector<float> &lep_E() { return opentuple.lep_E(); }
const vector<float> &lep_z0() { return opentuple.lep_z0(); }
const vector<int> &lep_charge() { return opentuple.lep_charge(); }
const vector<unsigned int> &lep_type() { return opentuple.lep_type(); }
const vector<bool> &lep_isTightID() { return opentuple.lep_isTightID(); }
const vector<float> &lep_ptcone30() { return opentuple.lep_ptcone30(); }
const vector<float> &lep_etcone20() { return opentuple.lep_etcone20(); }
const vector<float> &lep_trackd0pvunbiased() { return opentuple.lep_trackd0pvunbiased(); }
const vector<float> &lep_tracksigd0pvunbiased() { return opentuple.lep_tracksigd0pvunbiased(); }
const float &met_et() { return opentuple.met_et(); }
const float &met_phi() { return opentuple.met_phi(); }
const unsigned int &jet_n() { return opentuple.jet_n(); }
const vector<float> &jet_pt() { return opentuple.jet_pt(); }
const vector<float> &jet_eta() { return opentuple.jet_eta(); }
const vector<float> &jet_phi() { return opentuple.jet_phi(); }
const vector<float> &jet_E() { return opentuple.jet_E(); }
const vector<float> &jet_jvt() { return opentuple.jet_jvt(); }
const vector<int> &jet_trueflav() { return opentuple.jet_trueflav(); }
const vector<bool> &jet_truthMatched() { return opentuple.jet_truthMatched(); }
const vector<float> &jet_MV2c10() { return opentuple.jet_MV2c10(); }
const unsigned int &photon_n() { return opentuple.photon_n(); }
const vector<bool> &photon_truthMatched() { return opentuple.photon_truthMatched(); }
const vector<bool> &photon_trigMatched() { return opentuple.photon_trigMatched(); }
const vector<float> &photon_pt() { return opentuple.photon_pt(); }
const vector<float> &photon_eta() { return opentuple.photon_eta(); }
const vector<float> &photon_phi() { return opentuple.photon_phi(); }
const vector<float> &photon_E() { return opentuple.photon_E(); }
const vector<bool> &photon_isTightID() { return opentuple.photon_isTightID(); }
const vector<float> &photon_ptcone30() { return opentuple.photon_ptcone30(); }
const vector<float> &photon_etcone20() { return opentuple.photon_etcone20(); }
const vector<int> &photon_convType() { return opentuple.photon_convType(); }
const unsigned int &tau_n() { return opentuple.tau_n(); }
const vector<float> &tau_pt() { return opentuple.tau_pt(); }
const vector<float> &tau_eta() { return opentuple.tau_eta(); }
const vector<float> &tau_phi() { return opentuple.tau_phi(); }
const vector<float> &tau_E() { return opentuple.tau_E(); }
const vector<bool> &tau_isTightID() { return opentuple.tau_isTightID(); }
const vector<bool> &tau_truthMatched() { return opentuple.tau_truthMatched(); }
const vector<bool> &tau_trigMatched() { return opentuple.tau_trigMatched(); }
const vector<int> &tau_nTracks() { return opentuple.tau_nTracks(); }
const vector<float> &tau_BDTid() { return opentuple.tau_BDTid(); }
const float &ditau_m() { return opentuple.ditau_m(); }
const vector<float> &lep_pt_syst() { return opentuple.lep_pt_syst(); }
const float &met_et_syst() { return opentuple.met_et_syst(); }
const vector<float> &jet_pt_syst() { return opentuple.jet_pt_syst(); }
const vector<float> &photon_pt_syst() { return opentuple.photon_pt_syst(); }
const vector<float> &tau_pt_syst() { return opentuple.tau_pt_syst(); }
const float &XSection() { return opentuple.XSection(); }
const float &SumWeights() { return opentuple.SumWeights(); }
const unsigned int &largeRjet_n() { return opentuple.largeRjet_n(); }
const vector<float> &largeRjet_pt() { return opentuple.largeRjet_pt(); }
const vector<float> &largeRjet_eta() { return opentuple.largeRjet_eta(); }
const vector<float> &largeRjet_phi() { return opentuple.largeRjet_phi(); }
const vector<float> &largeRjet_E() { return opentuple.largeRjet_E(); }
const vector<float> &largeRjet_m() { return opentuple.largeRjet_m(); }
const vector<float> &largeRjet_truthMatched() { return opentuple.largeRjet_truthMatched(); }
const vector<float> &largeRjet_D2() { return opentuple.largeRjet_D2(); }
const vector<float> &largeRjet_tau32() { return opentuple.largeRjet_tau32(); }
const vector<float> &largeRjet_pt_syst() { return opentuple.largeRjet_pt_syst(); }
const vector<int> &tau_charge() { return opentuple.tau_charge(); }

}
