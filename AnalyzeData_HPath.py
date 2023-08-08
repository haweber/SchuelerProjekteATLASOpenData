import uproot
import numpy as np
#import pandas as pd
#import uproot3_methods #if you want to use lorentzvectors
import argparse
import os
#from scipy.optimize import curve_fit

### Diese Funktion wird immer aufgerufen
def main(args):
    print("Welcome to the HPath analysis.")
    ntupledir = os.path.join(args.inputdir,"")
    ### zuerst laden wir die Daten mit uproot
    ### bemerke, der code crashed, falls die drei Dateien nicht existieren
    fileData = uproot.open(ntupledir+"data_4lep.root")["events"]
    fileSignal = uproot.open(ntupledir+"simulation_signal_4lep.root")["events"]
    fileBackground = uproot.open(ntupledir+"simulation_background_4lep.root")["events"]
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
    ### Ereignis muss mindestens vier Leptonen haben
    fourlep_mask = ((arrays['lep1_E' ] >= 0) & (arrays['lep2_E' ] >= 0) & (arrays['lep3_E'] > 0) & (arrays['lep4_E'] > 0))
    ### Leptonen muessen mindestens 25/15/10/7 GeV als transversalen Impuls haben
    fourlep_pt_mask = (fourlep_mask & (np.sqrt(arrays["lep1_px"]**2+arrays["lep1_py"]**2)>25.) & (np.sqrt(arrays["lep2_px"]**2+arrays["lep2_py"]**2)>15.) & (np.sqrt(arrays["lep3_px"]**2+arrays["lep3_py"]**2)>10.) & (np.sqrt(arrays["lep4_px"]**2+arrays["lep4_py"]**2)>7.))
    ### Die Leptonen muessen gut im Spurendetektor und Kalorimeter detektierbar sein (eta gibt den Bereich dieser Detektoren an).
    lep1_eta = -np.log(np.tan( np.arccos(arrays["lep1_pz"] / np.sqrt(arrays["lep1_px"]**2+arrays["lep1_py"]**2+arrays["lep1_pz"]**2))/2.))
    lep2_eta = -np.log(np.tan( np.arccos(arrays["lep2_pz"] / np.sqrt(arrays["lep2_px"]**2+arrays["lep2_py"]**2+arrays["lep2_pz"]**2))/2.))
    lep3_eta = -np.log(np.tan( np.arccos(arrays["lep3_pz"] / np.sqrt(arrays["lep3_px"]**2+arrays["lep3_py"]**2+arrays["lep3_pz"]**2))/2.))
    lep4_eta = -np.log(np.tan( np.arccos(arrays["lep4_pz"] / np.sqrt(arrays["lep4_px"]**2+arrays["lep4_py"]**2+arrays["lep4_pz"]**2))/2.))
    lep1_eta_mask = (fourlep_pt_mask & (((np.abs(arrays['lep1_id'])==13) & (np.abs(lep1_eta)<2.5)) | ((np.abs(arrays['lep1_id'])==11) & ((np.abs(lep1_eta)<2.5) & ((np.abs(lep1_eta)<1.52) | (np.abs(lep1_eta)<1.37))))) )
    lep2_eta_mask = (fourlep_pt_mask & (((np.abs(arrays['lep2_id'])==13) & (np.abs(lep2_eta)<2.5)) | ((np.abs(arrays['lep2_id'])==11) & ((np.abs(lep2_eta)<2.5) & ((np.abs(lep2_eta)<1.52) | (np.abs(lep2_eta)<1.37))))) )
    lep3_eta_mask = (fourlep_pt_mask & (((np.abs(arrays['lep3_id'])==13) & (np.abs(lep3_eta)<2.5)) | ((np.abs(arrays['lep3_id'])==11) & ((np.abs(lep3_eta)<2.5) & ((np.abs(lep3_eta)<1.52) | (np.abs(lep3_eta)<1.37))))) )
    lep4_eta_mask = (fourlep_pt_mask & (((np.abs(arrays['lep4_id'])==13) & (np.abs(lep4_eta)<2.5)) | ((np.abs(arrays['lep4_id'])==11) & ((np.abs(lep4_eta)<2.5) & ((np.abs(lep4_eta)<1.52) | (np.abs(lep4_eta)<1.37))))) )
    fourlep_eta_mask = (lep1_eta_mask & lep2_eta_mask & lep3_eta_mask & lep4_eta_mask)
    ### Die zwei Leptonen muessen vom gleichen Typ sein (same flavor), aber auch ihre Antiteilchen (opposite sign), d.h. entweder 11*-11 == -121 oder 13*-13 == -169. Wir suchen zwei solche Paare
    SFOS_12_34_mask = (fourlep_eta_mask & ((arrays['lep1_id']*arrays['lep2_id']==-121) | (arrays['lep1_id']*arrays['lep2_id']==-169)) & ((arrays['lep3_id']*arrays['lep4_id']==-121) | (arrays['lep3_id']*arrays['lep4_id']==-169)))
    SFOS_13_24_mask = (fourlep_eta_mask & ((arrays['lep1_id']*arrays['lep3_id']==-121) | (arrays['lep1_id']*arrays['lep3_id']==-169)) & ((arrays['lep2_id']*arrays['lep4_id']==-121) | (arrays['lep2_id']*arrays['lep4_id']==-169)))
    SFOS_14_23_mask = (fourlep_eta_mask & ((arrays['lep1_id']*arrays['lep4_id']==-121) | (arrays['lep1_id']*arrays['lep4_id']==-169)) & ((arrays['lep2_id']*arrays['lep3_id']==-121) | (arrays['lep2_id']*arrays['lep3_id']==-169)))
    ### Eine der drei Moeglichkeiten oben sollte richtig sein.
    SFOS_mask = (SFOS_12_34_mask | SFOS_13_24_mask | SFOS_14_23_mask)
    ### Wir moechten nun alle Ereignisse herausfiltern, welche diese Bedingungen nicht erfuellen --> invert
    filters = np.invert(SFOS_mask)
    ### Erzeuge gefilterte Objekte - wir sortieren allerdings erst
    """
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
    lep3_px = np.delete(arrays['lep3_px'],filters)
    lep3_py = np.delete(arrays['lep3_py'],filters)
    lep3_pz = np.delete(arrays['lep3_pz'],filters)
    lep3_E  = np.delete(arrays['lep3_E' ],filters)
    lep3_id = np.delete(arrays['lep3_id'],filters)
    lep4_px = np.delete(arrays['lep4_px'],filters)
    lep4_py = np.delete(arrays['lep4_py'],filters)
    lep4_pz = np.delete(arrays['lep4_pz'],filters)
    lep4_E  = np.delete(arrays['lep4_E' ],filters)
    lep4_id = np.delete(arrays['lep4_id'],filters)
    met_px = np.delete(arrays['met_px'],filters)
    met_py = np.delete(arrays['met_py'],filters)
    weight = np.delete(arrays['weight'],filters)
    """
    ### Nun sortieren wir die Leptonen nach SFOS Paaren: l1-l2 bildet ein SFOS-Paar, l2-l3 bildet das zweite SFOS-Paar
    ### Streng genommen brauchen wir diese Sortierung nicht, aber eventuell ist es hilfreich fuer Folgestudien. Du kannst diesen Teil bis zum Filtern ueberspringen
    l1_px = arrays['lep1_px']
    l1_py = arrays['lep1_py']
    l1_pz = arrays['lep1_pz']
    l1_E  = arrays['lep1_E']
    l1_id = arrays['lep1_id']
    #lep2 falls SFOS_12_34 wahr, sonst lep3 falls SFOS_13_24 wahr, sonst lep4 falls SFOS_14_23 wahr, sonst lep2
    l2_px = np.where(SFOS_12_34_mask, arrays['lep2_px'], np.where(SFOS_13_24_mask, arrays['lep3_px'], np.where(SFOS_14_23_mask, arrays['lep4_px'], arrays['lep2_px']))) 
    l2_py = np.where(SFOS_12_34_mask, arrays['lep2_py'], np.where(SFOS_13_24_mask, arrays['lep3_py'], np.where(SFOS_14_23_mask, arrays['lep4_py'], arrays['lep2_py']))) 
    l2_pz = np.where(SFOS_12_34_mask, arrays['lep2_pz'], np.where(SFOS_13_24_mask, arrays['lep3_pz'], np.where(SFOS_14_23_mask, arrays['lep4_pz'], arrays['lep2_pz']))) 
    l2_E  = np.where(SFOS_12_34_mask, arrays['lep2_E'] , np.where(SFOS_13_24_mask, arrays['lep3_E'] , np.where(SFOS_14_23_mask, arrays['lep4_E'] , arrays['lep2_E'] ))) 
    l2_id = np.where(SFOS_12_34_mask, arrays['lep2_id'], np.where(SFOS_13_24_mask, arrays['lep3_id'], np.where(SFOS_14_23_mask, arrays['lep4_id'], arrays['lep2_id']))) 
    #lep3 falls SFOS_12_34 wahr, sonst lep2 falls SFOS_13_24 wahr, sonst lep2 falls SFOS_14_23 wahr, sonst lep3
    l3_px = np.where(SFOS_12_34_mask, arrays['lep3_px'], np.where(SFOS_13_24_mask, arrays['lep2_px'], np.where(SFOS_14_23_mask, arrays['lep2_px'], arrays['lep3_px']))) 
    l3_py = np.where(SFOS_12_34_mask, arrays['lep3_py'], np.where(SFOS_13_24_mask, arrays['lep2_py'], np.where(SFOS_14_23_mask, arrays['lep2_py'], arrays['lep3_py']))) 
    l3_pz = np.where(SFOS_12_34_mask, arrays['lep3_pz'], np.where(SFOS_13_24_mask, arrays['lep2_pz'], np.where(SFOS_14_23_mask, arrays['lep2_pz'], arrays['lep3_pz']))) 
    l3_E  = np.where(SFOS_12_34_mask, arrays['lep3_E'] , np.where(SFOS_13_24_mask, arrays['lep2_E'] , np.where(SFOS_14_23_mask, arrays['lep2_E'] , arrays['lep3_E'] ))) 
    l3_id = np.where(SFOS_12_34_mask, arrays['lep3_id'], np.where(SFOS_13_24_mask, arrays['lep2_id'], np.where(SFOS_14_23_mask, arrays['lep2_id'], arrays['lep3_id']))) 
    #lep4 falls SFOS_12_34 wahr, sonst lep4 falls SFOS_13_24 wahr, sonst lep3 falls SFOS_14_23 wahr, sonst lep4
    l4_px = np.where(SFOS_12_34_mask, arrays['lep4_px'], np.where(SFOS_13_24_mask, arrays['lep4_px'], np.where(SFOS_14_23_mask, arrays['lep3_px'], arrays['lep4_px']))) 
    l4_py = np.where(SFOS_12_34_mask, arrays['lep4_py'], np.where(SFOS_13_24_mask, arrays['lep4_py'], np.where(SFOS_14_23_mask, arrays['lep3_py'], arrays['lep4_py']))) 
    l4_pz = np.where(SFOS_12_34_mask, arrays['lep4_pz'], np.where(SFOS_13_24_mask, arrays['lep4_pz'], np.where(SFOS_14_23_mask, arrays['lep3_pz'], arrays['lep4_pz']))) 
    l4_E  = np.where(SFOS_12_34_mask, arrays['lep4_E'] , np.where(SFOS_13_24_mask, arrays['lep4_E'] , np.where(SFOS_14_23_mask, arrays['lep3_E'] , arrays['lep4_E'] ))) 
    l4_id = np.where(SFOS_12_34_mask, arrays['lep4_id'], np.where(SFOS_13_24_mask, arrays['lep4_id'], np.where(SFOS_14_23_mask, arrays['lep3_id'], arrays['lep4_id'])))
    ### Nun wollen wir noch, dass l1-l2 das SFOS-Paar ist, dass am naechsten zur Z-Masse kommt.
    l1l2_mass_squared = (l1_E+l2_E)**2-((l1_px+l2_px)**2+(l1_py+l2_py)**2+(l1_pz+l2_pz)**2)
    l3l4_mass_squared = (l3_E+l4_E)**2-((l3_px+l4_px)**2+(l3_py+l4_py)**2+(l3_pz+l4_pz)**2)
    mZ_squared_pdg = 91.1876**2
    l1l2iscloser = ((np.abs(l1l2_mass_squared - mZ_squared_pdg)) < (np.abs(l3l4_mass_squared - mZ_squared_pdg)))
    lep1_px = np.where(l1l2iscloser, l1_px, l3_px)
    lep1_py = np.where(l1l2iscloser, l1_py, l3_py)
    lep1_pz = np.where(l1l2iscloser, l1_pz, l3_pz)
    lep1_E  = np.where(l1l2iscloser, l1_E , l3_E )
    lep1_id = np.where(l1l2iscloser, l1_id, l3_id)
    lep2_px = np.where(l1l2iscloser, l2_px, l4_px)
    lep2_py = np.where(l1l2iscloser, l2_py, l4_py)
    lep2_pz = np.where(l1l2iscloser, l2_pz, l4_pz)
    lep2_E  = np.where(l1l2iscloser, l2_E , l4_E )
    lep2_id = np.where(l1l2iscloser, l2_id, l4_id)
    lep3_px = np.where(l1l2iscloser, l3_px, l1_px)
    lep3_py = np.where(l1l2iscloser, l3_py, l1_py)
    lep3_pz = np.where(l1l2iscloser, l3_pz, l1_pz)
    lep3_E  = np.where(l1l2iscloser, l3_E , l1_E )
    lep3_id = np.where(l1l2iscloser, l3_id, l1_id)
    lep4_px = np.where(l1l2iscloser, l4_px, l2_px)
    lep4_py = np.where(l1l2iscloser, l4_py, l2_py)
    lep4_pz = np.where(l1l2iscloser, l4_pz, l2_pz)
    lep4_E  = np.where(l1l2iscloser, l4_E , l2_E )
    lep4_id = np.where(l1l2iscloser, l4_id, l2_id)
    ### Jetzt filtern wir die sortierten arrays
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
    lep3_px = np.delete(lep3_px,filters)
    lep3_py = np.delete(lep3_py,filters)
    lep3_pz = np.delete(lep3_pz,filters)
    lep3_E  = np.delete(lep3_E ,filters)
    lep3_id = np.delete(lep3_id,filters)
    lep4_px = np.delete(lep4_px,filters)
    lep4_py = np.delete(lep4_py,filters)
    lep4_pz = np.delete(lep4_pz,filters)
    lep4_E  = np.delete(lep4_E ,filters)
    lep4_id = np.delete(lep4_id,filters)
    met_px = np.delete(arrays['met_px'],filters)
    met_py = np.delete(arrays['met_py'],filters)
    weight = np.delete(arrays['weight'],filters)
    
    ### Nun produzieren wir arrays fuer das H boson
    H_E  = lep1_E  + lep2_E  + lep3_E  + lep4_E
    H_px = lep1_px + lep2_px + lep3_px + lep4_px
    H_py = lep1_py + lep2_py + lep3_py + lep4_py
    H_pz = lep1_pz + lep2_pz + lep3_pz + lep4_pz

    ### this is the mass-squared for Z-bosons: (mc^2)^2 = (lep1_E + lep2_E)^2 - [ ((lep1_px+lep2_px)c)^2 + ((lep1_py+lep2_py)c)^2 + ((lep1_pz+lep2_pz)c)^2 ] - Analog gilt das fuer das Higgs-Boson, aber mit vier Teilchen
    H_mass_squared = (H_E**2 - (H_px**2 + H_py**2 + H_pz**2))
    ### Redefiniere Filter:
    filters = H_mass_squared < 0 # es gibt pathologische Faelle, bei der diese Groesse negativ wird. Falls das passiert, koennen wir nicht die Wurzel ziehen.

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
    lep3_px = np.delete(lep3_px,filters)
    lep3_py = np.delete(lep3_py,filters)
    lep3_pz = np.delete(lep3_pz,filters)
    lep3_E  = np.delete(lep3_E ,filters)
    lep3_id = np.delete(lep3_id,filters)
    lep4_px = np.delete(lep4_px,filters)
    lep4_py = np.delete(lep4_py,filters)
    lep4_pz = np.delete(lep4_pz,filters)
    lep4_E  = np.delete(lep4_E ,filters)
    lep4_id = np.delete(lep4_id,filters)
    met_px = np.delete(met_px,filters)
    met_py = np.delete(met_py,filters)
    weight = np.delete(weight,filters)
    H_E  = np.delete(H_E ,filters)
    H_px = np.delete(H_px,filters)
    H_py = np.delete(H_py,filters)
    H_pz = np.delete(H_pz,filters)
    H_mass_squared = np.delete(H_mass_squared,filters)
    ### interessanten Groessen sind:
    ## transversale Impulse: pT = np.sqrt(px**2 + py**2)
    ## Winkel phi (in Ebene senkrecht zum Protonstrahl): phi = np.arctan2(py,px)
    ## Winkel theta (Winkel bezueglich Protonstrahl): theta = np.arccos(pz / np.sqrt(px**2 + py**2 + pz**2))
    ## Pseudorapiditaet: eta = -np.log(np.tan(theta/2.)) #wobei theta der obere Winkel ist
    ## Masse: m = np.sqrt((E**2 - (px**2 + py**2 + pz**2))), beispielsweise von den beiden Zwei-Lepton-Paare l1l2 oder l3l4
    ### Weitere Interessante Groessen zum selbstcoden:
    #DeltaPhi - Winkel zwischen zwei beliebigen Objekten. Schwierigkeit: Wie stellt man sicher, dass der Winkel DeltaPhi zwischen 0 und 2pi liegt?
    #DeltaR = np.sqrt(DeltaPhi**2 + DeltaEta**2) - entweder zwischen Leptonen innerhalb eines Paares, oder zwischen den beiden Paaren
        
    ### Jetzt koennen wir auch die Z-Masse bestimmen
    H_m = H_mass_squared**0.5 # Wurzel ziehen geht entweder ueber math.sqrt oder so wie hier, da fuer eine Variable 'a' gilt: sqrt(a) = a^0.5 (und ^ wird mit ** in python ausgedrueckt)
    ### Nun sind wir soweit, dass wir einen Array mit allen Massen haben, die von Elektronen-Positronen- oder Muon-Antimuon-Paaren kommen und daher von Z-Bosonen kommen. Speichern wir diese Masse als Histogramme ab.
    ### Zuerst speichern wir alle Massen ab - das Histogram unterteilen wir in 100 Abschnitte
    ### hmll enthaelt die Summe fuer jeden Abschnitt, bins die unteren Grenzwert eines jeden Abschnitts
    hmllll, mllllbins = np.histogram(H_m,25,weights=weight)
    ### Falls wir es brauchen sollten, finden wir noch die statistische Unsicherheit:
    hmllll_unc = np.sqrt(np.histogram(H_m, bins=mllllbins, weights = weight**2)[0])

    ###Machen wir das selbe, aber nur fuer eine geringere Massenauswahl zwischen 40 - 140 GeV/c^2
    hmllllnarrow, narrowmllllbins = np.histogram(H_m,20,range=(70.,175.),weights=weight) #bemerke dass die obere Range 140 + einmal die Abschnittsbreite ist
    hmllllnarrow_unc = np.sqrt(np.histogram(H_m, bins=narrowmllllbins, weights = weight**2)[0])

    ### Nun speichern wir diese Werte komprimiert ab:
    ### Diese Numpy-Funktion speichert die Werte des Histogramms, den statistischen Filter und die Abschnitt-Grenzen in einer komprimierten Textdatei ab. Alternativ kannst du die savetxt fuer die unkomprimierte Text-Datei verwenden.
    np.savez_compressed(outdir+'hmllll'+appendname,histo=hmllll, uncertainty=hmllll_unc, binning=mllllbins)
    np.savez_compressed(outdir+'hmllllnarrow'+appendname,histo=hmllllnarrow, uncertainty=hmllllnarrow_unc, binning=narrowmllllbins)

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
