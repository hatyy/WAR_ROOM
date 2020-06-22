# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 11:11:42 2020

@author: sidyndiaye
"""
import dash_bootstrap_components as dbc
from dash import Dash
import dash_core_components as dcc
#import dash_html_components as html

print(dcc.__version__) # 0.6.0 or above is required


external_stylesheets = [dbc.themes.SIMPLEX]

app = Dash(
    __name__,
    external_stylesheets=external_stylesheets
)

app.config.suppress_callback_exceptions = True
server = app.server
