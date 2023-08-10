import uproot
import numpy as np
#import pandas as pd
#import uproot3_methods #if you want to use lorentzvectors
import argparse
import os
#from scipy.optimize import curve_fit

### Diese Funktion wird immer aufgerufen
def main(args):
    print("Welcome to the example analysis.")
    print("This analysis has no distributions of the H/W/Z bosons.")
    print("Thus this allows you to do all the analysis coding itself.")
    ntupledir = os.path.join(args.inputdir,"")
    ### zuerst laden wir die Daten mit uproot
    ### bemerke, der code crashed, falls die drei Dateien nicht existieren
    fileData = uproot.open(ntupledir+"data_2lep.root")["events"]
    fileSignal = uproot.open(ntupledir+"simulation_signal_2lep.root")["events"]
    fileBackground = uproot.open(ntupledir+"simulation_background_2lep.root")["events"]
    print("Loading files from " + ntupledir)
    print("In this example we work with two lepton data.")
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
    ### Bevor wir Daten analysieren, wollen wir eine Vorauswahl treffen.
    ### Dies koennte zum Beispiel zur Ladung der Leptonen sein, ihrer Energie, oder in welchem Bereich im Detektor sie sein sollen.
    ### Hier ein Beispiel, bei dem wir sagen: Wir wollen zwei Leptonen (e+, e-, mu+ oder mu-) haben, deren transversaler Impuls 30 bzw. 20 GeV sein soll, und mindestens ein Lepton soll ein Elektronen oder Positronen sein.
    ### ... Das ist moeglicherweise nicht, was du machen willst, aber wir zeigen dir hier die Code-Struktur.
    twolep_mask = ((arrays['lep1_E' ] >= 0) & (arrays['lep2_E' ] >= 0) & (arrays['lep3_E'] < 0))
    ### Leptonen muessen mindestens 30 GeV / 20 GeV als transversalen Impuls haben. Da beide Leptonen zwingend das erfuellen sollen, verwenden wir das UND "&"
    ### Nebenbemerkung: Leptonen sind gemaess ihres transversalen Impuls geordnet. Daher muss man hier nicht den Fall testen, lep1_pt > 20 & lep2_pt > 30
    ### Was wir hier machen ist, wir wollen zwei Leptonen (twolep_mask) und zusaetzlich die Lepton-pTs testen
    lep_pt_mask = (twolep_mask & (np.sqrt(arrays["lep1_px"]**2+arrays["lep1_py"]**2)>30.) & (np.sqrt(arrays["lep2_px"]**2+arrays["lep2_py"]**2)>20.)))
    ### Ein Lepton soll entweder Elektron oder Positron sein. Daher brauchen wir hier ein ODER "|"
    lep_id_mask = (lep_pt_mask & ((np.abs(arrays['lep1_id'])==11) | (np.abs(arrays['lep2_id'])==11) ) )
    ### Wir moechten nun alle Ereignisse herausfiltern, welche diese Bedingungen nicht erfuellen --> invert
    filters = np.invert(lep_id_mask)
    ### Erzeuge gefilterte Objekte - Da wir keine 3 oder 4 Leptonen haben, koennen wir die lep3_* und lep4_* arrays ignorieren
    lep1_px = np.delete(arrays['lep1_px'],filters)
    lep1_py = np.delete(arrays['lep1_py'],filters)
    lep1_pz = np.delete(arrays['lep1_pz'],filters)
    lep1_E  = np.delete(arrays['lep1_E' ],filters)
    lep1_id = np.delete(arrays['lep1_id'],filters)
    lep2_px = np.delete(arrays['lep2_px'],filters)
    lep2_py = np.delete(arrays['lep2_py'],filters)
    lep2_pz = np.delete(arrays['lep2_pz'],filters)
    lep2_E  = np.delete(arrays['lep2_E' ],filters)
    lep2_id = np.delete(arrays['lep2_id'],filters)
    met_px = np.delete(arrays['met_px'],filters)
    met_py = np.delete(arrays['met_py'],filters)
    weight = np.delete(arrays['weight'],filters)

    ### Nun koennen wir alles moegliche berechnen:
    ### interessanten Groessen sind:
    ## transversale Impulse: pT = np.sqrt(px**2 + py**2)
    ## Winkel phi (in Ebene senkrecht zum Protonstrahl): phi = np.arctan2(py,px)
    ## Winkel theta (Winkel bezueglich Protonstrahl): theta = np.arccos(pz / np.sqrt(px**2 + py**2 + pz**2))
    ## Pseudorapiditaet: eta = -np.log(np.tan(theta/2.)) #wobei theta der obere Winkel ist
    ## Masse: m = np.sqrt((E**2 - (px**2 + py**2 + pz**2)))
    ### Weitere Interessante Groessen zum selbstcoden:
    #DeltaPhi - Winkel zwischen zwei beliebigen Objekten. Schwierigkeit: Wie stellt man sicher, dass der Winkel DeltaPhi zwischen 0 und 2pi liegt?
    #DeltaR = np.sqrt(DeltaPhi**2 + DeltaEta**2)

    ### Fuer dieses Beispiel berechne ich pTmiss:
    pTmiss = np.sqrt(met_px**2 + met_py**2)

    ### Damit die Analyse auch Sinn macht, muessen wir die analysierten Daten auch speichern und darstellen.
    ### Der Darstellungscode ist MakePlot.py, also speichern wir hier nur die Daten ab. Dies tun wir als Histogramm.

    ### Unser Histogramm heisst hpTmiss_all - alle Ereignisse, welche die Vorselektion erfuellen werden aufgefuehrt.
    ### Unser Histogramm teilt pTmiss vom kleinsten vorkommenden Wert zum groessten vorkommenden Wert in 100 Abschnitte ein und speichert, wie viele Ereignisse pro Abschnitt in den Daten gefunden wurden. Wir speichern die Abschnitt-Definition in pTmissbins_all ab.
    ### weights bedeutet, dass die Simulation so gewichtet wird, dass sie der Erwartung der Daten entsprechen sollte.
    ### Die zweite Zeile speichert die statistischte Unsicherheit ab.
    hpTmiss_all, pTmissbins_all = np.histogram(pTmiss,100,weights=weight)
    hpTmiss_all_unc = np.sqrt(np.histogram(pTmiss, bins=pTmissbins_all, weights = weight**2)[0])

    ### Wir koennen auch dem Histogramm sagen, welcher Bereich uns Interessiert. Hier z.B. sagen wir, dass wir 20 Abschnitte zwischen 0 und 100 haben wollen
    hpTmiss_sel, pTmissbins_sel = np.histogram(pTmiss,100,range=(0.,105.),weights=weight) #bemerke dass die obere Range 100 + einmal die Abschnittsbreite ist
    hpTmiss_sel_unc = np.sqrt(np.histogram(pTmiss, bins=pTmissbins_sel, weights = weight**2)[0])

    ### Nun speichern wir diese Werte komprimiert ab:
    ### Diese Numpy-Funktion speichert die Werte des Histogramms, den statistischen Filter und die Abschnitt-Grenzen in einer komprimierten Textdatei ab. Alternativ kannst du die savetxt fuer die unkomprimierte Text-Datei verwenden.
    np.savez_compressed(outdir+'hpTmiss_all'+appendname,histo=hpTmiss_all, uncertainty=hpTmiss_all_unc, binning=pTmissbins_all)
    np.savez_compressed(outdir+'hpTmiss_sel'+appendname,histo=hpTmiss_sel, uncertainty=hpTmiss_sel_unc, binning=pTmissbins_sel)

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
