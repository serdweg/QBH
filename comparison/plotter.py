#!/bin/env python

import copy

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

def add_qbh_gg(in_vector):
    out_vector = copy.deepcopy(in_vector)
    file_object = open('info_gg.txt', 'r')
    lines = file_object.readlines()
    dim = '0'
    count_mass = 0
    for line in lines:
        objects = line.split('\t')
        if objects[0] != dim:
            dim = objects[0]
            count_mass = 0
        if (not out_vector[dim_match[str(dim)]][count_mass][0] == int(objects[1])):
            print('masses don\'t match. help!')
            print('qq mass: %i\tgg mass: %i'%(out_vector[dim_match[str(dim)]][count_mass][0],int(objects[1])))
            continue
        out_vector[dim_match[str(dim)]][count_mass][1] = out_vector[dim_match[str(dim)]][count_mass][1] * out_vector[dim_match[str(dim)]][count_mass][2] + float(objects[3])*mili/piko * float(objects[5])
        out_vector[dim_match[str(dim)]][count_mass][2] = 1.
        count_mass += 1
    file_object.close()
    return out_vector

def make_xs_plot():
    ####################################################################
    # Individual cross section plots
    ####################################################################

    print("Now plotting: cross section comparison")

    calchep_list = readin_calchep()
    qbh_list = readin_qbh()
    qbh_gg_list = add_qbh_gg(qbh_list)

    x_vals_1 =[]
    y_vals_qbh_1 = []
    y_vals_chp_1 = []
    y_vals_qbh_gg_1 = []

    for itemc,itemq,itemg in zip(calchep_list[dim_match['1']],qbh_list[dim_match['1']],qbh_gg_list[dim_match['1']]):
        x_vals_1.append(itemc[0])
        y_vals_qbh_1.append(itemq[1]*itemq[2])
        y_vals_chp_1.append(itemc[1]*itemc[2])
        y_vals_qbh_gg_1.append(itemg[1]*itemg[2])

    x_vals_4 =[]
    y_vals_qbh_4 = []
    y_vals_chp_4 = []
    y_vals_qbh_gg_4 = []

    for itemc,itemq,itemg in zip(calchep_list[dim_match['4']],qbh_list[dim_match['4']],qbh_gg_list[dim_match['4']]):
        x_vals_4.append(itemc[0])
        y_vals_qbh_4.append(itemq[1]*itemq[2])
        y_vals_chp_4.append(itemc[1]*itemc[2])
        y_vals_qbh_gg_4.append(itemg[1]*itemg[2])

    x_vals_5 =[]
    y_vals_qbh_5 = []
    y_vals_chp_5 = []
    y_vals_qbh_gg_5 = []

    for itemc,itemq,itemg in zip(calchep_list[dim_match['5']],qbh_list[dim_match['5']],qbh_gg_list[dim_match['5']]):
        x_vals_5.append(itemc[0])
        y_vals_qbh_5.append(itemq[1]*itemq[2])
        y_vals_chp_5.append(itemc[1]*itemc[2])
        y_vals_qbh_gg_5.append(itemg[1]*itemg[2])

    x_vals_6 =[]
    y_vals_qbh_6 = []
    y_vals_chp_6 = []
    y_vals_qbh_gg_6 = []

    for itemc,itemq,itemg in zip(calchep_list[dim_match['6']],qbh_list[dim_match['6']],qbh_gg_list[dim_match['6']]):
        x_vals_6.append(itemc[0])
        y_vals_qbh_6.append(itemq[1]*itemq[2])
        y_vals_chp_6.append(itemc[1]*itemc[2])
        y_vals_qbh_gg_6.append(itemg[1]*itemg[2])

    x_vals_1 = np.array(x_vals_1)
    y_vals_qbh_1 = np.array(y_vals_qbh_1)
    y_vals_chp_1 = np.array(y_vals_chp_1)
    y_vals_qbh_gg_1 = np.array(y_vals_qbh_gg_1)

    x_vals_4 = np.array(x_vals_4)
    y_vals_qbh_4 = np.array(y_vals_qbh_4)
    y_vals_chp_4 = np.array(y_vals_chp_4)
    y_vals_qbh_gg_4 = np.array(y_vals_qbh_gg_4)

    x_vals_5 = np.array(x_vals_5)
    y_vals_qbh_5 = np.array(y_vals_qbh_5)
    y_vals_chp_5 = np.array(y_vals_chp_5)
    y_vals_qbh_gg_5 = np.array(y_vals_qbh_gg_5)

    x_vals_6 = np.array(x_vals_6)
    y_vals_qbh_6 = np.array(y_vals_qbh_6)
    y_vals_chp_6 = np.array(y_vals_chp_6)
    y_vals_qbh_gg_6 = np.array(y_vals_qbh_gg_6)

    graph_qbh_1 = Graph(x_vals_1.shape[0])
    graph_chp_1 = Graph(x_vals_1.shape[0])
    graph_qbh_gg_1 = Graph(x_vals_1.shape[0])
    graph_ratio_1 = Graph(x_vals_1.shape[0])
    graph_ratio_gg_1 = Graph(x_vals_1.shape[0])
    for i, (xx, y1, y2, y3) in enumerate(zip(x_vals_1, y_vals_qbh_1, y_vals_chp_1, y_vals_qbh_gg_1)):
        graph_qbh_1.SetPoint(i, xx, y1)
        graph_qbh_1.SetPointError(i, 0, 0, 0, 0)
        graph_chp_1.SetPoint(i, xx, y2)
        graph_chp_1.SetPointError(i, 0, 0, 0, 0)
        graph_qbh_gg_1.SetPoint(i, xx, y3)
        graph_qbh_gg_1.SetPointError(i, 0, 0, 0, 0)
        graph_ratio_1.SetPoint(i, xx, y2/y1)
        graph_ratio_1.SetPointError(i, 0, 0, 0, 0)
        graph_ratio_gg_1.SetPoint(i, xx, y2/y3)
        graph_ratio_gg_1.SetPointError(i, 0, 0, 0, 0)

    graph_qbh_4 = Graph(x_vals_4.shape[0])
    graph_chp_4 = Graph(x_vals_4.shape[0])
    graph_qbh_gg_4 = Graph(x_vals_4.shape[0])
    graph_ratio_4 = Graph(x_vals_4.shape[0])
    graph_ratio_gg_4 = Graph(x_vals_4.shape[0])
    for i, (xx, y1, y2, y3) in enumerate(zip(x_vals_4, y_vals_qbh_4, y_vals_chp_4, y_vals_qbh_gg_4)):
        graph_qbh_4.SetPoint(i, xx, y1)
        graph_qbh_4.SetPointError(i, 0, 0, 0, 0)
        graph_chp_4.SetPoint(i, xx, y2)
        graph_chp_4.SetPointError(i, 0, 0, 0, 0)
        graph_qbh_gg_4.SetPoint(i, xx, y3)
        graph_qbh_gg_4.SetPointError(i, 0, 0, 0, 0)
        graph_ratio_4.SetPoint(i, xx, y2/y1)
        graph_ratio_4.SetPointError(i, 0, 0, 0, 0)
        graph_ratio_gg_4.SetPoint(i, xx, y2/y3)
        graph_ratio_gg_4.SetPointError(i, 0, 0, 0, 0)

    graph_qbh_5 = Graph(x_vals_5.shape[0])
    graph_chp_5 = Graph(x_vals_5.shape[0])
    graph_qbh_gg_5 = Graph(x_vals_5.shape[0])
    graph_ratio_5 = Graph(x_vals_5.shape[0])
    graph_ratio_gg_5 = Graph(x_vals_5.shape[0])
    for i, (xx, y1, y2, y3) in enumerate(zip(x_vals_5, y_vals_qbh_5, y_vals_chp_5, y_vals_qbh_gg_5)):
        graph_qbh_5.SetPoint(i, xx, y1)
        graph_qbh_5.SetPointError(i, 0, 0, 0, 0)
        graph_chp_5.SetPoint(i, xx, y2)
        graph_chp_5.SetPointError(i, 0, 0, 0, 0)
        graph_qbh_gg_5.SetPoint(i, xx, y3)
        graph_qbh_gg_5.SetPointError(i, 0, 0, 0, 0)
        graph_ratio_5.SetPoint(i, xx, y2/y1)
        graph_ratio_5.SetPointError(i, 0, 0, 0, 0)
        graph_ratio_gg_5.SetPoint(i, xx, y2/y3)
        graph_ratio_gg_5.SetPointError(i, 0, 0, 0, 0)

    graph_qbh_6 = Graph(x_vals_6.shape[0])
    graph_chp_6 = Graph(x_vals_6.shape[0])
    graph_qbh_gg_6 = Graph(x_vals_6.shape[0])
    graph_ratio_6 = Graph(x_vals_6.shape[0])
    graph_ratio_gg_6 = Graph(x_vals_6.shape[0])
    for i, (xx, y1, y2, y3) in enumerate(zip(x_vals_6, y_vals_qbh_6, y_vals_chp_6, y_vals_qbh_gg_6)):
        graph_qbh_6.SetPoint(i, xx, y1)
        graph_qbh_6.SetPointError(i, 0, 0, 0, 0)
        graph_chp_6.SetPoint(i, xx, y2)
        graph_chp_6.SetPointError(i, 0, 0, 0, 0)
        graph_qbh_gg_6.SetPoint(i, xx, y3)
        graph_qbh_gg_6.SetPointError(i, 0, 0, 0, 0)
        graph_ratio_6.SetPoint(i, xx, y2/y1)
        graph_ratio_6.SetPointError(i, 0, 0, 0, 0)
        graph_ratio_gg_6.SetPoint(i, xx, y2/y3)
        graph_ratio_gg_6.SetPointError(i, 0, 0, 0, 0)

    graph_qbh_1.SetTitle('n = 1, QBH')
    graph_qbh_1.xaxis.SetTitle('$M$ (GeV)')
    graph_qbh_1.yaxis.SetTitle('xs $\cdot$ BR (pb)')

    graph_chp_1.SetTitle('n = 1, CalcHEP')
    graph_chp_1.xaxis.SetTitle('$M$ (GeV)')
    graph_chp_1.yaxis.SetTitle('xs $\cdot$ BR (pb)')

    graph_qbh_gg_1.SetTitle('n = 1, QBH(+gg)')
    graph_qbh_gg_1.xaxis.SetTitle('$M$ (GeV)')
    graph_qbh_gg_1.yaxis.SetTitle('xs $\cdot$ BR (pb)')

    graph_qbh_1.SetLineColor('red')
    graph_chp_1.SetLineColor('red')
    graph_qbh_gg_1.SetLineColor('red')
    graph_ratio_1.SetLineColor('red')
    graph_ratio_gg_1.SetLineColor('red')
    graph_qbh_1.SetLineStyle(2)
    graph_ratio_1.SetLineStyle(2)
    graph_qbh_gg_1.SetLineStyle(3)
    graph_ratio_gg_1.SetLineStyle(3)

    graph_qbh_4.SetTitle('n = 4, QBH')
    graph_qbh_4.xaxis.SetTitle('$M$ (GeV)')
    graph_qbh_4.yaxis.SetTitle('xs $\cdot$ BR (pb)')

    graph_chp_4.SetTitle('n = 4, CalcHEP')
    graph_chp_4.xaxis.SetTitle('$M$ (GeV)')
    graph_chp_4.yaxis.SetTitle('xs $\cdot$ BR (pb)')

    graph_qbh_gg_4.SetTitle('n = 4, QBH(+gg)')
    graph_qbh_gg_4.xaxis.SetTitle('$M$ (GeV)')
    graph_qbh_gg_4.yaxis.SetTitle('xs $\cdot$ BR (pb)')

    graph_qbh_4.SetLineColor('green')
    graph_chp_4.SetLineColor('green')
    graph_qbh_gg_4.SetLineColor('green')
    graph_ratio_4.SetLineColor('green')
    graph_ratio_gg_4.SetLineColor('green')
    graph_qbh_4.SetLineStyle(2)
    graph_qbh_gg_4.SetLineStyle(3)
    graph_ratio_4.SetLineStyle(2)
    graph_ratio_gg_4.SetLineStyle(3)

    graph_qbh_5.SetTitle('n = 5, QBH')
    graph_qbh_5.xaxis.SetTitle('$M$ (GeV)')
    graph_qbh_5.yaxis.SetTitle('xs $\cdot$ BR (pb)')

    graph_chp_5.SetTitle('n = 5, CalcHEP')
    graph_chp_5.xaxis.SetTitle('$M$ (GeV)')
    graph_chp_5.yaxis.SetTitle('xs $\cdot$ BR (pb)')

    graph_qbh_gg_5.SetTitle('n = 5, QBH(+gg)')
    graph_qbh_gg_5.xaxis.SetTitle('$M$ (GeV)')
    graph_qbh_gg_5.yaxis.SetTitle('xs $\cdot$ BR (pb)')

    graph_qbh_5.SetLineColor('black')
    graph_chp_5.SetLineColor('black')
    graph_qbh_gg_5.SetLineColor('black')
    graph_ratio_5.SetLineColor('black')
    graph_ratio_gg_5.SetLineColor('black')
    graph_qbh_5.SetLineStyle(2)
    graph_qbh_gg_5.SetLineStyle(3)
    graph_ratio_5.SetLineStyle(2)
    graph_ratio_gg_5.SetLineStyle(3)

    graph_qbh_6.SetTitle('n = 6, QBH')
    graph_qbh_6.xaxis.SetTitle('$M$ (GeV)')
    graph_qbh_6.yaxis.SetTitle('xs $\cdot$ BR (pb)')

    graph_chp_6.SetTitle('n = 6, CalcHEP')
    graph_chp_6.xaxis.SetTitle('$M$ (GeV)')
    graph_chp_6.yaxis.SetTitle('xs $\cdot$ BR (pb)')

    graph_qbh_gg_6.SetTitle('n = 6, QBH(+gg)')
    graph_qbh_gg_6.xaxis.SetTitle('$M$ (GeV)')
    graph_qbh_gg_6.yaxis.SetTitle('xs $\cdot$ BR (pb)')

    graph_qbh_6.SetLineColor('magenta')
    graph_chp_6.SetLineColor('magenta')
    graph_qbh_gg_6.SetLineColor('magenta')
    graph_ratio_6.SetLineColor('magenta')
    graph_ratio_gg_6.SetLineColor('magenta')
    graph_qbh_6.SetLineStyle(2)
    graph_qbh_gg_6.SetLineStyle(3)
    graph_ratio_6.SetLineStyle(2)
    graph_ratio_gg_6.SetLineStyle(3)

    hist_style = sc.style_container(style = 'CMS', useRoot = False, kind = 'Linegraphs', cmsPositon = "upper left", legendPosition = 'upper right', lumi = 0, cms = 13)
    hist_style.Set_n_legend_collumns(2)

    hist_style.Set_additional_text('Simulation')
 

    test = plotter(hist = [graph_qbh_1, graph_chp_1, graph_qbh_gg_1,graph_qbh_4, graph_chp_4, graph_qbh_gg_4,graph_qbh_5, graph_chp_5, graph_qbh_gg_5,graph_qbh_6, graph_chp_6, graph_qbh_gg_6], style=hist_style)

    # test = plotter(hist = [graph_qbh_1, graph_chp_1], style=hist_style)

    test.Add_plot('Empty',pos=1, height=25, label='CalcHEP/QBH')

    test.create_plot()

    test.Get_axis1().set_ylim(ymin = 1.6e-8, ymax = 1e5)

    x,y=[],[]
    for i in graph_ratio_1:
        x.append( i[0])
        y.append( i[1])
    test.Get_axis2().plot(x,y,'o-', markeredgewidth=0,
    color=graph_ratio_1.GetLineColor(),
    linestyle = convert_linestyle(graph_ratio_1.GetLineStyle(), 'mpl'),
    markersize = hist_style.Get_marker_size(),
    marker = hist_style.Get_marker_style())

    x,y=[],[]
    for i in graph_ratio_gg_1:
        x.append( i[0])
        y.append( i[1])
    test.Get_axis2().plot(x,y,'o-', markeredgewidth=0,
    color=graph_ratio_gg_1.GetLineColor(),
    linestyle = convert_linestyle(graph_ratio_gg_1.GetLineStyle(), 'mpl'),
    markersize = hist_style.Get_marker_size(),
    marker = hist_style.Get_marker_style())

    x,y=[],[]
    for i in graph_ratio_4:
        x.append( i[0])
        y.append( i[1])
    test.Get_axis2().plot(x,y,'o-', markeredgewidth=0,
    color=graph_ratio_4.GetLineColor(),
    linestyle = convert_linestyle(graph_ratio_4.GetLineStyle(), 'mpl'),
    markersize = hist_style.Get_marker_size(),
    marker = hist_style.Get_marker_style())

    x,y=[],[]
    for i in graph_ratio_gg_4:
        x.append( i[0])
        y.append( i[1])
    test.Get_axis2().plot(x,y,'o-', markeredgewidth=0,
    color=graph_ratio_gg_4.GetLineColor(),
    linestyle = convert_linestyle(graph_ratio_gg_4.GetLineStyle(), 'mpl'),
    markersize = hist_style.Get_marker_size(),
    marker = hist_style.Get_marker_style())

    x,y=[],[]
    for i in graph_ratio_5:
        x.append( i[0])
        y.append( i[1])
    test.Get_axis2().plot(x,y,'o-', markeredgewidth=0,
    color=graph_ratio_5.GetLineColor(),
    linestyle = convert_linestyle(graph_ratio_5.GetLineStyle(), 'mpl'),
    markersize = hist_style.Get_marker_size(),
    marker = hist_style.Get_marker_style())

    x,y=[],[]
    for i in graph_ratio_gg_5:
        x.append( i[0])
        y.append( i[1])
    test.Get_axis2().plot(x,y,'o-', markeredgewidth=0,
    color=graph_ratio_gg_5.GetLineColor(),
    linestyle = convert_linestyle(graph_ratio_gg_5.GetLineStyle(), 'mpl'),
    markersize = hist_style.Get_marker_size(),
    marker = hist_style.Get_marker_style())

    x,y=[],[]
    for i in graph_ratio_6:
        x.append( i[0])
        y.append( i[1])
    test.Get_axis2().plot(x,y,'o-', markeredgewidth=0,
    color=graph_ratio_6.GetLineColor(),
    linestyle = convert_linestyle(graph_ratio_6.GetLineStyle(), 'mpl'),
    markersize = hist_style.Get_marker_size(),
    marker = hist_style.Get_marker_style())

    x,y=[],[]
    for i in graph_ratio_gg_1:
        x.append( i[0])
        y.append( i[1])
    test.Get_axis2().plot(x,y,'o-', markeredgewidth=0,
    color=graph_ratio_gg_1.GetLineColor(),
    linestyle = convert_linestyle(graph_ratio_gg_1.GetLineStyle(), 'mpl'),
    markersize = hist_style.Get_marker_size(),
    marker = hist_style.Get_marker_style())

    test.Get_axis2().set_ylim(ymin = 0.6, ymax = 1.6)

    test.SavePlot('xs_comparison.pdf')

def create_histos(filename, gg = False):
    lhe_file = LHEAnalysis(filename)
    print('analyzing file %s'%filename)
    for item in lhe_file.processes:
        print('process:')
        print(item.id)
        print('cross section:')
        print(str(item.crossSection) + ' +- ' + str(item.crossSectionUncertainty))
    print(' ')

    ele_hist_pT = Hist(300, 0, 6000, name = 'ele_hist_pT')
    ele_hist_phi = Hist(65, -3.5, 3.5, name = 'ele_hist_phi')
    ele_hist_eta = Hist(100, -5, 5, name = 'ele_hist_eta')

    muo_hist_pT = Hist(300, 0, 6000, name = 'muo_hist_pT')
    muo_hist_phi = Hist(65, -3.5, 3.5, name = 'muo_hist_phi')
    muo_hist_eta = Hist(100, -5, 5, name = 'muo_hist_eta')

    emu_hist_mass = Hist(300, 0, 6000, name = 'emu_hist_mass')

    while(True):
        try:
            event = lhe_file.next()
        except(StopIteration):
            break
        if gg:
            count_gluon = 0
            for part in event.particles:
                if(abs(part.pdgId) == 21):
                    count_gluon += 1
            # if count_gluon < 2:
                # continue
        electron = r.TLorentzVector()
        muon = r.TLorentzVector()
        qbh = r.TLorentzVector()
        for part in event.particles:
            if(abs(part.pdgId) == 11):
                ele_hist_pT.Fill(part.pt)
                ele_hist_phi.Fill(part.phi)
                ele_hist_eta.Fill(part.eta)
                electron.SetPtEtaPhiM(part.pt,part.eta,part.phi,part.mass)

            if(abs(part.pdgId) == 13):
                muo_hist_pT.Fill(part.pt)
                muo_hist_phi.Fill(part.phi)
                muo_hist_eta.Fill(part.eta)
                muon.SetPtEtaPhiM(part.pt,part.eta,part.phi,part.mass)

        qbh = electron + muon
        emu_hist_mass.Fill(qbh.M())

    ele_hist_pT.Scale(1./ele_hist_pT.Integral())
    ele_hist_phi.Scale(1./ele_hist_phi.Integral())
    ele_hist_eta.Scale(1./ele_hist_eta.Integral())

    muo_hist_pT.Scale(1./muo_hist_pT.Integral())
    muo_hist_phi.Scale(1./muo_hist_phi.Integral())
    muo_hist_eta.Scale(1./muo_hist_eta.Integral())

    emu_hist_mass.Scale(1./emu_hist_mass.Integral())

    # ele_hist_pT = Graph(ele_hist_pT)
    # ele_hist_phi = Graph(ele_hist_phi)
    # ele_hist_eta = Graph(ele_hist_eta)

    # muo_hist_pT = Graph(muo_hist_pT)
    # muo_hist_phi = Graph(muo_hist_phi)
    # muo_hist_eta = Graph(muo_hist_eta)

    # emu_hist_mass = Graph(emu_hist_mass)

    return [ele_hist_pT,ele_hist_phi,ele_hist_eta,muo_hist_pT,muo_hist_phi,muo_hist_eta,emu_hist_mass]

def plot_shape_comparison(n, mass, gg = False):
    add_txt = ''
    if gg:
        add_txt = 'gg_'
    if n == 1:
        chp_1_500 = create_histos('/net/scratch_cms/institut_3a/13TeV_rpv_LFV_resonances/QBH_emu/CalcHEP_n_%i_RS/QBH_n%i_RS_Mth-MPL%i.lhe'%(n, n, mass), gg)
        qbh_1_500 = create_histos('/disk1/erdweg/QBH/lhes/LHEFQBH_n%i_RS_%s%i.lhe'%(n, add_txt, mass), gg)
    else:
        chp_1_500 = create_histos('/net/scratch_cms/institut_3a/13TeV_rpv_LFV_resonances/QBH_emu/CalcHEP_n_%i_PDG/QBH_n%i_ADD_Mth-MPL%i.lhe'%(n, n, mass), gg)
        qbh_1_500 = create_histos('/disk1/erdweg/QBH/lhes/LHEFQBH_n%i_ADD_%s%i.lhe'%(n, add_txt, mass), gg)

    hists = [[0,'ele_pT','$p_{T}^{ele}$ (GeV)'],
             [1,'ele_phi','$\phi_{ele}$ (GeV)'],
             [2,'ele_eta','$\eta_{ele}$ (GeV)'],
             [3,'muo_pT','$p_{T}^{muo}$ (GeV)'],
             [4,'muo_phi','$\phi_{muo}$ (GeV)'],
             [5,'muo_eta','$\eta_{muo}$ (GeV)'],
             [6,'emu_mass','$M_{ele,muo}$ (GeV)']]

    for item in hists:
        hist_style = sc.style_container(style = 'CMS', useRoot = False, kind = 'Linegraphs', cmsPositon = "upper right", legendPosition = 'lower left', lumi = 0, cms = 13)

        hist_style.Set_additional_text('Simulation')
    
        # hist_style.Set_axis(logy = True, grid = True, xmin = 200, xmax = 2000, histaxis_ymin = 1.0, histaxis_ymax = 1.5)

        ratio = chp_1_500[item[0]].Clone('ratio')
        ratio.Divide(qbh_1_500[item[0]])

        dummy_chp = Graph(chp_1_500[item[0]])
        dummy_qbh = Graph(qbh_1_500[item[0]])

        dummy_chp.SetLineColor('red')
        dummy_chp.SetTitle('CalcHEP, n = %i, M = %i'%(n, mass))
        dummy_chp.xaxis.SetTitle('%s'%(item[2]))
        dummy_qbh.SetLineColor('green')
        dummy_qbh.SetTitle('QBH, n = %i, M = %i'%(n, mass))
        dummy_qbh.xaxis.SetTitle('%s'%(item[2]))

        test = plotter(hist = [dummy_chp, dummy_qbh], style=hist_style)

        test.Add_plot('Empty',pos=1, height=15, label='CalcHEP/QBH')

        test.create_plot()

        duke_errorbar(ratio, xerr = hist_style.Get_xerr(), emptybins = False, axes = test.Get_axis2(),
                      markersize = hist_style.Get_marker_size(),
                      marker = hist_style.Get_marker_style(),
                      ecolor = hist_style.Get_marker_color(),
                      markerfacecolor = hist_style.Get_marker_color(),
                      markeredgecolor = hist_style.Get_marker_color(),
                      capthick = hist_style.Get_marker_error_cap_width(),
                      zorder = 2.2)

        test.Get_axis2().set_ylim(ymin = 0, ymax = 2)

        test.SavePlot(item[1] + '_%i_%i_comparison.pdf'%(n, mass))

def main():

    make_xs_plot()
    plot_shape_comparison(1,500, True)
    plot_shape_comparison(1,1000, False)
    # plot_shape_comparison(1,1500, False)
    # plot_shape_comparison(1,2000)
    # plot_shape_comparison(1,2500)
    # plot_shape_comparison(1,3000)
    # plot_shape_comparison(1,3500)
    # plot_shape_comparison(1,4000)

    # plot_shape_comparison(4,500)
    # plot_shape_comparison(4,1000)
    # plot_shape_comparison(4,1500)
    # plot_shape_comparison(4,2000)
    plot_shape_comparison(4,2500, False)
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
