import ROOT

#In diesem Skript haben wir drei Funktionen bestimmt
#Die erste ist AnalyzeOneDataset - die Hauptfunktion
#Die zweite ist GetLorentzVector - eine Hilfsfunktion, die in AnalyzeOneDataset aufgerufen wird
#Die dritte ist AnalyzeAll - ruft die Hauptfunktion fuer mehrere Datensaetze auf


#Hier definieren wir eine Funktion, welche das Hauptprogramm ist. Wir wollen am Ende alle Daten analysieren, allerdings werden wir das nacheinander machen. Diese funktion wird es uns erlauben, der Funktion den Ort der Eingabedaten mitzuteilen wie auch den Ort, bei dem wir unsere Resultate speichern. Zudem zeigen wir an, ob das inputfile echte Daten sind (oder Simulation)
def AnalyzeOneDataset(isdata, inputname, outputname):
    _mZ = 91.18
    
    print("Open file " + inputname)
    #zuerst oeffnen wir die Eingabedatei und rufen das ntuple in dem File auf (das ist der tree)
    f = ROOT.TFile.Open(inputname) ## 13 TeV sample
    tree = f.Get("mini")

    #Danach definieren wir hier die Histogramme, welche unseren Datenresultate darstellen. D.h. hier definieren wir die Distributionen, welche wir anschauen wollen.
    #Im Beispiel zeige ich drei Histogramme, eines davon werden wir haeufiger betrachten.
    #Das Format ist so, dass wir zuerst den Python-Variablen-Name initialisieren mit einem ROOT.TH1F (1D histogram mit floating-point precision).
    #Dieses ROOT.TH1F braucht 5 (4) Eingaben, zuerst der ROOT-Variablen-Name (wie ROOT das Histogramm speichert), einen beschreibenen Titel (Histogramm-Titel; x-Achsenbeschreibung; y-Achsenbeschreibung), die Anzahl von Abschnitten (nbins), sowie die Histogramm-Grenzen der x-Achse
    hNLeps  = ROOT.TH1F("hNLeps", "Example plot: Number of leptons; Number of leptons ; Events ",7,-0.5,6.5)
    hNLepsT = ROOT.TH1F("hNLepsT","Example plot: Number of triggering leptons; Number of triggering leptons ; Events ",5,-0.5,4.5)
    hLepPt  = ROOT.TH1F("hLepPt", "Example plot: pT of leptons; p_{T} [GeV] ; Events times N_{leptons} ",25,0,250)
    hMll_1  = ROOT.TH1F("hMll_1", "Example plot: Dilepton invariant mass closest to Z Mass; m_{ll}^{lead} [GeV] ; Events ",30,0,150)
    hMll_2  = ROOT.TH1F("hMll_2", "Example plot: Dilepton invariant mass further from Z Mass; m_{ll}^{sub} [GeV] ; Events ",30,0,150)
    hMllll  = ROOT.TH1F("hMllll", "Example plot: 4-lepton invariant mass; m_{llll} [GeV] ; Events ",100,0,500)

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
        nlepsT = 0
        indices = []
        for ilep in range(event.lep_n):
            #ilep zeigt den Index innerhalb der lep_n branches da.
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
            if event.lep_pt[ilep] < 7.*1000.: #minimaler Impuls
                continue
            #Die selektierten Leptonen sind nun gut.
            nleps += 1
            indices += [ilep]
            hLepPt.Fill(event.lep_pt[ilep]/1000.,eventweight)#keine Ueberpruefung, ob Trigger durch ein ausgewaehltes Lepton ausgeloest wurde
            if event.lep_pt[ilep] < 25.*1000.: #minimaler Impuls fuer Trigger
                continue
            nlepsT += 1
            if event.lep_trigMatched[ilep]:
                leptontriggereddata = True

        if not leptontriggereddata:
            continue
            
        #Jetzt fuellen wir unser erstes Histogram mit der nleps variable und dem Gewicht eventweight.
        hNLeps.Fill(nleps, eventweight)
        hNLepsT.Fill(nlepsT, eventweight)

        if nleps<4:
            continue

        #Impulse der ATLAS HZZ Analyse
        if event.lep_pt[indices[0] ]<25.*1000.:
            continue
        if event.lep_pt[indices[1] ]<15.*1000.:
            continue
        if event.lep_pt[indices[2] ]<20.*1000.:
            continue
        if event.lep_pt[indices[3] ]< 7.*1000.:
            continue

        #wir haben die Indizes fuer Mllll.
        #Allerdings gibt es hier einige Selektionen: Wir wollen zwei Z-Zerfaelle, also zwei Paare e+e- oder mu+mu-. D.h. H --> e+e-e+e-, e+e-mu+mu-, mu+mu-mu+mu-
        #Da diese Variable nicht sehr einfach zu berechnen ist, Habe ich hier die Berechnung aufgeschrieben. Was ich hier mache ist ein LorenzVektor aus den zwei Leptonen bauen, und die Masse mit der LorentzVector internen Funktion bestimmen.
        #Die Formel dafuer findest du z.B. hier: https://en.wikipedia.org/wiki/Invariant_mass#Example:_two-particle_collision
        #Ein Lorentzvektor ist z.B. hier beschrieben: https://de.wikipedia.org/wiki/Vierervektor
        lvZ1, lvZ2 = GetLorentzVector(0,0,0,0), GetLorentzVector(0,0,0,0)
        #Die fuenf naechsten Zeilen helfen, schneller zu programmieren
        i1, i2, i3, i4 = indices[0], indices[1], indices[2], indices[3]
        lvlep1 = GetLorentzVector(event.lep_pt[i1],event.lep_eta[i1],event.lep_phi[i1],event.lep_E[i1])
        lvlep2 = GetLorentzVector(event.lep_pt[i2],event.lep_eta[i2],event.lep_phi[i2],event.lep_E[i2])
        lvlep3 = GetLorentzVector(event.lep_pt[i3],event.lep_eta[i3],event.lep_phi[i3],event.lep_E[i3])
        lvlep4 = GetLorentzVector(event.lep_pt[i4],event.lep_eta[i4],event.lep_phi[i4],event.lep_E[i4])
        #dM ist Abstand zur Z-Bosonenmasse
        dM = 99999.
        if ((event.lep_type[i1] == event.lep_type[i2]) and (event.lep_charge[i1] != event.lep_charge[i2])) and ((event.lep_type[i3] == event.lep_type[i4]) and (event.lep_charge[i3] != event.lep_charge[i4])):
            M1 = (lvlep1+lvlep2).M()/1000.
            M2 = (lvlep3+lvlep4).M()/1000.
            if abs(M1-_MZ) < abs(M2-_MZ):
                if abs(M1-_MZ)<dM:
                    dM = abs(M1-_MZ)
                    lvZ1 = (lvlep1+lvlep2)
                    lvZ2 = (lvlep3+lvlep4)
            else:
                if abs(M2-_MZ)<dM:
                    dM = abs(M2-_MZ)
                    lvZ1 = (lvlep3+lvlep4)
                    lvZ2 = (lvlep1+lvlep2)
        #Habe Kombination (12) (34) getestet.
        if ((event.lep_type[i1] == event.lep_type[i3]) and (event.lep_charge[i1] != event.lep_charge[i3])) and ((event.lep_type[i2] == event.lep_type[i4]) and (event.lep_charge[i2] != event.lep_charge[i4])):
            M1 = (lvlep1+lvlep3).M()/1000.
            M2 = (lvlep2+lvlep4).M()/1000.
            if abs(M1-_MZ) < abs(M2-_MZ):
                if abs(M1-_MZ)<dM:
                    dM = abs(M1-_MZ)
                    lvZ1 = (lvlep1+lvlep3)
                    lvZ2 = (lvlep2+lvlep4)
            else:
                if abs(M2-_MZ)<dM:
                    dM = abs(M2-_MZ)
                    lvZ1 = (lvlep2+lvlep4)
                    lvZ2 = (lvlep1+lvlep3)
        #Habe Kombination (13) (24) getestet.
        if ((event.lep_type[i1] == event.lep_type[i4]) and (event.lep_charge[i1] != event.lep_charge[i4])) and ((event.lep_type[i2] == event.lep_type[i3]) and (event.lep_charge[i2] != event.lep_charge[i3])):
            M1 = (lvlep1+lvlep4).M()/1000.
            M2 = (lvlep2+lvlep3).M()/1000.
            if abs(M1-_MZ) < abs(M2-_MZ):
                if abs(M1-_MZ)<dM:
                    dM = abs(M1-_MZ)
                    lvZ1 = (lvlep1+lvlep4)
                    lvZ2 = (lvlep2+lvlep3)
            else:
                if abs(M2-_MZ)<dM:
                    dM = abs(M2-_MZ)
                    lvZ1 = (lvlep2+lvlep3)
                    lvZ2 = (lvlep1+lvlep4)
        #Habe Kombination (14) (24) getestet.

        #Jetzt haben wir 2 Z Bosonen, falls dM geaendert wurde.
        if dM < 99000.:
           hMll_1.Fill(lvZ1.M()/1000., eventweight)
           hMll_2.Fill(lvZ2.M()/1000., eventweight)
           hMllll.Fill((lvZ1+lvZ2).M()/1000., eventweight)
         
   
        
    print("Save results in "+outputname)
    #Nun sind wir aus der Ereignis(Event) Schleife, speichern wir unsere Resultate ab
    #Achtung, "recreate" sagt, dass die alte Datei geloescht und ueberschrieben werden soll.
    fout = ROOT.TFile(outputname,"recreate")
    hNLeps.Write()
    hNLepsT.Write()
    hLepPt.Write()
    hMll_1.Write()
    hMll_2.Write()
    hMllll.Write()
    fout.Close()

#Eine Hilfsfunktion
#Erzeuge einen Lorentzvektor aus pt, eta, phi und E
def GetLorentzVector(pt, eta, phi, E):
    lvtemp = ROOT.Math.PtEtaPhiEVector(pt,eta,phi,E)
    #lv = ROOT.Math.LorentzVector(lvtemp)
    return lvtemp

def AnalyzeAll():
    basepath = "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/" #from internet
    #basepath = "/lustre/fs22/group/atlas/haweber/SchuelerProjekte/ATLASOpenData/13TeV/4lep/" #local path
    
    AnalyzeOneDataset(True, basepath+"Data/data_A.4lep.root",                 "output/data_A.root")
    AnalyzeOneDataset(True, basepath+"Data/data_B.4lep.root",                 "output/data_B.root")
    AnalyzeOneDataset(True, basepath+"Data/data_C.4lep.root",                 "output/data_C.root")
    AnalyzeOneDataset(True, basepath+"Data/data_D.4lep.root",                 "output/data_D.root")
    AnalyzeOneDataset(False,basepath+"MC/mc_361106.Zee.4lep.root",            "output/mc_Zee.root")
    AnalyzeOneDataset(False,basepath+"MC/mc_361107.Zmumu.4lep.root",          "output/mc_Zmumu.root")
    AnalyzeOneDataset(False,basepath+"MC/mc_361108.Ztautau.4lep.root",        "output/mc_Ztautau.root")
    AnalyzeOneDataset(False,basepath+"MC/mc_363491.lllv.4lep.root",           "output/mc_WZ3lnu.root")
    AnalyzeOneDataset(False,basepath+"MC/mc_363490.llll.4lep.root",           "output/mc_ZZ4l.root")
    AnalyzeOneDataset(False,basepath+"MC/mc_345060.ggH125_ZZ4lep.4lep.root",  "output/mc_ggH_HZZ.root")
    AnalyzeOneDataset(False,basepath+"MC/mc_344235.VBFH125_ZZ4lep.4lep.root", "output/mc_Ztautau.root")
    AnalyzeOneDataset(False,basepath+"MC/mc_341947.ZH125_ZZ4lep.4lep.root",   "output/mc_Ztautau.root")
    AnalyzeOneDataset(False,basepath+"MC/mc_341964.WH125_ZZ4lep.4lep.root",   "output/mc_Ztautau.root")

AnalyzeAll()
