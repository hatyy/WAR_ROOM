## -*- coding: utf-8 -*-
#"""
#Created on Fri Feb  7 08:32:02 2020
#
#@author: sidyndiaye
#"""
#
## -*- coding: utf-8 -*-
#"""
#Created on Tue Feb  4 16:44:22 2020
#
#@author: sidyndiaye
#"""
#
#import json
#import datetime as dt 
#from datetime import date
#import dash
#import dash_core_components as dcc
#import dash_html_components as html
#import geopandas as gpd
#import pyodbc
#import numpy as np
#import pandas as pd
#import matplotlib
#import matplotlib.cm as cm
#import plotly.graph_objs as go
#import dash_table
#import dash_bootstrap_components as dbc
#from app import app
#
#
#
#app.config.suppress_callback_exceptions = True
#
#
#conn = pyodbc.connect('Driver={SQL Server};'
#                      'Server=BOC-DB;'
#                      'Database=BD_THIERNO_SIDY_ST201908_WARR_ROOM;'
#                      'Trusted_Connection=yes;')
#
#cursor = conn.cursor()
#req=cursor.execute('SELECT * FROM [ACTIF_FL]')
#
#columns = cursor.description 
#result = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
#df= pd.DataFrame(result)
#
#
#
#
#
#df['Territory'] = np.where((df.Territory == 'Dakar ville'),'DAKAR VILLE',df.Territory)
#df['Territory'] = np.where((df.Territory == 'Free Dakar Ville'),'DAKAR VILLE',df.Territory)
#df['Territory'] = np.where((df.Territory == 'Tigo Dakar Ville'),'DAKAR VILLE',df.Territory)
#df['Territory'] = np.where((df.Territory == 'Free Banlieue'),'DAKAR BANLIEUE',df.Territory)
#df['Territory'] = np.where((df.Territory == 'Tigo Banlieue'),'DAKAR BANLIEUE',df.Territory)
#df['Territory'] = np.where((df.Territory == 'Tigo CENTRE'),' CENTRE',df.Territory)
#df['Territory'] = np.where((df.Territory == 'Free CENTRE'),' CENTRE',df.Territory)
#df['Territory'] = np.where((df.Territory == 'Free CENTRE-OUEST'),' CENTRE-OUEST',df.Territory)
#df['Territory'] = np.where((df.Territory == 'Tigo CENTRE-OUEST'),' CENTRE-OUEST',df.Territory)
#df['Territory'] = np.where((df.Territory == 'Free NORD'),' NORD',df.Territory)
#df['Territory'] = np.where((df.Territory == 'Free NORD'),' NORD',df.Territory)
#df['Territory'] = np.where((df.Territory == 'Free NORD-EST'),' NORD-EST',df.Territory)
#df['Territory'] = np.where((df.Territory == 'Tigo NORD-EST'),' NORD-EST',df.Territory)
#df['Territory'] = np.where((df.Territory == 'Tigo SUD'),' SUD',df.Territory)
#df['Territory'] = np.where((df.Territory == 'Free SUD'),' SUD',df.Territory)
#df['Territory'] = np.where((df.Territory == 'Free EST'),' EST',df.Territory)
#
#
#
#df_obj =pd.read_csv('C:\\Users\\sidyndiaye\\Desktop\\dash_h\\objectifs_gross.csv',sep=';',encoding = "ISO-8859-1", engine='python')
#
#df['Territory'] = df['Territory'].str.lstrip()
#df['Territory'] = df['Territory'].str.rstrip()
#
##df= df[(df['Territory'] == 'CENTRE')]
##df=df[['Territory','sale_date','GROSS','ZONE_COM']]
#
#ll=df[['Territory','sale_date','nbr_AFL']]
#
#
#ll['Year'] = pd.DatetimeIndex(ll['sale_date']).year
#datetime_object = pd.DatetimeIndex(df['sale_date'])
#ll['Month'] = datetime_object.month_name()
#ll.sale_date=pd.to_datetime(ll.sale_date,format='%Y-%m-%d')
#
#ll = (ll.groupby(['Year','Month','Territory'],as_index=False).mean()).round(decimals=0)
#ll['Month']=ll['Month'].map({'January':'Janvier','February':'March',3:'Mars','April':'Avril',
#  'May':'Mai','June':'Juin','Jully':'Juillet','August':'Aout','September':'Septembre','October':'Octobre','November':'Novembre','December':'Decembre'})
#
#
#sd = pd.merge(ll,df_obj,on=['Year','Territory','Month'])
#sd['NOM']=sd['Territory']
#
#sd=sd[['Year','Month','NOM','nbr_AFL','objectifs']]
#
## Example shapefile from:
## https://gis-pdx.opendata.arcgis.com/datasets/a0e5ed95749d4181abfb2a7a2c98d7ef_121
## Portland Limited English Proficiency
#lep_shp = "C:\\Users\\sidyndiaye\\Desktop\\dash_h\\TERUTORIES-polygon.shp"
#lep_df = gpd.read_file(lep_shp)
#
#lep_df = pd.merge(lep_df,sd, on =['NOM'])
#
#lep_df['R_O'] = ((lep_df['nbr_AFL']) / (lep_df['objectifs'].astype(int))).round(decimals=2)
#df['Year'] = pd.DatetimeIndex(df['sale_date']).year
#datetime_object = pd.DatetimeIndex(df['sale_date'])
#df['Month'] = datetime_object.month_name()
#df.sale_date=pd.to_datetime(df.sale_date,format='%Y-%m-%d')
#
#df['YearMonth'] = df['sale_date'].apply(lambda x:x.strftime('%Y%m'))
#
#df.YearMonth=pd.to_datetime(df.YearMonth,format='%Y%m')
#
#df= (df.groupby(['Territory','sale_date','Year','Month','ZONE_COM'],as_index=False).mean()).round(decimals=0)
#
#df['Previous'] = df.groupby([df['Year'],df['Month']])['nbr_AFL'].shift()
###YOY%
#fd_ =df[['Territory','sale_date','nbr_AFL']]
#
#fd_['Prev_m'] = fd_.groupby([fd_['sale_date'].dt.month,fd_['sale_date'].dt.day])['nbr_AFL'].shift()
#fd_['Year'] = pd.DatetimeIndex(fd_['sale_date']).year
#
#all = (fd_.groupby(['Year','Territory'],as_index=False).mean()).round(decimals=0)
#
#all['YOY%'] = (((all['nbr_AFL']-all['Prev_m'])/all['Prev_m'])*100).round(decimals=3)
#
#
#fd_m=fd_ =df[['Territory','ZONE_COM','sale_date','nbr_AFL']]
#
#datetime_objects = pd.DatetimeIndex(fd_m['sale_date'])
#
#fd_m['Month'] = datetime_objects.month_name()
#
#fd_m['Prev_m'] = fd_.groupby([fd_['sale_date'].dt.year,fd_['sale_date'].dt.month])['nbr_AFL'].shift()
#
#fd_m['Year'] = pd.DatetimeIndex(fd_m['sale_date']).year
#
#all_m = (fd_m.groupby(['Year','Month','Territory','ZONE_COM'],as_index=False).mean()).round(decimals=0)
#
#all_m['MOM%'] = (((all_m['nbr_AFL'] - all_m['Prev_m'])/all_m['Prev_m'])*100).round(decimals=2)
#
#
##s=pd.merge(all_m,df_obj,on=['Year'], how='inner')
#
##s= all_m.drop_duplicates()
#
#all_m = pd.merge(all_m,df_obj,on=['Year','Territory','Month'])
#
###all_m['objectifs']=  pd.to_numeric(all_m['objectifs'])
#
#all_m['R_O'] = ((all_m['nbr_AFL']) / (all_m['objectifs'].astype(int))).round(decimals=2)
#
#mgr_options = df["Year"].unique()
#
#mgr_option_m = df["Month"].unique()
#
#mgr_option_ZONE_COM = df["Territory"].unique()
#
#
###app = dash.Dash()
#
#app.css.append_css({"external_url": [
#    "https://codepen.io/chriddyp/pen/bWLwgP.css",
#    "https://codepen.io/chriddyp/pen/rzyyWo.css",
#    "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
#]})
#
#
#t=dt.datetime.today().strftime("%Y")
#
#mydate = dt.datetime.now()
#m= mydate.strftime("%B")
#
#val_2018 = 0
#val_2019 = 0
#
#
#max_date = max(df.sale_date)
#
#periode_m= ['January', 'February', 'March','April', 'May', 'June','July', 'August', 'September','October','November','December']
#
##periode_m= periode.strftime("%B")
#for i in periode_m:
#    if(i==m):
#        break
#    val_2018 += int(  df[(df['Year'] == int(t)-1)&(df['Month'] == i)]['nbr_AFL'].mean())
##    val_2019 += int(df[(df['Year'] == int(t))&(df['Month'] == i)]['nbr_AFL'].mean())
##
##
##Croissance = round( ((val_2019-val_2018)/val_2019)*100,2)
##
##
##col = 'De Jan à : '  +""+ max_date.strftime('%B %d, %Y, %r')
###col2 ='De Jan à : '+ ""+date(mydate.year - 1, mydate.month, mydate.day).strftime('%B %d, %Y, %r')
##
##
##data = {col:[val_2019],
##        'Croissance':[Croissance],
##       # col2:[val_2018]}
#
##val_2018 =int( df[df['Year']==2018]['nbr_AFL'].mean())
##val_2019 =int( df[df['Year']==2019]['nbr_AFL'].mean())
#
##Croissance = round( ((val_2019-val_2018)/val_2019)*100,2)
##max_date = max(df.sale_date)
##col = 'De Jan à : '  +""+max_date.strftime('%B %d, %Y, %r')
#
##data = {col:[val_2019],
## #       'Croissance':[Croissance],
##        'ALL 2018 YEAR ':[val_2018]}
#
#
##df_table = pd.DataFrame(data)
#
#
#
#
#fd_s=fd_ =df[['Territory','sale_date','nbr_AFL']]
#fd_s['Week'] = fd_s['sale_date'].dt.week
#fd_s['Year'] = pd.DatetimeIndex(fd_s['sale_date']).year
#datetime_object = pd.DatetimeIndex(fd_s['sale_date'])
#fd_s['Month'] = datetime_object.month_name()
#fd_s=fd_s[['Territory','Year','Month','Week','nbr_AFL']]
#fd_s=fd_s.groupby(['Territory','Week','Year','Month'],as_index=False).mean()
#fd_s=fd_s.sort_values(by = ['Territory','Week','Year','Month'])
#fd_s['Prev_m'] = fd_s.groupby([fd_s['Year'],fd_s['Month'],fd_s['Week']])['nbr_AFL'].shift(1)
#fd_s=fd_s.fillna(0)
#fd_s['base']=fd_s['nbr_AFL']-fd_s['Prev_m']
##fd_s_all = fd_s.groupby(['Year','Month','Territory','Week'],as_index=False).mean()
#
#
#
#
## Generate centroids for each polygon to use as marker locations
#lep_df['lon_lat'] = lep_df['geometry'].apply(lambda row: row.centroid)
#lep_df['LON'] = lep_df['lon_lat'].apply(lambda row: row.x)
#lep_df['LAT'] = lep_df['lon_lat'].apply(lambda row: row.y)
#lep_df = lep_df.drop('lon_lat', axis=1)
#
#lon = lep_df['LON'][0]
#lat = lep_df['LAT'][0]
#
## Get list of languages given in the shapefile
#langs = [lng for lng in lep_df.columns]
#
## Generate stats for example
#lep_df['NUM_LEP'] = lep_df[langs].mean(axis=1)
## Create hover info text
#lep_df['HOVER'] = 'Geography: ' + lep_df.NOM + \
#    '<br /> Num.LEP:' + lep_df.NUM_LEP.astype(str)
#
#mcolors = matplotlib.colors
#
#mon=[]
#for i in range(0,len(lep_df.R_O)):
#    if lep_df.R_O[i]<0.8:
#        mon.append('grey') 
#    elif lep_df.R_O[i]>=0.8 and lep_df.R_O[i]<=1:
#        mon.append('grey') 
#    else:
#        mon.append('grey') 
#
#
#col=[]
#for i in range(0,len(lep_df.R_O)):
#    if lep_df.R_O[i]<0.8:
#        col.append('red') 
#    elif lep_df.R_O[i]>=0.8 and lep_df.R_O[i]<=1:
#        col.append('yellow') 
#    else:
#        col.append('green') 
#
#def set_overlay_colors(dataset):
#    """Create overlay colors based on values
#    :param dataset: gpd.Series, array of values to map colors to
#    :returns: dict, hex color value for each language or index value
#    """
# 
#    minima = dataset.min()
#    maxima = dataset.max()
#    norm = mcolors.Normalize(vmin=minima, vmax=maxima, clip=True)
#    mapper = cm.ScalarMappable(norm=norm, cmap=cm.inferno)
#    colors = [mcolors.to_hex(mapper.to_rgba(v)) for v in dataset]
#    
#
#    overlay_color = {
#        idx: shade
#        for idx, shade in zip(dataset.index, colors)
#    }
#
#    return overlay_color
## End set_overlay_colors()
#
## Create layer options that get displayed to the user in the dropdown
#all_opt = {'label': 'All', 'value': 'All'}
#opts = [{'label': lng.title(), 'value': lng} for lng in langs]
#opts.append(all_opt)
#
## template for map
#map_layout = {
#    'data': [{
#        'lon': lep_df['LON'],
#        'lat': lep_df['LAT'],
#        'mode': 'markers',
#        'marker': {
#            'opacity': 0.0,
#        },
#        'type': 'scattermapbox',
#        #'name': 'Portland LEP',
#        'text': lep_df['HOVER'],
#        'hoverinfo': 'text',
#        'showlegend': True,
#    }],
#    'layout': {
#        'autosize': False,
#        'hovermode': 'closest',
#        'margin': {'l': 50, 'r': 0, 'b': 0, 't': 0},
#        'mapbox': {
#            'accesstoken': 'pk.eyJ1IjoiamFja3AiLCJhIjoidGpzN0lXVSJ9.7YK6eRwUNFwd3ODZff6JvA',
#            'center': {
#                'lat': lat,
#                'lon': lon
#            },
#            'zoom': 6.0,
#            'bearing': 0.0,
#            'pitch': 0.0,
#        },
#    }
#}
#PLOTLY_LOGO = "data:image/png;base64,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"
#
#_navbar = dbc.Navbar(  
#    sticky="top",
#    color="light",
#    dark="True",
#    children=[
#         html.A(
#            # Use row and col to control vertical alignment of logo / brand
#            dbc.Row(
#                [
#                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="50px",width="500px")),
#                    
#                ],
#                align="center",
#                no_gutters=True,
#            ),
#            href="#",
#            
#        ),
#   
#        dbc.DropdownMenu(
#            nav=True,
#            #in_navbar=True,
#            label="S&D Telco",
#            children=[
#                dbc.DropdownMenuItem("GROSS_ALL",href='GROSS_ALL'),
#                dbc.DropdownMenuItem("PARC"),
#                dbc.DropdownMenuItem(divider=True),
#                dbc.DropdownMenuItem("SWAP",href='/swap'),
#                dbc.DropdownMenuItem("GRATTE")
#            ],
#            
#            
#        ),
#        
#        dbc.DropdownMenu(
#            nav=True,
#            in_navbar=True,
#            label="FREEMONEY",
#            children=[
#                dbc.DropdownMenuItem("EMONEY PURCHASSE",href='/EM_purchasse'),
#                dbc.DropdownMenuItem("EMONEY INJECTE",href='EM_INJECTE'),
#                dbc.DropdownMenuItem(divider=True),
#                dbc.DropdownMenuItem("WALLET",href='/wallet'),
#                dbc.DropdownMenuItem("BALANCE SUPER-AGENT")
#            ],
#        ),
#        dbc.DropdownMenu(
#            nav=True,
#            in_navbar=True,
#            label="CANNAUX",
#            children=[
#                dbc.DropdownMenuItem("FREELANCER",href='/freelancer'),
#                dbc.DropdownMenuItem("BOUTIQUE",href='/Boutique'),
#                dbc.DropdownMenuItem(divider=True),
#                dbc.DropdownMenuItem("POA",href='/POA'),
#                dbc.DropdownMenuItem("QUIOSQUE",href='/KIOSQUE')
#            ],
#        ),
#        dbc.DropdownMenu(
#            nav=True,
#            in_navbar=True,
#            label="ACHAT GROSSIST",
#            children=[
#                dbc.DropdownMenuItem("ACHAT GRS"),
#                dbc.DropdownMenuItem(divider=True),
#                dbc.DropdownMenuItem("BALANCE DEALER")                              
#            ],
#        ),
#        dbc.DropdownMenu(
#            nav=True,
#            in_navbar=True,
#            label="AGENCE",
#            children=[
#                dbc.DropdownMenuItem("AQUISITION"),
#                dbc.DropdownMenuItem("SWAP"),
#                dbc.DropdownMenuItem(divider=True),
#                dbc.DropdownMenuItem("FILE D'ATTENTE"),
#                dbc.DropdownMenuItem("VENTE DE SMARPHONE")             
#            ],
#        ),
#        
#        
#        dbc.DropdownMenu(
#            nav=True,
#            in_navbar=True,
#            label="QoS ITN",
#            children=[
#                dbc.DropdownMenuItem("PLATEFORME"),
#                 dbc.DropdownMenuItem(divider=True),
#                dbc.DropdownMenuItem("RESEAUX")
#               
#                            
#            ],
#        ),
#             dbc.Row(
#    [
#        dbc.Col(
#            dbc.Button("ALL TERRYTORY GROSS ALL", color="primary", className="ml-2",block=True),
#            width="500px",
#        ),
#    ],
#    no_gutters=True,
#    className="ml-auto flex-nowrap mt-3 mt-md-0",
#    align="center",
#),
#       
#    ],
#)
#
#"""
#external_stylesheets = [dbc.themes.SIMPLEX]
#
#app = Dash(
#    __name__,
#    external_stylesheets=external_stylesheets
#)
#"""
#app.layout = html.Div([_navbar])
#
#
#
#
#trace_1 = go.Scatter(x = fd_s.Week, y = fd_s['nbr_AFL'],
#                    name = 'ACTIF',
#                    line = dict(width = 2,
#                                ))
##layout = go.Layout(title = 'Time Series Plot',
#                   #hovermode = 'closest',width=500,margin=dict(l=50)) 
#
#fig = go.Figure(data = [trace_1])
#
#
#
#
#
#
#
#
#
#
#layout = html.Div([
#      html.Div([_navbar]),
#      
#      html.Div(
#        [
#            dcc.Dropdown(
#                id="Territory",
#                options=[{
#                    'label': i,
#                    'value': i
#                } for i in mgr_options],
#                value='All Year'),
#        ],
#         style = {'width': '30%',
#                  'fontSize' : '20px',
#                  'padding-left' : '50px',
#                  'padding-top' : '5px',
#                  'height': '40px',
#                  'display': 'inline-block'}),
#
#    html.Div(
#        [
#            dcc.Dropdown(
#                id="month",
#                options=[{
#                    'label': i,
#                    'value': i
#                } for i in mgr_option_m],
#                value='All Month'),
#        ],
#         style = {'width': '30%',
#                  'fontSize' : '20px',
#                  'padding-top' : '5px',
#                 'padding-left' : '100px',
#                  'height': '40px',
#                  'display': 'inline-block'}),
#    
#    #mgr_option_ZONE_COM
#html.Div(
#        [
#            dcc.Dropdown(
#                id="zone_com",
#                options=[{
#                    'label': i,
#                    'value': i
#                } for i in mgr_option_ZONE_COM],
#                value='All ZONE'),
#        ],
#         style = {'width': '35%',
#                  'fontSize' : '20px',
#                  'padding-top' : '5px',
#                 'padding-left' : '100px',
#                  'height': '40px',
#                  'display': 'inline-block'})    
#    
#    ,
#html.Div([
#        dcc.Graph(id='map-display-FC'),    
#    
#  
# dash_table.DataTable(
#    id='table-FC',
#    columns=[{"name": i, "id": i} for i in df_table.columns],
#    data=df_table.to_dict('records'),
#    style_data_conditional=[
#        {
#            'if': {
#                'column_id': 'Croissance',
#                'filter_query': '{Croissance} <0'
#            },
#            'color': 'red',
#        },
#                    {
#            'if': {
#                'column_id': 'Croissance',
#                'filter_query': '{Croissance} >0'
#            },
#            'color': 'green',
#        }
#                    
#        ],
#style_table={
#      'width':'95%',
#      'padding': 40,
#      
#    },
#        style_cell={'textAlign': 'center','font_size': '26px'},
#         style_header={
#        'backgroundColor': 'rgb(55, 83, 109)',
#        'fontWeight': 'bold',
#        'color':'white'
#    }
#),
#
#html.Div(dash_table.DataTable(
#        
#        id='datatable-paging-FC',
#        
#        data=all_m.to_dict('records'),
#        
#        columns=[{'id': c, 'name': c} for c in all_m.columns],
#        
#        style_cell_conditional=[
#     {
#       'if': {'column_id': c},
#       
#           'display': 'none'
#           
#           } for c in ['Year', 'Month','Prev_m','Territory']
#             
#     ],
#      style_data={
#        'whiteSpace': 'normal',
#        'height': '30px',
#        'size':'50px'
#    },  
#        
#         style_header={
#        'backgroundColor': 'rgb(55, 83, 109)',
#        'fontWeight': 'bold',
#        'color':'white'
#    },
#style_data_conditional=[
#        {
#            'if': {
#                'column_id': 'MOM%',
#                'filter_query': '{MOM%} <0'
#            },
#            'color': 'red',
#        },
#        {
#            'if': {
#                'column_id': 'MOM%',
#                'filter_query': '{MOM%} >0'
#            },
#            'color': 'green',
#        },
#        {
#            'if': {
#                'column_id': 'R_O',
#                'filter_query': '{R_O} < 0.8'
#            },
#            'color': '0000FF',
#            'backgroundColor':'red'
#        },
#        {
#            'if': {
#                'column_id': 'R_O',
#                'filter_query': '0.8 <= {R_O} <= 1'
#            },
#            'color': '0000FF',
#            'backgroundColor':'yellow'
#        },
#        {
#            'if': {
#                'column_id': 'R_O',
#                'filter_query': '{R_O} > 1'
#            },
#            'color': '0000FF',
#            'backgroundColor':'green'
#        }
#       ]
#        ,
#        style_table={
#        'top':'40%',
#        'maxHeight': '70ex',
#        'overflowY': 'scroll',
#        'width': '50%',
#        'minWidth': '20%',
#        'left':'45%',
#        'float':'left'
#        
#    },
#      style_cell={'textAlign': 'center','height':'33px','font_size': '22px'},
#     
#   
#        
#)),
#
#    dcc.Graph(id='funnel-graph-FC',style={"height" : "25%", "width" : "40%"}),
#    dcc.Graph(id='funnel-AC',style={"height" : "25%", "width" : "40%"}),
#    dcc.Graph(id = 'plot-FC', figure = fig,style={"height" : "50%", "width" : "60%","position":"absolute","left":"42%","top":"95%"}),
#    ])
#])
#@app.callback(
#    dash.dependencies.Output('map-display-FC', 'figure'),
#    [dash.dependencies.Input('month', 'value')])
#
#def update_map(overlay_choice):
#
#    tmp = map_layout.copy()
#    if overlay_choice == 'All Month':
#        dataset = lep_df
#        colors = mon
#        tmp['data'][0]['text'] = lep_df['HOVER']
#    else:
#        dataset = lep_df[(lep_df['Month'] == overlay_choice)]
#
#        colors = col
#
#        # Update hovertext display
#        hovertext = lep_df['NOM'].str.cat(
#                        lep_df['Month'].astype(str), sep=': ')
#        tmp['data'][0]['text'] = hovertext
#    # End if
#    # Create a layer for each region colored by LEP value
#    layers = [{
#        'name': overlay_choice,
#        'source': json.loads(dataset.loc[dataset.index == i, :].to_json()),
#        'sourcetype': 'geojson',
#        'type': 'fill',
#        'opacity': 1.0,
#        'color': colors[i]
#    } for i in dataset.index]
#
#    tmp['layout']['mapbox']['layers'] = layers
#
#    return tmp
#
#
#
#@app.callback(
#    [dash.dependencies.Output('datatable-paging-FC', 'data'),dash.dependencies.Output('funnel-graph-FC', 'figure'),dash.dependencies.Output('funnel-AC', 'figure'),
#     dash.dependencies.Output('plot-FC', 'figure')],
#    
#    [dash.dependencies.Input('Territory', 'value'),dash.dependencies.Input('month', 'value'),dash.dependencies.Input('zone_com', 'value')])
#
#def updates_table(Year,month,zone_com):
#   
#    if Year == "All Year":
#        
#        all_plot =all_m.copy()
#        df_plot_y = df.copy()
#        df_plot_m = df.copy()
#        
#    else :
#         all_plot = all_m[(all_m['Year'] == Year)&(all_m['Month'] == month)&(all_m['Territory'] == zone_com)]
#         
#         df_plot_y = df[(df['Year'] == Year)&(df['Territory'] == zone_com)]
#    pv = pd.pivot_table(
#        df_plot_y,
#        index=['ZONE_COM'],
#        values=['nbr_AFL','Previous'],
#        aggfunc=np.mean,
#        fill_value=0)
#
#    MTD = go.Bar(x=pv.index, y=pv['nbr_AFL'],name='ACTIF',marker_color='rgb(55, 83, 109)')
#    MTD_1 = go.Bar(x=pv.index, y=pv['Previous'],name='PREVIOUS', marker_color='rgb(26, 118, 255)')
#    
#    
#    df_plot_m = df[(df['Year'] == Year)&(df['Month'] == month)&(df['Territory'] == zone_com)]
#    pv = pd.pivot_table(
#        df_plot_m,
#        index=['ZONE_COM'],
#        values=['nbr_AFL','Previous'],
#        aggfunc=np.mean,
#        fill_value=0)
#
#    MTD_m = go.Bar(x=pv.index, y=pv['nbr_AFL'],name='ACTIF',marker_color='rgb(55, 83, 109)')
#    MTD_1_m = go.Bar(x=pv.index, y=pv['Previous'],name='PREVIOUS', marker_color='rgb(26, 118, 255)')
#    
#    st2 = fd_s[(fd_s['Year']==Year)&(fd_s['Month']==month)&(fd_s['Territory']==zone_com)]
#    trace_1 = go.Scatter(x = st2.Week, y = st2['nbr_AFL'],
#                        name = 'ACTIF',
#                        line = dict(width = 2,
#                                    ))
#    trace_2 = go.Scatter(x = st2.Week, y = st2['Prev_m'],
#                        name = 'PREVIOUS',
#                        line = dict(width = 2,
#                                    ))
#    fig = go.Figure(data = [trace_1])
#   
#    return all_plot.to_dict('records'),{
#        'data': [MTD,MTD_1],
#        'layout':
#        go.Layout(
#            title=' ACTIF YOY% {}'.format(Year),
#            barmode='group')
#  },{
#        'data': [MTD_m,MTD_1_m],
#        'layout':
#        go.Layout(
#            title=' ACTIF MOM% {}'.format(Year),
#            barmode='group')
#  },fig 
# 
#
#    
#    
#    
#    
#    
#    