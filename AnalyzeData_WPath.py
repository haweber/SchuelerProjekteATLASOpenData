import uproot
import numpy as np
#import pandas as pd
#import uproot3_methods #if you want to use lorentzvectors
import argparse
import os
#from scipy.optimize import curve_fit

### Diese Funktion wird immer aufgerufen
def main(args):
    print("Welcome to the WPath analysis.")
    ntupledir = os.path.join(args.inputdir,"")
    ### zuerst laden wir die Daten mit uproot
    ### bemerke, der code crashed, falls die drei Dateien nicht existieren
    fileData = uproot.open(ntupledir+"data_1lep.root")["events"]
    fileSignal = uproot.open(ntupledir+"simulation_signal_1lep.root")["events"]
    fileBackground = uproot.open(ntupledir+"simulation_background_1lep.root")["events"]
    print("Loading files from " + ntupledir)
    ### Hier bearbeiten wir die Daten. Damit wir den Code nicht dreimal wiederholen muessen (ATLAS-Daten, Sim,ulation von Z-Teilchen und Simulation von anderen Prozessen die Elektronen-Positron / Muon-Antimuon-Paare erzeigen)
    processEvents(fileData,      True, False,args)
    processEvents(fileSignal,    False,True, args)
    processEvents(fileBackground,False,False,args)

    ### Das ist das Ende dieser Funktion
    print("Analysis done. Plotting is done with MakePlot.py")






### Diese Funktion verwenden wir, um Daten und Simulationen zu analysieren.
def processEvents(inputfile, isdata, issignal, args):
    ### Das brauchen wir spaeter - wo speichern wir unsere Resultate ab.    
    outdir = os.path.join(args.savedir,"")
    ### Stelle sicher, dass das Verzeichnis, in welche wir die Daten speichern wollen, existiert. Falls nicht, wird es erzeugt.
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    appendname = ""
    if isdata:
        appendname = "Data"
    elif issignal:
        appendname = "Signal"   
    else:
        appendname = "Background"
    print("Running over " + appendname)
    appendname = "_"+appendname + ".npz"
        
    ### zuerst laden wir die Daten in sogenannte numpy-Arrays
    arrays = inputfile.arrays()
    ### die Arrays sind hier beschrieben:
    """
    arrays["lep1_px"] # x-Komponente des Impulses des ersten Leptons, -999 falls Ereignisse keine Leptonen hat
    arrays["lep1_py"] # y-Komponente des Impulses des ersten Leptons, -999 falls Ereignisse keine Leptonen hat
    arrays["lep1_pz"] # z-Komponente des Impulses des ersten Leptons, -999 falls Ereignisse keine Leptonen hat
    arrays["lep1_E"]  # Energie des ersten Leptons, -999 falls Ereignisse keine Leptonen hat
    arrays["lep1_id"] # Lepton-ID (siehe unten) des ersten Leptons, -999 falls Ereignisse keine Leptonen hat
    arrays["lep2_px"] # x-Komponente des Impulses des zweiten Leptons, -999 falls Ereignisse nur ein Lepton hat
    arrays["lep2_py"] # y-Komponente des Impulses des zweiten Leptons, -999 falls Ereignisse nur ein Lepton hat
    arrays["lep2_pz"] # z-Komponente des Impulses des zweiten Leptons, -999 falls Ereignisse nur ein Lepton hat
    arrays["lep2_E"]  # Energie des zweiten Leptons, -999 falls Ereignisse nur ein Lepton hat
    arrays["lep2_id"] # Lepton-ID (siehe unten) des zweiten Leptons, -999 falls Ereignisse nur ein Lepton hat
    arrays["lep3_px"] # x-Komponente des Impulses des dritten Leptons, -999 falls Ereignisse nur zwei Leptonen hat
    arrays["lep3_py"] # y-Komponente des Impulses des dritten Leptons, -999 falls Ereignisse nur zwei Leptonen hat
    arrays["lep3_pz"] # z-Komponente des Impulses des dritten Leptons, -999 falls Ereignisse nur zwei Leptonen hat
    arrays["lep3_E"]  # Energie des dritten Leptons, -999 falls Ereignisse nur zwei Leptonen hat
    arrays["lep3_id"] # Lepton-ID (siehe unten) des dritten Leptons, -999 falls Ereignisse nur zwei Leptonen hat
    arrays["lep4_px"] # x-Komponente des Impulses des vierten Leptons, -999 falls Ereignisse nur drei Leptonen hat
    arrays["lep4_py"] # y-Komponente des Impulses des vierten Leptons, -999 falls Ereignisse nur drei Leptonen hat
    arrays["lep4_pz"] # z-Komponente des Impulses des vierten Leptons, -999 falls Ereignisse nur drei Leptonen hat
    arrays["lep4_E"]  # Energie des vierten Leptons, -999 falls Ereignisse nur drei Leptonen hat
    arrays["lep4_id"] # Lepton-ID (siehe unten) des vierten Leptons, -999 falls Ereignisse nur drei Leptonen hat
    arrays["met_px"]  # x-Komponente des transversalen fehlenden Impulses (Mass fuer Neutrino-Impuls)
    arrays["met_py"]  # y-Komponente des transversalen fehlenden Impulses (Mass fuer Neutrino-Impuls)
    arrays["weight"]  # Da man ja beliebig viele Simulationsereignisse produzieren kann, muss man diese Gewichten, damit sie der zu analysierenden Datenmenge entspricht. Dies macht man mit dieser Variable
    ### Kommentar zu lepton-ID: Identifikation, ob das Lepton ein Elektron (id == 11), Positron (id == -11), Muon (id == 13) oder Anti-Muon (id == -13) ist
    ### Kommentar zu met: Bei Proton-Proton-Kollisionen kann man kein met_pz abschaetzen, da Protonen keine fundamentalen Teilchen sind.
    """
    ### nun erstellen wir Masken:
    ### in Numpy arrays can man "&" fuer "UND" und "|"  fuer "ODER" verwenden. Ansonsten gilt in python, dass "and" als "UND" und "or" als "ODER" verwendet.
    ### Ereignis muss genau ein Lepton haben
    onelep_mask = ((arrays['lep1_E' ] >= 0) & (arrays['lep2_E' ] < 0))
    ### Lepton muss mindestens 35 GeV als transversalen Impuls haben
    onelep_pt_mask = (onelep_mask & (np.sqrt(arrays["lep1_px"]**2+arrays["lep1_py"]**2)>35.))
    ### Das Lepton muss gut im Spurendetektor und Kalorimeter detektierbar sein (eta gibt den Bereich dieser Detektoren an).
    lep1_eta = -np.log(np.tan( np.arccos(arrays["lep1_pz"] / np.sqrt(arrays["lep1_px"]**2+arrays["lep1_py"]**2+arrays["lep1_pz"]**2))/2.))
    onelep_eta_mask = (onelep_pt_mask & (((np.abs(arrays['lep1_id'])==13) & (np.abs(lep1_eta)<2.5)) | ((np.abs(arrays['lep1_id'])==11) & ((np.abs(lep1_eta)<2.5) & ((np.abs(lep1_eta)<1.52) | (np.abs(lep1_eta)<1.37))))))
    ### Es muss einen minimalen transversalen fehlenden Impuls geben, was das Vorhandensein eines Neutrinos angibt 
    met_mask = (np.sqrt(arrays["met_px"]**2+arrays["met_py"]**2)>30.)
    evt_mask = onelep_eta_mask & met_mask
    ### Wir moechten nun alle Ereignisse herausfiltern, welche diese Bedingungen nicht erfuellen --> invert
    filters = np.invert(evt_mask)
    ### erzeuge gefilterte Objekte - fuer das W-Boson interessieren uns nur Lepton 1, met und der weights-array
    lep1_px = np.delete(arrays['lep1_px'],filters)
    lep1_py = np.delete(arrays['lep1_py'],filters)
    lep1_pz = np.delete(arrays['lep1_pz'],filters)
    lep1_E  = np.delete(arrays['lep1_E' ],filters)
    lep1_id = np.delete(arrays['lep1_id'],filters)
    met_px = np.delete(arrays['met_px'],filters)
    met_py = np.delete(arrays['met_py'],filters)
    weight = np.delete(arrays['weight'],filters)

    ### Nun wollen wir die transversale Masse berechnen. In den Kommentaren ist der "korrekte Weg" (vollstaendige Formel).
    ### Der vereinfachte Weg (bei dem wir annehmen, dass die Leptonenmasse vernachlaessigbar ist), ist unkommentiert

    """
    ## Zuerst der vollstaendige Weg
    ## Zuerst die transversale Energie
    lep1_m2 = lep1_E**2 - (lep1_px**2+lep1_py**2+lep1_pz**2)
    np.asarray(lep1_m2)[lep1_m2 < 0] = 0
    #lep1_m2[lep1_m2 < 0] = 0 # wir erlauben keine negative Masse
    lep1_Et = np.sqrt(lep1_m2 + (lep1_px**2+lep1_py**2))  # Et = sqrt(m^2 + pT^2)
    met_Et = np.sqrt((met_px**2+met_py**2))  # Et = sqrt(m^2 + pT^2), fuer met ist m=0
    ## Dann transversale Masse zum Quadrat
    MT_squared_full = (lep1_Et + met_Et)**2 - ( (lep1_px+met_px)**2 + (lep1_py+met_py)**2 )
    """
    ## Beim vereinfachten Weg, fehlt uns nur der Winkel zwischen dem Lepton und MET in der transversalen Ebene
    dphi = np.arctan2(lep1_py,lep1_px) - np.arctan2(met_py,met_px) #dies ist nicht genau der Winkel (warum nicht?) - aber mit cos(dphi) stimmt es.
    ## Vereinfachte transversale Masse zum Quadrat
    MT_squared = 2*np.sqrt(lep1_px**2+lep1_py**2)*np.sqrt(met_px**2+met_py**2)*(1-np.cos(dphi))

    """
    ### Pathologische Faelle tauchen nur bei der vollen Berechnung auf
    ### Redefiniere Filter:
    filters = (MT_squared_full < 0) | (MT_squared < 0) # es gibt pathologische Faelle, bei der diese Groesse negativ wird. Falls das passiert, koennen wir nicht die Wurzel ziehen.

    ### Filtere die pathologischen Faelle
    lep1_px = np.delete(lep1_px,filters)
    lep1_py = np.delete(lep1_py,filters)
    lep1_pz = np.delete(lep1_pz,filters)
    lep1_E  = np.delete(lep1_E ,filters)
    lep1_id = np.delete(lep1_id,filters)
    met_px = np.delete(met_px,filters)
    met_py = np.delete(met_py,filters)
    weight = np.delete(weight,filters)
    MT_squared_full = np.delete(MT_squared_full,filters)
    MT_squared = np.delete(MT_squared,filters)
    """
    
    ### interessanten Groessen sind:
    ## transversale Impulse: pT = np.sqrt(px**2 + py**2)
    ## Winkel phi (in Ebene senkrecht zum Protonstrahl): phi = np.arctan2(py,px)
    ## Winkel theta (Winkel bezueglich Protonstrahl): theta = np.arccos(pz / np.sqrt(px**2 + py**2 + pz**2))
    ## Pseudorapiditaet: eta = -np.log(np.tan(theta/2.)) #wobei theta der obere Winkel ist
    ### Weitere Interessante Groessen zum selbstcoden:
    #DeltaPhi - Winkel zwischen zwei beliebigen Objekten. Schwierigkeit: Wie stellt man sicher, dass der Winkel DeltaPhi zwischen 0 und 2pi liegt?
    
    ### Jetzt koennen wir auch die transversale Masse bestimmen
    MT = MT_squared**0.5 # Wurzel ziehen geht entweder ueber math.sqrt oder so wie hier, da fuer eine Variable 'a' gilt: sqrt(a) = a^0.5 (und ^ wird mit ** in python ausgedrueckt)
    ### Nun sind wir soweit, dass wir einen Array mit allen transversalen Massen haben. Speichern wir diese Masse als Histogramme ab.
    ### Zuerst speichern wir alle Massen ab - das Histogram unterteilen wir in 100 Abschnitte
    ### hmT enthaelt die Summe fuer jeden Abschnitt, bins die unteren Grenzwert eines jeden Abschnitts
    hmT, mTbins = np.histogram(MT,100,weights=weight)
    ### Falls wir es brauchen sollten, finden wir noch die statistische Unsicherheit:
    hmT_unc = np.sqrt(np.histogram(MT, bins=mTbins, weights = weight**2)[0])
    """
    ### Volle Berechnung
    MT_full = MT_squared_full**0.5 # Wurzel ziehen geht entweder ueber math.sqrt oder so wie hier, da fuer eine Variable 'a' gilt: sqrt(a) = a^0.5 (und ^ wird mit ** in python ausgedrueckt)
    hmTfull, mTbinsfull = np.histogram(MT_full,100,weights=weight)
    hmTfull_unc = np.sqrt(np.histogram(MT_full, bins=mTbinsfull, weights = weight**2)[0])
    """
    ###Machen wir das selbe, aber nur fuer eine geringere Massenauswahl zwischen 30 - 230 GeV/c^2
    hmTnarrow, narrowmTbins = np.histogram(MT,100,range=(30.,232.),weights=weight) #bemerke dass die obere Range 230 + einmal die Abschnittsbreite ist
    hmTnarrow_unc = np.sqrt(np.histogram(MT, bins=narrowmTbins, weights = weight**2)[0])

    ### Nun speichern wir diese Werte komprimiert ab:
    ### Diese Numpy-Funktion speichert die Werte des Histogramms, den statistischen Filter und die Abschnitt-Grenzen in einer komprimierten Textdatei ab. Alternativ kannst du die savetxt fuer die unkomprimierte Text-Datei verwenden.
    # np.savez_compressed(outdir+'hmTfull'+appendname,histo=hmTfull, uncertainty=hmTfull_unc, binning=mTbinsfull)
    np.savez_compressed(outdir+'hmT'+appendname,histo=hmT, uncertainty=hmT_unc, binning=mTbins)
    np.savez_compressed(outdir+'hmTnarrow'+appendname,histo=hmTnarrow, uncertainty=hmTnarrow_unc, binning=narrowmTbins)

    ### Das ist das Ende dieser Funktion. Sie laeuft jetzt drei mal fuer Daten, Signalsimulation und Untergrundsimulation
    


if __name__ == "__main__":

    # Define options
    ### Der Parser erlaubt Inputs beim Aufrufen der Funktion zu verwenden, z.B.
    ### 'python3 AnalyzeData_ZPath.py --process -sv "LieblingsVerzeichnis/"
    parser = argparse.ArgumentParser(description="Inputs for student projects")
    parser.add_argument('-in', '--inputdir', dest='inputdir', help='Directory with the input rootfiles'        , type=str, required=False, default='MakeFlatTrees/OutputTrees/')
    parser.add_argument('-sd', '--savedir', dest='savedir', help='Directory where to store the histogram files', type=str, required=False, default='HistogramData/')

    
    # Argument parser is set up
    args = parser.parse_args()

    # run Main function
    main(args)
