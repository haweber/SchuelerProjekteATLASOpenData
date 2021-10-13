import ROOT
import math

#In diesem Skript haben wir drei Funktionen bestimmt
#Die erste ist AnalyzeOneDataset - die Hauptfunktion
#Die zweite ist GetLorentzVector - eine Hilfsfunktion, die in AnalyzeOneDataset aufgerufen wird
#Die dritte ist AnalyzeAll - ruft die Hauptfunktion fuer mehrere Datensaetze auf


#Hier definieren wir eine Funktion, welche das Hauptprogramm ist. Wir wollen am Ende alle Daten analysieren, allerdings werden wir das nacheinander machen. Diese funktion wird es uns erlauben, der Funktion den Ort der Eingabedaten mitzuteilen wie auch den Ort, bei dem wir unsere Resultate speichern. Zudem zeigen wir an, ob das inputfile echte Daten sind (oder Simulation)
def AnalyzeOneDataset(isdata, inputname, outputname):

    print("Open file " + inputname)
    #zuerst oeffnen wir die Eingabedatei und rufen das ntuple in dem File auf (das ist der tree)
    f = ROOT.TFile.Open(inputname) ## 13 TeV sample
    tree = f.Get("mini")

    #Danach definieren wir hier die Histogramme, welche unseren Datenresultate darstellen. D.h. hier definieren wir die Distributionen, welche wir anschauen wollen.
    #Im Beispiel zeige ich drei Histogramme, eines davon werden wir haeufiger betrachten.
    #Das Format ist so, dass wir zuerst den Python-Variablen-Name initialisieren mit einem ROOT.TH1F (1D histogram mit floating-point precision).
    #Dieses ROOT.TH1F braucht 5 (4) Eingaben, zuerst der ROOT-Variablen-Name (wie ROOT das Histogramm speichert), einen beschreibenen Titel (Histogramm-Titel; x-Achsenbeschreibung; y-Achsenbeschreibung), die Anzahl von Abschnitten (nbins), sowie die Histogramm-Grenzen der x-Achse
    hNLeps = ROOT.TH1F("hNLeps", "Example plot: Number of leptons; Number of leptons ; Events ",5,-0.5,4.5)
    hLepPt = ROOT.TH1F("hLepPt", "Example plot: pT of leptons; p_{T} [GeV] ; Events times N_{leptons} ",25,0,250)
    hETmiss= ROOT.TH1F("hETmiss","Example plot: Missing transverse momentum; p_{T}^{miss} [GeV] ; Events",50,0,500)
    hMT    = ROOT.TH1F("hMT",  "  Example plot: Transverse mass; m_{T} [GeV] ; Events ",100,0,500)

    #Als naechstes wollen wir die Analyse durchfuehren. Dazu schauen wir also die Ereignisse (events) im ntuple an
    print("Analyze "+ str(tree.GetEntries())+" events")
    eventcounter = 0
    for event in tree:
        if eventcounter%int(tree.GetEntries()/20)==0:
            print("Processed "+str(eventcounter)+"/"+tree.GetEntries()+" events")
        eventcounter += 1
        #Jedes event hat die Eigenschaften, die ATLAS hier angibt: http://opendata.atlas.cern/release/2020/documentation/datasets/dataset13.html
        #Bespreche mit deinem Betreuer, was diese bedeuten.

        #Zuerst brauchen wir ein Eventweight. Diese Gewichtung ist fuer die Simulation wichtig, allerdings soll Sie nicht fuer Daten geaendert werden.
        eventweight = 1
        if not isdata:
            #Dieses Gewicht ist dafuer zustaendig, dass sich die Simulation sich an die Daten anschmiegt (beziehungsweise dies sollte)
            eventweight *= event.mcWeight*event.scaleFactor_PILEUP*event.scaleFactor_ELE*event.scaleFactor_MUON*event.scaleFactor_LepTRIGGER*event.XSection/event.SumWeights*event.10000.

        #Nun schauen wir uns die Daten an. Da wir nur Ereignisse wollen, die von Leptonentrigger selektiert wurden, machen wir hier eine Selektion.
        #Theoretisch sollten wir uns Elektronen und Muonen separat anschauen, aber fuer dieses Beispiel schauen wir es uns kombiniert an
        if not event.trigE and not event.trigM:
            continue

        #Wir haben lep_n als Auswahl, aber wir schauen uns nur bestimmte Leptonen an. Unsere Selektion ist zwar schon in den ATLAS OpenData fuer uns getan, aber es ist gut, selbst eine Selektion zu bestimmen.
        #Zuerst testen wir, ob wir ueberhaupt gute Leptonen haben
        leptontriggereddata = False
        nleps = 0
        index = -1
        for ilep in range(event.lep_n):
            #ilep zeigt den Index innerhalb der lep_n branches da.
            if event.lep_pt[ilep] < 20.*1000.: #minimaler Impuls
                continue
            if abs(event.lep_eta[ilep]) > 2.5:#zentral im Detektor
                continue
            if not event.lep_isTightID[ilep]:#Klare Identifikation als Lepton
                continue
            if event.lep_ptcone30[ilep]/event.lep_pt[ilep]>0.15:#isoliert von anderen Objekten (Track basiert)
                continue
            if event.etcone20[ilep]/event.lep_pt[ilep]>0.15:#isoliert von anderen Objekten (Kalorimeter basiert)
                continue
            if event.lep_type[ilep]==11 and abs(event.lep_eta[ilep]) > 1.37 and abs(event.lep_eta[ilep]) > 1.52:#Besonderheit fuer Elektronen/Positronen
                continue
            #Die selektierten Leptonen sind nun gut.
            nleps += 1
            if event.lep_trigMatched[ilep]:
                leptontriggereddata = True
            if index<0:
                index = ilep
            hLepPt.Fill(event.lep_pt[ilep]/1000.,eventweight)

        if not leptontriggereddata:
            continue
            
        #Jetzt fuellen wir ein Histogram mit der nleps variable und dem Gewicht eventweight.
        hNLeps.Fill(nleps, eventweight)
        hETmiss.Fill(event.met_et/1000., eventweight)

        if inde1 >=0:
            #wir haben den Index fuer MT.
            #Da diese Variable nicht sehr einfach zu berechnen ist, Habe ich hier die Berechnung aufgeschrieben. Was ich hier mache ist ein LorenzVektor aus den zwei Leptonen bauen, und die Masse mit der LorentzVector internen Funktion bestimmen.
            #Die Formel dafuer findest du z.B. hier: https://en.wikipedia.org/wiki/Invariant_mass#Example:_two-particle_collision
            #Ein Lorentzvektor ist z.B. hier beschrieben: https://de.wikipedia.org/wiki/Vierervektor
            lvlep = GetLorentzVector(event.lep_pt[index],event.lep_eta[index],event.lep_phi[index],event.lep_E[index])
            lvmet = GetLorentzVector(event.met_et,event.0.,event.met_phi,event.met_et)
            MT = math.sqrt( math.pow(lvlep.M(),2)+math.pow(lvmet.M(),2) + 2*(lvlep.Et()*lvmet.Et() - lvlep.Px()*lvmet.Px() - lvlep.Py()*lvmet.Py() ) ) / 1000.
            hMT.Fill(MT,eventweight)
    
    print("Save results in "+outputname)
    #Nun sind wir aus der Ereignis(Event) Schleife, speichern wir unsere Resultate ab
    #Achtung, "recreate" sagt, dass die alte Datei geloescht und ueberschrieben werden soll.
    fout = ROOT.TFile(outputname,"recreate")
    hNLeps.Write()
    hLepPt.Write()
    hETmiss.Write()
    hMT.Write()
    fout.Close()

#Eine Hilfsfunktion
#Erzeuge einen Lorentzvektor aus pt, eta, phi und E
def GetLorentzVector(pt, eta, phi, E):
    lvtemp = ROOT.Math.PtEtaPhiEVector(pt,eta,phi,E)
    #lv = ROOT.Math.LorentzVector(lvtemp)
    return lvtemp

def AnalyzeAll():
    basepath = "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1lep/" #from internet
    #basepath = "/lustre/fs22/group/atlas/haweber/SchuelerProjekte/ATLASOpenData/13TeV/1lep/" #local path

    AnalyzeOneDataset(True, basepath+"Data/data_A.1lep.root",                       "output/data_A.root")
    AnalyzeOneDataset(True, basepath+"Data/data_B.1lep.root",                       "output/data_B.root")
    AnalyzeOneDataset(True, basepath+"Data/data_C.1lep.root",                       "output/data_C.root")
    AnalyzeOneDataset(True, basepath+"Data/data_D.1lep.root",                       "output/data_D.root")
    AnalyzeOneDataset(False,basepath+"MC/mc_361100.Wplusenu.1lep.root",             "output/mc_Wpenu.root")
    AnalyzeOneDataset(False,basepath+"MC/mc_361101.Wplusmunu.1lep.root",            "output/mc_Wpmunu.root")
    AnalyzeOneDataset(False,basepath+"MC/mc_361102.Wplustaunu.1lep.root",           "output/mc_Wptaunu.root")
    AnalyzeOneDataset(False,basepath+"MC/mc_361103.Wminusenu.1lep.root",            "output/mc_Wmenu.root")
    AnalyzeOneDataset(False,basepath+"MC/mc_361104.Wminusmunu.1lep.root",           "output/mc_Wmmunu.root")
    AnalyzeOneDataset(False,(basepath+"MC/mc_361105.Wminustaunu.1lep.root",         "output/mc_Wmtaunu.root")
    AnalyzeOneDataset(False,basepath+"MC/mc_410000.ttbar_lep.1lep.root",            "output/mc_tt1l.root")
    AnalyzeOneDataset(False,basepath+"MC/mc_363492.llvv.1lep.root",                 "output/mc_WW2l.root")
    AnalyzeOneDataset(False,basepath+"MC/mc_363359.WpqqWmlv.1lep.root",             "output/mc_WWm1l.root")
    AnalyzeOneDataset(False,basepath+"MC/mc_363360.WplvWmqq.1lep.root",             "output/mc_WWp1l.root")
    AnalyzeOneDataset(False,basepath+"MC/mc_363489.WlvZqq.1lep.root",               "output/mc_WZ1l.root")
    AnalyzeOneDataset(False,basepath+"MC/mc_361106.Zee.1lep.root",                  "output/mc_Zee.root")
    AnalyzeOneDataset(False,basepath+"MC/mc_361107.Zmumu.1lep.root",                "output/mc_Zmumu.root")
    AnalyzeOneDataset(False,basepath+"MC/mc_361108.Ztautau.1lep.root",              "output/mc_Ztautau.root")
    AnalyzeOneDataset(False,basepath+"MC/mc_410011.single_top_tchan.1lep.root",     "output/mc_t_t.root")
    AnalyzeOneDataset(False,basepath+"MC/mc_410012.single_antitop_tchan.1lep.root", "output/mc_tbar_t.root")
    AnalyzeOneDataset(False,basepath+"MC/mc_410025.single_top_schan.1lep.root",     "output/mc_t_s.root")
    AnalyzeOneDataset(False,basepath+"MC/mc_410026.single_antitop_schan.1lep.root", "output/mc_tbar_s.root")
    AnalyzeOneDataset(False,basepath+"MC/mc_410013.single_top_wtchan.1lep.root",    "output/mc_t_tW.root")
    AnalyzeOneDataset(False,basepath+"MC/mc_410014.single_antitop_wtchan.1lep.root","output/mc_tbar_tW.root")

