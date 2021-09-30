import ROOT

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
    hNLeps = ROOT.TH1F("hNLeps","Example plot: Number of leptons; Number of leptons ; Events ",5,-0.5,4.5)
    hLepPt = ROOT.TH1F("hLepPt","Example plot: pT of leptons; p_{T} [GeV] ; Events times N_{leptons} ",25,0,250)
    hMll   = ROOT.TH1F("hMll",  "Example plot: Dilepton invariant mass; m_{ll} [GeV] ; Events ",100,0,500)

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
        for ilep in range(event.lep_n):
            #ilep zeigt den Index innerhalb der lep_n branches da.
            if event.lep_pt[ilep] < 20.*1000.:
                continue
            if abs(event.lep_eta[ilep]) > 2.5:
                continue
            if not event.lep_isTightID[ilep]:
                continue
            #Die selektierten Leptonen sind nun gut.
            nleps += 1
            if event.lep_trigMatched[ilep]:
                leptontriggereddata = True

        if not leptontriggereddata:
            continue
            
        #Jetzt fuellen wir unser erstes Histogram mit der nleps variable und dem Gewicht eventweight.
        hNLeps.Fill(nleps, eventweight)

        index1, index2 = -1, -1
        #Um eine per Lepton-Analyse zu machen, muessen wir wieder eine for-Schleife schreiben
        for ilep in range(event.lep_n):
            #ilep zeigt den Index innerhalb der lep_n branches da.
            if event.lep_pt[ilep] < 20.*1000.:
                continue
            if abs(event.lep_eta[ilep]) > 2.5:
                continue
            if not event.lep_isTightID[ilep]:
                continue
            #Hier speichern wir den transversalen Impuls der Leptonen ab.
            hLepPt.Fill(event.lep_pt[ilep]/1000.,eventweight)
            #Nun machen wir es etwas schwieriger, eine Variable, die sich aus 2 Leptonen besteht. Also brauchen wir eine Doppelschlaufe. Jetzt wirst du gleich merken, was es sich mit index1 und index2 auf sich hat.
            #Warum ist hier ein ilep+1
            for jlep in range(ilep+1,event.lep_n):
                if index1 >=0:
                    #Warum gibt es hier ein break Statement?
                    break
                if event.lep_pt[jlep] < 20.*1000.:
                    continue
                if abs(event.lep_eta[jlep]) > 2.5:
                    continue
                if not event.lep_isTightID[jlep]:
                    continue
                #Wir wollen ein e+e- oder ein mu+mu- Paar auswaehlen.
                #Zuerst testen wir den Lepton-Flavor. Uebrigens, fuer Elektronen/Positronen ist der Wert von lep_type 11, fuer Muonen ist er 13.
                if event.lep_type[ilep] != event.lep_type[jlep]:
                    continue
                #Und als naechstes, ob die Ladungen verschieden sind
                if event.lep_charge[ilep] == event.lep_charge[jlep]:
                    continue
                index1 = ilep
                index2 = jlep
                break

        if index1 >=0:
            #wir haben die Indizes fuer Mll.
            #Da diese Variable nicht sehr einfach zu berechnen ist, Habe ich hier die Berechnung aufgeschrieben. Was ich hier mache ist ein LorenzVektor aus den zwei Leptonen bauen, und die Masse mit der LorentzVector internen Funktion bestimmen.
            #Die Formel dafuer findest du z.B. hier: https://en.wikipedia.org/wiki/Invariant_mass#Example:_two-particle_collision
            #Ein Lorentzvektor ist z.B. hier beschrieben: https://de.wikipedia.org/wiki/Vierervektor
            lvlep1 = GetLorentzVector(event.lep_pt[index1],event.lep_eta[index1],event.lep_phi[index1],event.lep_E[index1])
            lvlep2 = GetLorentzVector(event.lep_pt[index2],event.lep_eta[index2],event.lep_phi[index2],event.lep_E[index2])
            Mll = (lvlep1+lvlep2).M()
            hMll.Fill(Mll,eventweight)
        
    print("Save results in "+outputname)
    #Nun sind wir aus der Ereignis(Event) Schleife, speichern wir unsere Resultate ab
    #Achtung, "recreate" sagt, dass die alte Datei geloescht und ueberschrieben werden soll.
    fout = ROOT.TFile(outputname,"recreate")
    hNLeps.Write()
    hLepPt.Write()
    hMll.Write()
    fout.Close()

#Eine Hilfsfunktion
#Erzeuge einen Lorentzvektor aus pt, eta, phi und E
def GetLorentzVector(pt, eta, phi, E):
    lvtemp = ROOT.Math.PtEtaPhiEVector(pt,eta,phi,E)
    #lv = ROOT.Math.LorentzVector(lvtemp)
    return lvtemp

def AnalyzeAll():
    basepath = "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/2lep/" #from internet
    #basepath = "/lustre/fs22/group/atlas/haweber/SchuelerProjekte/ATLASOpenData/13TeV/2lep/" #local path
    
    AnalyzeOneDataset(True, basepath+"Data/data_A.2lep.root",            "output/data_A.root")
    AnalyzeOneDataset(True, basepath+"Data/data_B.2lep.root",            "output/data_B.root")
    AnalyzeOneDataset(True, basepath+"Data/data_C.2lep.root",            "output/data_C.root")
    AnalyzeOneDataset(True, basepath+"Data/data_D.2lep.root",            "output/data_D.root")
    AnalyzeOneDataset(False,basepath+"MC/mc_361106.Zee.2lep.root",       "output/mc_Zee.root")
    AnalyzeOneDataset(False,basepath+"MC/mc_361107.Zmumu.2lep.root",     "output/mc_Zmumu.root")
    AnalyzeOneDataset(False,basepath+"MC/mc_361108.Ztautau.2lep.root",   "output/mc_Ztautau.root")
    AnalyzeOneDataset(False,basepath+"MC/mc_410000.ttbar_lep.2lep.root", "output/mc_tt2l.root")
    AnalyzeOneDataset(False,basepath+"MC/mc_363492.llvv.2lep.root",      "output/mc_WW2l.root")
    
