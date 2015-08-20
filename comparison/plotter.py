#!/bin/env python

from DukePlotALot import *
from DukePlotALot2D import *
from plotlib import HistStorage,getColorList,getDictValue,HistStorageContainer
import matplotlib.pyplot as plt
from configobj import ConfigObj
try:
    from collections import OrderedDict
except ImportError:
    from ordered import OrderedDict

from rootpy.plotting.views import ScaleView
from rootpy.io import root_open
from rootpy.plotting import Graph

import style_class as sc

from object_plotting import *

from lheanalyzer import *

import ROOT as r

mili = 1e-3
femto = 1e-15
piko = 1e-12

dim_match = {
 '1':0,
 '4':1,
 '5':2,
 '6':3
}

def readin_calchep():
    out_vector = []
    file_object = open('info_xsec_QBH.txt', 'r')
    lines = file_object.readlines()
    dim = 0
    mass_vector = []
    for line in lines:
        if line == '\n': continue
        if 'Mth' in line: continue
        objects = line.split('\t')
        if '' in objects:
            objects.remove('')
        if 'QBH_' in objects[0]:
            out_vector.append(mass_vector)
            mass_vector = []
            dim = int(objects[0].split('_')[1].replace('n',''))
            continue
        if dim == 0: continue
        mass_vector.append([int(objects[0]),float(objects[1])*femto/piko,1.0])
    out_vector.append(mass_vector)
    out_vector.remove([])
    file_object.close()
    return out_vector

def readin_qbh():
    out_vector = []
    file_object = open('info.txt', 'r')
    lines = file_object.readlines()
    dim = 0
    mass_vector = []
    for line in lines:
        objects = line.split('\t')
        if objects[0] != dim:
            out_vector.append(mass_vector)
            mass_vector = []
            dim = objects[0]
        mass_vector.append([int(objects[1]),float(objects[3])*mili/piko,float(objects[5])])
    out_vector.append(mass_vector)
    out_vector.remove([])
    file_object.close()
    return out_vector

def make_xs_plot():
    ####################################################################
    # Individual cross section plots
    ####################################################################

    print("Now plotting: cross section comparison")

    calchep_list = readin_calchep()
    qbh_list = readin_qbh()

    x_vals_1 =[]
    y_vals_qbh_1 = []
    y_vals_chp_1 = []

    for itemc,itemq in zip(calchep_list[dim_match['1']],qbh_list[dim_match['1']]):
        x_vals_1.append(itemc[0])
        y_vals_qbh_1.append(itemq[1]*itemq[2])
        y_vals_chp_1.append(itemc[1]*itemc[2])

    # x_vals_2 =[]
    # y_vals_qbh_2 = []
    # y_vals_chp_2 = []
# 
    # for itemc,itemq in zip(calchep_list[dim_match['2']],qbh_list[dim_match['2']]):
        # x_vals_2.append(itemc[0])
        # y_vals_qbh_2.append(itemq[1]*itemq[2])
        # y_vals_chp_2.append(itemc[1]*itemc[2])

    x_vals_4 =[]
    y_vals_qbh_4 = []
    y_vals_chp_4 = []

    for itemc,itemq in zip(calchep_list[dim_match['4']],qbh_list[dim_match['4']]):
        x_vals_4.append(itemc[0])
        y_vals_qbh_4.append(itemq[1]*itemq[2])
        y_vals_chp_4.append(itemc[1]*itemc[2])

    x_vals_5 =[]
    y_vals_qbh_5 = []
    y_vals_chp_5 = []

    for itemc,itemq in zip(calchep_list[dim_match['5']],qbh_list[dim_match['5']]):
        x_vals_5.append(itemc[0])
        y_vals_qbh_5.append(itemq[1]*itemq[2])
        y_vals_chp_5.append(itemc[1]*itemc[2])

    x_vals_6 =[]
    y_vals_qbh_6 = []
    y_vals_chp_6 = []

    for itemc,itemq in zip(calchep_list[dim_match['6']],qbh_list[dim_match['6']]):
        x_vals_6.append(itemc[0])
        y_vals_qbh_6.append(itemq[1]*itemq[2])
        y_vals_chp_6.append(itemc[1]*itemc[2])

    x_vals_1 = np.array(x_vals_1)
    y_vals_qbh_1 = np.array(y_vals_qbh_1)
    y_vals_chp_1 = np.array(y_vals_chp_1)

    # x_vals_2 = np.array(x_vals_2)
    # y_vals_qbh_2 = np.array(y_vals_qbh_2)
    # y_vals_chp_2 = np.array(y_vals_chp_2)

    x_vals_4 = np.array(x_vals_4)
    y_vals_qbh_4 = np.array(y_vals_qbh_4)
    y_vals_chp_4 = np.array(y_vals_chp_4)

    x_vals_5 = np.array(x_vals_5)
    y_vals_qbh_5 = np.array(y_vals_qbh_5)
    y_vals_chp_5 = np.array(y_vals_chp_5)

    x_vals_6 = np.array(x_vals_6)
    y_vals_qbh_6 = np.array(y_vals_qbh_6)
    y_vals_chp_6 = np.array(y_vals_chp_6)

    graph_qbh_1 = Graph(x_vals_1.shape[0])
    graph_chp_1 = Graph(x_vals_1.shape[0])
    for i, (xx, y1, y2) in enumerate(zip(x_vals_1, y_vals_qbh_1, y_vals_chp_1)):
        graph_qbh_1.SetPoint(i, xx, y1)
        graph_qbh_1.SetPointError(i, 0, 0, 0, 0)
        graph_chp_1.SetPoint(i, xx, y2)
        graph_chp_1.SetPointError(i, 0, 0, 0, 0)

    # graph_qbh_2 = Graph(x_vals_2.shape[0])
    # graph_chp_2 = Graph(x_vals_2.shape[0])
    # for i, (xx, y1, y2) in enumerate(zip(x_vals_2, y_vals_qbh_2, y_vals_chp_2)):
        # graph_qbh_2.SetPoint(i, xx, y1)
        # graph_qbh_2.SetPointError(i, 0, 0, 0, 0)
        # graph_chp_2.SetPoint(i, xx, y2)
        # graph_chp_2.SetPointError(i, 0, 0, 0, 0)

    graph_qbh_4 = Graph(x_vals_4.shape[0])
    graph_chp_4 = Graph(x_vals_4.shape[0])
    for i, (xx, y1, y2) in enumerate(zip(x_vals_4, y_vals_qbh_4, y_vals_chp_4)):
        graph_qbh_4.SetPoint(i, xx, y1)
        graph_qbh_4.SetPointError(i, 0, 0, 0, 0)
        graph_chp_4.SetPoint(i, xx, y2)
        graph_chp_4.SetPointError(i, 0, 0, 0, 0)

    graph_qbh_5 = Graph(x_vals_5.shape[0])
    graph_chp_5 = Graph(x_vals_5.shape[0])
    for i, (xx, y1, y2) in enumerate(zip(x_vals_5, y_vals_qbh_5, y_vals_chp_5)):
        graph_qbh_5.SetPoint(i, xx, y1)
        graph_qbh_5.SetPointError(i, 0, 0, 0, 0)
        graph_chp_5.SetPoint(i, xx, y2)
        graph_chp_5.SetPointError(i, 0, 0, 0, 0)

    graph_qbh_6 = Graph(x_vals_6.shape[0])
    graph_chp_6 = Graph(x_vals_6.shape[0])
    for i, (xx, y1, y2) in enumerate(zip(x_vals_6, y_vals_qbh_6, y_vals_chp_6)):
        graph_qbh_6.SetPoint(i, xx, y1)
        graph_qbh_6.SetPointError(i, 0, 0, 0, 0)
        graph_chp_6.SetPoint(i, xx, y2)
        graph_chp_6.SetPointError(i, 0, 0, 0, 0)

    graph_qbh_1.SetTitle('n = 1, QBH')
    graph_qbh_1.xaxis.SetTitle('$M$ (GeV)')
    graph_qbh_1.yaxis.SetTitle('xs $\cdot$ BR (pb)')

    graph_chp_1.SetTitle('n = 1, CalcHEP')
    graph_chp_1.xaxis.SetTitle('$M$ (GeV)')
    graph_chp_1.yaxis.SetTitle('xs $\cdot$ BR (pb)')

    graph_qbh_1.SetLineColor('red')
    graph_chp_1.SetLineColor('red')
    graph_chp_1.SetLineStyle(2)

    # graph_qbh_2.SetTitle('n = 2, QBH')
    # graph_qbh_2.xaxis.SetTitle('$M$ (GeV)')
    # graph_qbh_2.yaxis.SetTitle('xs $\cdot$ BR (pb)')
# 
    # graph_chp_2.SetTitle('n = 2, CalcHEP')
    # graph_chp_2.xaxis.SetTitle('$M$ (GeV)')
    # graph_chp_2.yaxis.SetTitle('xs $\cdot$ BR (pb)')

    # graph_qbh_2.SetLineColor('blue')
    # graph_chp_2.SetLineColor('blue')
    # graph_chp_2.SetLineStyle(2)

    graph_qbh_4.SetTitle('n = 4, QBH')
    graph_qbh_4.xaxis.SetTitle('$M$ (GeV)')
    graph_qbh_4.yaxis.SetTitle('xs $\cdot$ BR (pb)')

    graph_chp_4.SetTitle('n = 4, CalcHEP')
    graph_chp_4.xaxis.SetTitle('$M$ (GeV)')
    graph_chp_4.yaxis.SetTitle('xs $\cdot$ BR (pb)')

    graph_qbh_4.SetLineColor('green')
    graph_chp_4.SetLineColor('green')
    graph_chp_4.SetLineStyle(2)

    graph_qbh_5.SetTitle('n = 5, QBH')
    graph_qbh_5.xaxis.SetTitle('$M$ (GeV)')
    graph_qbh_5.yaxis.SetTitle('xs $\cdot$ BR (pb)')

    graph_chp_5.SetTitle('n = 5, CalcHEP')
    graph_chp_5.xaxis.SetTitle('$M$ (GeV)')
    graph_chp_5.yaxis.SetTitle('xs $\cdot$ BR (pb)')

    graph_qbh_5.SetLineColor('black')
    graph_chp_5.SetLineColor('black')
    graph_chp_5.SetLineStyle(2)

    graph_qbh_6.SetTitle('n = 6, QBH')
    graph_qbh_6.xaxis.SetTitle('$M$ (GeV)')
    graph_qbh_6.yaxis.SetTitle('xs $\cdot$ BR (pb)')

    graph_chp_6.SetTitle('n = 6, CalcHEP')
    graph_chp_6.xaxis.SetTitle('$M$ (GeV)')
    graph_chp_6.yaxis.SetTitle('xs $\cdot$ BR (pb)')

    graph_qbh_6.SetLineColor('magenta')
    graph_chp_6.SetLineColor('magenta')
    graph_chp_6.SetLineStyle(2)

    hist_style = sc.style_container(style = 'CMS', useRoot = False, kind = 'Linegraphs', cmsPositon = "upper right", legendPosition = 'lower left', lumi = 0, cms = 13)

    hist_style.Set_additional_text('Simulation')
 
    # hist_style.Set_axis(logy = True, grid = True, xmin = 200, xmax = 2000, histaxis_ymin = 1.0, histaxis_ymax = 1.5)

    test = plotter(hist = [graph_qbh_1, graph_chp_1,graph_qbh_4, graph_chp_4,graph_qbh_5, graph_chp_5,graph_qbh_6, graph_chp_6], style=hist_style)

    # test = plotter(hist = [graph_qbh_1, graph_chp_1], style=hist_style)


    test.create_plot()

    test.SavePlot('xs_comparison.pdf')

def create_histos(filename):
    lhe_file = LHEAnalysis(filename)
    print('analyzing file %s'%filename)
    for item in lhe_file.processes:
        print('process:')
        print(item.id)
        print('cross section:')
        print(str(item.crossSection) + ' +- ' + str(item.crossSectionUncertainty))
    print(' ')

    ele_hist_pT = Hist(3000, 0, 6000, name = 'ele_hist_pT')
    ele_hist_phi = Hist(65, -3.5, 3.5, name = 'ele_hist_phi')
    ele_hist_eta = Hist(100, -5, 5, name = 'ele_hist_eta')

    muo_hist_pT = Hist(3000, 0, 6000, name = 'muo_hist_pT')
    muo_hist_phi = Hist(65, -3.5, 3.5, name = 'muo_hist_phi')
    muo_hist_eta = Hist(100, -5, 5, name = 'muo_hist_eta')

    emu_hist_mass = Hist(3000, 0, 6000, name = 'emu_hist_mass')

    while(True):
        try:
            event = lhe_file.next()
        except(StopIteration):
            break

        electron = r.TLorentzVector()
        muon = r.TLorentzVector()
        qbh = r.TLorentzVector()
        for part in event.particles:
            if(abs(part.pdgId) == 11):
                ele_hist_pT.Fill(part.pt)
                ele_hist_phi.Fill(part.phi)
                ele_hist_eta.Fill(part.eta)
                electron.SetPtEtaPhiM(part.pt,part.phi,part.eta,part.mass)

            if(abs(part.pdgId) == 13):
                muo_hist_pT.Fill(part.pt)
                muo_hist_phi.Fill(part.phi)
                muo_hist_eta.Fill(part.eta)
                muon.SetPtEtaPhiM(part.pt,part.phi,part.eta,part.mass)

        qbh = electron + muon
        emu_hist_mass.Fill(qbh.M())

    ele_hist_pT.Scale(1./ele_hist_pT.Integral())
    ele_hist_phi.Scale(1./ele_hist_phi.Integral())
    ele_hist_eta.Scale(1./ele_hist_eta.Integral())

    muo_hist_pT.Scale(1./muo_hist_pT.Integral())
    muo_hist_phi.Scale(1./muo_hist_phi.Integral())
    muo_hist_eta.Scale(1./muo_hist_eta.Integral())

    emu_hist_mass.Scale(1./emu_hist_mass.Integral())

    ele_hist_pT = Graph(ele_hist_pT)
    ele_hist_phi = Graph(ele_hist_phi)
    ele_hist_eta = Graph(ele_hist_eta)

    muo_hist_pT = Graph(muo_hist_pT)
    muo_hist_phi = Graph(muo_hist_phi)
    muo_hist_eta = Graph(muo_hist_eta)

    emu_hist_mass = Graph(emu_hist_mass)

    return [ele_hist_pT,ele_hist_phi,ele_hist_eta,muo_hist_pT,muo_hist_phi,muo_hist_eta,emu_hist_mass]

def plot_shape_comparison(n, mass):

    if n == 1:
        chp_1_500 = create_histos('/net/scratch_cms/institut_3a/13TeV_rpv_LFV_resonances/QBH_emu/CalcHEP_n_%i_RS/QBH_n%i_RS_Mth-MPL%i.lhe'%(n, n, mass))
        qbh_1_500 = create_histos('/disk1/erdweg/QBH/lhes/LHEFQBH_n%i_RS_%i.lhe'%(n, mass))
    else:
        chp_1_500 = create_histos('/net/scratch_cms/institut_3a/13TeV_rpv_LFV_resonances/QBH_emu/CalcHEP_n_%i_PDG/QBH_n%i_ADD_Mth-MPL%i.lhe'%(n, n, mass))
        qbh_1_500 = create_histos('/disk1/erdweg/QBH/lhes/LHEFQBH_n%i_ADD_%i.lhe'%(n, mass))

    hists = [[0,'ele_pT'], [1,'ele_phi'], [2,'ele_eta'], [3,'muo_pT'], [4,'muo_phi'], [5,'muo_eta'], [6,'emu_mass']]

    for item in hists:
        hist_style = sc.style_container(style = 'CMS', useRoot = False, kind = 'Linegraphs', cmsPositon = "upper right", legendPosition = 'lower left', lumi = 0, cms = 13)

        hist_style.Set_additional_text('Simulation')
    
        # hist_style.Set_axis(logy = True, grid = True, xmin = 200, xmax = 2000, histaxis_ymin = 1.0, histaxis_ymax = 1.5)

        chp_1_500[item[0]].SetLineColor('red')
        chp_1_500[item[0]].SetTitle('CalcHEP, n = %i, M = %i'%(n, mass))
        qbh_1_500[item[0]].SetLineColor('green')
        qbh_1_500[item[0]].SetTitle('QBH, n = %i, M = %i'%(n, mass))

        test = plotter(hist = [chp_1_500[item[0]], qbh_1_500[item[0]]], style=hist_style)

        test.create_plot()

        test.SavePlot(item[1] + '_%i_%i_comparison.pdf'%(n, mass))

def main():

    make_xs_plot()
    # plot_shape_comparison(1,500)
    # plot_shape_comparison(1,1000)
    # plot_shape_comparison(1,1500)
    # plot_shape_comparison(1,2000)
    # plot_shape_comparison(1,2500)
    # plot_shape_comparison(1,3000)
    # plot_shape_comparison(1,3500)
    # plot_shape_comparison(1,4000)

    # plot_shape_comparison(4,500)
    # plot_shape_comparison(4,1000)
    # plot_shape_comparison(4,1500)
    # plot_shape_comparison(4,2000)
    # plot_shape_comparison(4,2500)
    # plot_shape_comparison(4,3000)
    # plot_shape_comparison(4,3500)
    # plot_shape_comparison(4,4000)

    # plot_shape_comparison(5,500)
    # plot_shape_comparison(5,1000)
    # plot_shape_comparison(5,1500)
    # plot_shape_comparison(5,2000)
    # plot_shape_comparison(5,2500)
    # plot_shape_comparison(5,3000)
    # plot_shape_comparison(5,3500)
    # plot_shape_comparison(5,4000)

    # plot_shape_comparison(6,500)
    # plot_shape_comparison(6,1000)
    # plot_shape_comparison(6,1500)
    # plot_shape_comparison(6,2000)
    # plot_shape_comparison(6,2500)
    # plot_shape_comparison(6,3000)
    # plot_shape_comparison(6,3500)
    # plot_shape_comparison(6,4000)

    return 42



main()
