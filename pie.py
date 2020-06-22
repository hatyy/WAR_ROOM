# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 08:28:36 2020

@author: sidyndiaye
"""
import plotly.graph_objects as go

labels = ['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']

values = [4500, 2500, 1053, 500]

fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent',insidetextorientation='radial')])

fig.show()