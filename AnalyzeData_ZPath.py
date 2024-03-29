import uproot
import numpy as np
#import pandas as pd
#import uproot3_methods #if you want to use lorentzvectors
import argparse
import os
#from scipy.optimize import curve_fit

### Diese Funktion wird immer aufgerufen
def main(args):
    print("Welcome to the ZPath analysis.")
    ntupledir = os.path.join(args.inputdir,"")
    ### zuerst laden wir die Daten mit uproot
    ### bemerke, der code crashed, falls die drei Dateien nicht existieren
    fileData = uproot.open(ntupledir+"data_2lep.root")["events"]
    fileSignal = uproot.open(ntupledir+"simulation_signal_2lep.root")["events"]
    fileBackground = uproot.open(ntupledir+"simulation_background_2lep.root")["events"]
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
    ### Ereignis muss genau zwei Leptonen haben
    twolep_mask = ((arrays['lep1_E' ] >= 0) & (arrays['lep2_E' ] >= 0) & (arrays['lep3_E'] < 0))
    ### Leptonen muessen mindestens 20 GeV als transversalen Impuls haben
    twolep_pt_mask = (twolep_mask & (np.sqrt(arrays["lep1_px"]**2+arrays["lep1_py"]**2)>20.) & (np.sqrt(arrays["lep2_px"]**2+arrays["lep2_py"]**2)>20.))
    ### Die Leptonen muessen gut im Spurendetektor und Kalorimeter detektierbar sein (eta gibt den Bereich dieser Detektoren an).
    lep1_eta = -np.log(np.tan( np.arccos(arrays["lep1_pz"] / np.sqrt(arrays["lep1_px"]**2+arrays["lep1_py"]**2+arrays["lep1_pz"]**2))/2.))
    lep2_eta = -np.log(np.tan( np.arccos(arrays["lep2_pz"] / np.sqrt(arrays["lep2_px"]**2+arrays["lep2_py"]**2+arrays["lep2_pz"]**2))/2.))
    twolep_eta_mask = (twolep_pt_mask & (((np.abs(arrays['lep1_id'])==13) & (np.abs(lep1_eta)<2.5)) | ((np.abs(arrays['lep1_id'])==11) & ((np.abs(lep1_eta)<2.5) & ((np.abs(lep1_eta)<1.52) | (np.abs(lep1_eta)<1.37))))) & (((np.abs(arrays['lep2_id'])==13) & (np.abs(lep2_eta)<2.5)) | ((np.abs(arrays['lep2_id'])==11) & ((np.abs(lep2_eta)<2.5) & ((np.abs(lep2_eta)<1.52) | (np.abs(lep2_eta)<1.37))))))
    ### Die zwei Leptonen muessen vom gleichen Typ sein (same flavor), aber auch ihre Antiteilchen (opposite sign), d.h. entweder 11*-11 == -121 oder 13*-13 == -169
    SFOS_mask = (twolep_eta_mask & ((arrays['lep1_id']*arrays['lep2_id']==-121) | (arrays['lep1_id']*arrays['lep2_id']==-169)))
    ### Wir moechten nun alle Ereignisse herausfiltern, welche diese Bedingungen nicht erfuellen --> invert
    filters = np.invert(SFOS_mask)
    ### Erzeuge gefilterte Objekte - fuer das Z-Boson interessieren uns nur Lepton 1, 2 und der weights-array, wir koennen aber auch met mitnehmen
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

    ### Nun produzieren wir arrays fuer das Z boson
    Z_E  = lep1_E  + lep2_E
    Z_px = lep1_px + lep2_px
    Z_py = lep1_py + lep2_py
    Z_pz = lep1_pz + lep2_pz

    ### this is the mass-squared for Z-bosons: (mc^2)^2 = (lep1_E + lep2_E)^2 - [ ((lep1_px+lep2_px)c)^2 + ((lep1_py+lep2_py)c)^2 + ((lep1_pz+lep2_pz)c)^2 ]
    Z_mass_squared = (Z_E**2 - (Z_px**2 + Z_py**2 + Z_pz**2))
    ### Redefiniere Filter:
    filters = Z_mass_squared < 0 # es gibt pathologische Faelle, bei der diese Groesse negativ wird. Falls das passiert, koennen wir nicht die Wurzel ziehen.

    ### Filtere die pathologischen Faelle
    lep1_px = np.delete(lep1_px,filters)
    lep1_py = np.delete(lep1_py,filters)
    lep1_pz = np.delete(lep1_pz,filters)
    lep1_E  = np.delete(lep1_E ,filters)
    lep1_id = np.delete(lep1_id,filters)
    lep2_px = np.delete(lep2_px,filters)
    lep2_py = np.delete(lep2_py,filters)
    lep2_pz = np.delete(lep2_pz,filters)
    lep2_E  = np.delete(lep2_E ,filters)
    lep2_id = np.delete(lep2_id,filters)
    met_px = np.delete(met_px,filters)
    met_py = np.delete(met_py,filters)
    weight = np.delete(weight,filters)
    Z_E  = np.delete(Z_E ,filters)
    Z_px = np.delete(Z_px,filters)
    Z_py = np.delete(Z_py,filters)
    Z_pz = np.delete(Z_pz,filters)
    Z_mass_squared = np.delete(Z_mass_squared,filters)
    ### interessanten Groessen sind:
    ## transversale Impulse: pT = np.sqrt(px**2 + py**2)
    ## Winkel phi (in Ebene senkrecht zum Protonstrahl): phi = np.arctan2(py,px)
    ## Winkel theta (Winkel bezueglich Protonstrahl): theta = np.arccos(pz / np.sqrt(px**2 + py**2 + pz**2))
    ## Pseudorapiditaet: eta = -np.log(np.tan(theta/2.)) #wobei theta der obere Winkel ist
    ## Masse: m = np.sqrt((E**2 - (px**2 + py**2 + pz**2)))
    ### Weitere Interessante Groessen zum selbstcoden:
    #DeltaPhi - Winkel zwischen zwei beliebigen Objekten. Schwierigkeit: Wie stellt man sicher, dass der Winkel DeltaPhi zwischen 0 und 2pi liegt?
    #DeltaR = np.sqrt(DeltaPhi**2 + DeltaEta**2)
    
    ### Jetzt koennen wir auch die Z-Masse bestimmen
    Z_m = Z_mass_squared**0.5 # Wurzel ziehen geht entweder ueber math.sqrt oder so wie hier, da fuer eine Variable 'a' gilt: sqrt(a) = a^0.5 (und ^ wird mit ** in python ausgedrueckt)
    ### Nun sind wir soweit, dass wir einen Array mit allen Massen haben, die von Elektronen-Positronen- oder Muon-Antimuon-Paaren kommen und daher von Z-Bosonen kommen. Speichern wir diese Masse als Histogramme ab.
    ### Zuerst speichern wir alle Massen ab - das Histogram unterteilen wir in 100 Abschnitte
    ### hmll enthaelt die Summe fuer jeden Abschnitt, bins die unteren Grenzwert eines jeden Abschnitts
    hmll, mllbins = np.histogram(Z_m,100,weights=weight)
    ### Falls wir es brauchen sollten, finden wir noch die statistische Unsicherheit:
    hmll_unc = np.sqrt(np.histogram(Z_m, bins=mllbins, weights = weight**2)[0])

    ###Machen wir das selbe, aber nur fuer eine geringere Massenauswahl zwischen 40 - 140 GeV/c^2
    hmllnarrow, narrowmllbins = np.histogram(Z_m,100,range=(40.,141.),weights=weight) #bemerke dass die obere Range 140 + einmal die Abschnittsbreite ist
    hmllnarrow_unc = np.sqrt(np.histogram(Z_m, bins=narrowmllbins, weights = weight**2)[0])

    ### Nun speichern wir diese Werte komprimiert ab:
    ### Diese Numpy-Funktion speichert die Werte des Histogramms, den statistischen Filter und die Abschnitt-Grenzen in einer komprimierten Textdatei ab. Alternativ kannst du die savetxt fuer die unkomprimierte Text-Datei verwenden.
    np.savez_compressed(outdir+'hmll'+appendname,histo=hmll, uncertainty=hmll_unc, binning=mllbins)
    np.savez_compressed(outdir+'hmllnarrow'+appendname,histo=hmllnarrow, uncertainty=hmllnarrow_unc, binning=narrowmllbins)

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
