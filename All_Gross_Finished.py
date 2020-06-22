# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 11:57:36 2020

@author: tndao
"""
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib
from navbar import navbar
from connect import connection, cursor
from dateutil.relativedelta import relativedelta
import json
import matplotlib.cm as cm
from sort_dataframeby_monthorweek import Sort_Dataframeby_Month


navbar = navbar()
##########DASH App################
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
#gdf = gpd.read_file('ZONE_COM_-.shp') 
#All Gross Table
Req_Gross=cursor.execute('SELECT * FROM ALL_GROSS')
columns = cursor.description
result = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
All_Gross_Table= pd.DataFrame(result)
Objectifs = pd.read_csv('C:/Users/tndao/Desktop/War room Pandas/Objectifs_Gross.csv', sep=';')
All_Gross_Table['ROLE'] = All_Gross_Table['ROLE'].map({'team leader':'FREELANCER','TEAM LEADER':'FREELANCER',
'chef agence':'Chef Agence','Chef Agence':'Chef Agence',
'sales coordinator':'FREELANCER','SALES COORDINATOR':'FREELANCER',
'Mobile agent':'MOBILE AGENT','MOBILE AGENT':'MOBILE AGENT',
'Freelancer':'FREELANCER' ,'FREELANCER':'FREELANCER',
'Espace Tigo':'ESPACE TIGO','ESPACE TIGO':'ESPACE TIGO',
'AGENT MIDCOM_SMK':'AGENT MIDCOM_SMK',
'BOUTIQUE':'BOUTIQUE',
'Complaint':'Complaint',
'Stagiaire ':'Stagiaire ',
'Dealer':'Dealer',
'ESPACE TIGO/dealer':'ESPACE TIGO',
'Experience Center Agent' :'Experience Center Agent' ,
'MOBILE AGENT' :'MOBILE AGENT',
'MARKET DEV':'MARKET DEV',
'POA':'POA','ROOT SUPERVISOR':'ROOT SUPERVISOR'})


#Data Analysis
All_Gross_Table['sale_date']=pd.to_datetime(All_Gross_Table['sale_date'])
All_Gross_Table['GROSS']=pd.to_numeric(All_Gross_Table['GROSS'], downcast='unsigned')
All_Gross_Table['FullName']=All_Gross_Table['FullName'].astype(str)
All_Gross_Table['Quarter']=All_Gross_Table['sale_date'].dt.quarter
All_Gross_Table['Month']=All_Gross_Table['sale_date'].dt.strftime('%B')
All_Gross_Table['Year']=All_Gross_Table['sale_date'].dt.year
All_Gross_Table['Week']=All_Gross_Table['sale_date'].dt.week
#Objectifs['objectifs']=pd.to_numeric(Objectifs['objectifs'], downcast='unsigned')

##Replacing Territory Values
All_Gross_Table['Territory'] = All_Gross_Table['Territory'].map({'Free SUD':'SUD','Tigo SUD':'SUD','SUD':'SUD','CENTRE':'CENTRE','Free CENTRE':'CENTRE',
'Tigo CENTRE':'CENTRE',' CENTRE':'CENTRE','Free CENTRE-OUEST':'CENTRE-OUEST','CENTRE-OUEST':'CENTRE-OUEST','Tigo CENTRE-OUEST':'CENTRE-OUEST',
'Free Dakar Ville':'DAKAR VILLE', 'DAKAR VILLE':'DAKAR VILLE', 'Dakar ville':'DAKAR VILLE', 'Tigo Dakar Ville':'DAKAR VILLE',
'Free Banlieue':'DAKAR BANLIEUE', 'DAKAR BANLIEUE':'DAKAR BANLIEUE', 'Tigo Banlieue':'DAKAR BANLIEUE', 'DAKAR BANLIEUE ' :'DAKAR BANLIEUE',
'Tigo NORD-EST':'NORD-EST','NORD-EST':'NORD-EST','Free NORD-EST':'NORD-EST',
'Free EST':'EST', 'EST' :'EST',
'Free NORD':'NORD', 'NORD':'NORD',
'Complaint':'Complaint',
 '' :'',
'UNKONWN':'UNKONWN',
'NULL' :'NULL',
'AGENCE' :'AGENCE',
None :None})


#MTD
tmp= All_Gross_Table.sale_date.max()
start_Date_MTD =tmp.to_period('M').to_timestamp()
end_Date_MTD = All_Gross_Table.sale_date.max()
mask =(All_Gross_Table['sale_date']>= start_Date_MTD) & (All_Gross_Table['sale_date']<= end_Date_MTD)
MTD_Table = All_Gross_Table[mask]

MTD_Tab= MTD_Table.groupby(['Month','Territory'], as_index=False)[['GROSS']].sum()
MTD = MTD_Tab['GROSS']


#MTD-1
tmp1= All_Gross_Table.sale_date.max() + relativedelta(months=-1)
start_Date_MTD_1 = tmp1.to_period('M').to_timestamp()
end_Date_MTD_1 = All_Gross_Table.sale_date.max() + relativedelta(months=-1)
mask_MTD_1 =(All_Gross_Table['sale_date']>= start_Date_MTD_1) & (All_Gross_Table['sale_date']<= end_Date_MTD_1)
MTD_Table_1= All_Gross_Table[mask_MTD_1]
MTD_1_Tab= MTD_Table_1.groupby(['Month','Territory'], as_index=False)[['GROSS']].sum()
MTD_1 = MTD_1_Tab['GROSS']


##Month over Month
MoM= ((MTD - MTD_1)/MTD_1)*100


#YTD
tmp2= All_Gross_Table.sale_date.max()
start_Date_YTD =tmp2.to_period('Y').to_timestamp()
end_Date_YTD = All_Gross_Table.sale_date.max()
mask_YTD =(All_Gross_Table['sale_date']>= start_Date_YTD) & (All_Gross_Table['sale_date']<= end_Date_YTD)
YTD_Table= All_Gross_Table[mask_YTD]
YTD_Tab= YTD_Table.groupby(['Year'], as_index=False)[['GROSS']].sum()
YTD = YTD_Tab['GROSS']
YTD_year = YTD_Tab['Year']
YTD_Tab_Month= YTD_Table.groupby(['Month','Territory'], as_index=False)[['GROSS']].sum()



#YTD-1
tmp3= All_Gross_Table.sale_date.max() + relativedelta(years=-1)
start_Date_YTD_1 =tmp3.to_period('Y').to_timestamp()
end_Date_YTD_1 = All_Gross_Table.sale_date.max() + relativedelta(years=-1)
mask_YTD_1 =(All_Gross_Table['sale_date']>= start_Date_YTD_1) & (All_Gross_Table['sale_date']<= end_Date_YTD_1)
YTD_Table_1= All_Gross_Table[mask_YTD_1]
YTD_1_Tab= YTD_Table_1.groupby(['Year'], as_index=False)[['GROSS']].sum()
YTD_1= YTD_1_Tab['GROSS']
YTD_1_Year= YTD_1_Tab['Year']
YTD_Tab_1_Month= YTD_Table_1.groupby(['Month','Territory'], as_index=False)[['GROSS']].sum()
YTD_Tab_1_Month.sort_values(by=['Territory'])
##Year over Year
YoY= ((YTD - YTD_1)/YTD_1)*100

###♠Final Table 
fina_ytd= YTD_Table.groupby(['Territory'], as_index=False)[['GROSS']].sum()
fina_ytd_1= YTD_Table_1.groupby(['Territory'], as_index=False)[['GROSS']].sum()
fina_mtd= MTD_Table.groupby(['Territory'], as_index=False)[['GROSS']].sum()
fina_mtd_1= MTD_Table_1.groupby(['Territory'], as_index=False)[['GROSS']].sum()

fin_half= pd.merge(left=fina_ytd,right=fina_ytd_1,left_on='Territory',right_on='Territory')
fin_half1= pd.merge(left=fina_mtd,right=fina_mtd_1,left_on='Territory',right_on='Territory')
finale_mi= pd.merge(left=fin_half,right=fin_half1,left_on='Territory',right_on='Territory')
finale_Table= pd.merge(left=finale_mi,right=Objectifs,left_on='Territory',right_on='Territory')
#finale_Table.drop(columns=['Year_x','Year_y','Month_x','Month_y'])
finale_Table.rename(columns={'GROSS_x_y':'Current Month','GROSS_y_y':'Previous Month','GROSS_x_x':'Current Year','GROSS_y_x':'Previous Year'},inplace = True)
finale_Table['MoM']= ((finale_Table['Current Month'] - finale_Table['Previous Month'])/finale_Table['Previous Month'])*100
finale_Table['R/O'] = finale_Table['Current Month'] / finale_Table['objectifs']
finale_Table['YoY']= ((finale_Table['Current Year'] - finale_Table['Previous Year'])/finale_Table['Previous Year'])*100

print(finale_Table)

pd.options.display.float_format = '{:,.2f}'.format  

##Gross week 
Grossbyweek= All_Gross_Table.groupby(['Territory','Year','Month','Week'], as_index=False)[['GROSS']].sum()
#gross by week by territories
Grossbyweekbyterritory= All_Gross_Table.groupby(['Territory','Year','Week'], as_index=False)[['GROSS']].sum()
#gross by week by zone_com
Grossbyweekbyzc= All_Gross_Table.groupby(['Year','Week'], as_index=False)[['GROSS']].sum()

#All_Gross_Table['Previousweek'] = pd.to_datetime(All_Gross_Table['sale_date']) + relativedelta(weeks=+1)
#print(All_Gross_Table['Previousweek'])

print(All_Gross_Table)
print(Grossbyweek)
#Aggregate data#
#Aggregate data#

for ind in Grossbyweek.index:
    if Grossbyweek['Month'][ind] == 'December' and Grossbyweek['Week'][ind] == 1:
        Grossbyweek['Year'][ind] = Grossbyweek['Year'][ind]+1
        Grossbyweek['Month'][ind] ='January'


Sort_Dataframeby_Month(df=Grossbyweek,monthcolumnname='Month')  
mask_wdd =(Grossbyweek['Year']== 2020) 
Grossbyweek=Grossbyweek[mask_wdd] 
mask_wd =(Grossbyweek['Territory']== 'DAKAR VILLE') 
Grossbyweek=Grossbyweek[mask_wd] 
#mask_wdm =(Grossbyweek['Month']== 'June') 
#Grossbyweek=Grossbyweek[mask_wdm] 
Grossbyweek['Pweek'] = np . where ( Grossbyweek['Week'] >=2 , Grossbyweek['Week']-1 , 52 ) 
Grossbyweek['PValues'] = np . where ( Grossbyweek['Week'] == Grossbyweek['Pweek']+1,Grossbyweek['GROSS'].shift(1),0) 
Grossbyweek['change'] = Grossbyweek['GROSS'] - Grossbyweek['PValues']


df_sort = Sort_Dataframeby_Month(df=Grossbyweek,monthcolumnname='Month')
df_sort
 
#### this month

this_month = MTD_Table.groupby(['sale_date','Month','Territory'], as_index=False)[['GROSS']].sum()
this_month ['Day']=this_month['sale_date'].dt.day
mask_wdt =(this_month['Territory']== 'DAKAR VILLE') 
this_month =this_month [mask_wdt] 

#### previous month
Prev_month = MTD_Table_1.groupby(['sale_date','Month','Territory'], as_index=False)[['GROSS']].sum()
Prev_month ['Day']=Prev_month['sale_date'].dt.day
mask_pt =(Prev_month['Territory']== 'DAKAR VILLE') 
Prev_month =Prev_month [mask_pt] 


mapbox_key = "pk.eyJ1IjoiYmlib3kxMjMiLCJhIjoiY2s1cDZjdHZjMWNlMTNkcnczZTF2Mmc2dSJ9.rRDb7sYg4PKvD9yf3kzZag"
if not mapbox_key:
    raise RuntimeError("Mapbox key not specified! Edit this file and add it.")

# Example shapefile from:
# https://gis-pdx.opendata.arcgis.com/datasets/a0e5ed95749d4181abfb2a7a2c98d7ef_121

lep_shp = 'Territories/TERUTORIES-polygon.shp'
lep_df = gpd.read_file(lep_shp)

# Generate centroids for each polygon to use as marker locations
lep_df['lon_lat'] = lep_df['geometry'].apply(lambda row: row.centroid)
lep_df['LON'] = lep_df['lon_lat'].apply(lambda row: row.x)
lep_df['LAT'] = lep_df['lon_lat'].apply(lambda row: row.y)
lep_df = lep_df.drop('lon_lat', axis=1)

lon = lep_df['LON'][0]
lat = lep_df['LAT'][0]

# Generate stats for example

lep_df['NUM_LEP'] = finale_Table['R/O']

# Create hover info text
lep_df['HOVER'] = 'Territoire: ' + lep_df.NOM +\
    '<br /> R/O: '+lep_df['NUM_LEP'].astype(str)

mcolors = matplotlib.colors


def set_overlay_colors(dataset):
    """Create overlay colors based on values
    :param dataset: gpd.Series, array of values to map colors to
    :returns: dict, hex color value for each language or index value
    """
    minima = dataset.min()
    maxima = dataset.max()
    norm = mcolors.Normalize(vmin=minima, vmax=maxima, clip=True)
    mapper = cm.ScalarMappable(norm=norm, cmap=cm.cool)
    colors = [mcolors.to_hex(mapper.to_rgba(v)) for v in dataset]

    overlay_color = {
        idx: shade
        for idx, shade in zip(dataset.index, colors)
    }

    return overlay_color
# End set_overlay_colors()




# template for map
map_layout = {
    'title': 'Free Sn',
    'data': [{
        'lon': lep_df['LON'],
        'lat': lep_df['LAT'],
        'mode': 'markers',
        'marker': {
            'opacity': 0.6,
        },
        'type': 'scattermapbox',
        'name': 'Free Sn',
        'text': lep_df['HOVER'],
        'hoverinfo': 'text',
        'showlegend': True,
    }],
    'layout': {
        'autosize': True,
        'hovermode': 'closest',
        'margin': {'l': 0, 'r': 0, 'b': 0, 't': 0},
        'mapbox': {
            'accesstoken': mapbox_key,
            'center': {
                'lat': 14.30,
                'lon': -14.35
            },
            'zoom': 6.0,
            'bearing': 0.0,
            'pitch': 0.0,
        },
    }
}


###
byRole= All_Gross_Table.groupby(['ROLE','Year','Month'], as_index=False)[['GROSS']].sum()
maskr =(byRole['Month']== 'April') & (byRole['Year']== 2019)
byRole= byRole[maskr]
w = byRole['ROLE'].unique()
##Replacing Territory Values

bytype= All_Gross_Table.groupby(['type','Year','Month'], as_index=False)[['GROSS']].sum()
maskt =(bytype['Month']== 'April') & (bytype['Year']== 2019)
bytype= bytype[maskt]
w = bytype['type'].unique()
bytype['type'] = bytype['type'].map({'GROSS POS-AP':'POS-AP','GROSS USSD':'USSD'})









#Aggregate data#
"""Sale_ThisYear_by_Vendors= All_Gross_Table.groupby(['FullName','Month','Year'], as_index=False)[['GROSS']].sum()"""
### Selector Options
Territory_Option = []
for Territory in All_Gross_Table['Territory'].unique():
    Territory_Option.append({'label':str(Territory),'value':Territory})
    Month_Option = []
for Month in All_Gross_Table['Month'].unique():
    Month_Option.append({'label':str(Month),'value':Month})
    Year_Option = []
for Year in All_Gross_Table['Year'].unique():
    Year_Option.append({'label':str(Year),'value':Year})
    
card_content1 = [
    dbc.CardHeader(YTD_1_Year),
    dbc.CardBody(
        [
            html.H5(YTD_1 , className="card-title"),
        ]
    )
]

card_content2 = [
    dbc.CardHeader("YoY Growth(%)"),
    dbc.CardBody(
        [
            html.H5(YoY , className="card-title"),
        ]
    )
]

card_content3 = [
    dbc.CardHeader(YTD_year),
    dbc.CardBody(
        [
            html.H5(YTD , className="card-title"),
        ]
    )
]


body = dbc.Container([
         dbc.Row(
            [
                     dbc.Col(
                    [
                       html.H1("ALL GROSS",style={'text-align':'center'})
                    ],
                     md=12),
            ],
            className="mb-12",
            style={'text-align':'center'}
        ),
                            
                
     dbc.Row([
                dbc.Col(
                    [
                    html.H3("Filters by:"),
                    dcc.Dropdown(id='Territory_picker',options= Territory_Option ,value=All_Gross_Table['Territory'].unique(),multi=True,style={'margin':'5% 1% 5% 1%'}),
                    dcc.Dropdown(id='overlay-choice', options=Month_Option,value='All',style={'margin':'5% 1% 5% 1%'}),
                    dcc.Dropdown(id='Year_Picker', options=Year_Option ,value=YTD_year,multi=True,style={'margin':'5% 1% 5% 1%'}),
                    ],
                     md=5),
                    dbc.Col(
                    [
                      dcc.Graph(id='map-display')
                         ],
                     md=7,
            style={'text-align':'center','margin':'1% 0% 1% 0%' }),
                   
                   
                ]),
                dbc.Row(
            [
                dbc.Col(dbc.Card(card_content1, inverse=True, style={'text-align':'center','backgroundColor':'#ca4f00'})),
                dbc.Col(
                    dbc.Card( card_content2, inverse=True, style={'text-align':'center','backgroundColor':'#ca4f00'})
                ),
                dbc.Col(dbc.Card( card_content3 , inverse=True, style={'text-align':'center','backgroundColor':'#ca4f00'})),
            ],
            className="mb-4",
        ),
                    
                    
                    ###Dash Table
                 html.Div([ 
                           dbc.Row([
                           dbc.Col(
                    [
                      
                    ],
                     md=12),
                ]),
 
                dbc.Row([
                  dbc.Col(
                    [
                           
                                    dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in finale_Table.columns],
    data=finale_Table.to_dict('records'),
    style_data_conditional=[{
            'if': {
                'column_id': 'R/O',
                'filter_query': '{R/O} >= 1'
            },
            'backgroundColor': '#3D9970',
            'color': 'white',
        },
        {
            'if': {
                'column_id': 'R/O',
                'filter_query': '{R/O} <= 0.8'
            },
            'backgroundColor': '#e33232',
            'color': 'white',
        }]
)

                                    
                                   
    

                    ],
                    md=12,
                ),
                    ])
     ]),
    
                
                ###MAP MAP
     
                ###
                
                ###
            dbc.Row([
                  dbc.Col(
                    [
                        dcc.Graph(id='month',
                            figure={"data": [{"x": YTD_Tab_Month['Territory'], "y": YTD_Tab_Month['GROSS'],'type': 'bar', 'text' : YTD_Tab_Month['GROSS'],'name': 'Current Year'},
                            {"x": YTD_Tab_1_Month['Territory'], "y": YTD_Tab_1_Month['GROSS'],'type': 'bar', 'name': 'Previous Year'}
                            ]}
                        ),
                            html.H5("Current Year VS Previous Year by Territory",style={'text-align':'center',}),
                    ],
                    md=7,style={'padding':'0.5% 0.5% 0.5% 0.5%'}
                ),
                     dbc.Col(
                    [
                        dcc.Graph( figure=dict(
        data=[
                 dict(
                x=Prev_month['Day'],
                y=Prev_month['GROSS'],
                mode='lines+markers',
                name= 'Month-1',
                marker=dict(
                    color='rgb(55, 83, 109)'
                ),
                
                 ),
               dict(
                x=this_month['Day'],
                y=this_month['GROSS'],
                mode='lines+markers',
                name='this month',
                marker=dict(
                    color='rgb(255, 0, 0)'
                )
                 ),   
        ],
        layout=dict(
            showlegend=True,
            legend=dict(
                x=0,
                y=1.0
            ),
            paper_bgcolor = '#ffffff', plot_bgcolor='#ffffff',
            margin=dict(l=40, r=0, t=40, b=30)
        )
    ),
    id='my-graph'  ),
                            html.H5("This month vs last month evolution",style={'text-align':'center'}),
                    ],
                    md=5,
                    style={'padding':'0.5% 0.5% 0.5% 0.5%'}
                )
                    ]),
        
          #second row
                dbc.Row([
                  dbc.Col(
                    [
                       dcc.Graph(
                               id='FUN',

                                        figure = {'data':[

                       go.Funnel(
             y = bytype['type'].unique(),
             x = bytype['GROSS'])
            ],

                                        'layout':go.Layout(paper_bgcolor = '#ffffff', plot_bgcolor='#ffffff')}
                       ), html.H5("Part by Role",style={'text-align':'center','padding':'0.5% 0.5% 0.5% 0.5%'})

                    ],
                    md=6,
                ),
        dbc.Col([
                       dcc.Graph(
                               id='FUN1',

                                        figure = {'data':[

                       go.Pie(
  labels=byRole['ROLE'].unique(),
   values=byRole['GROSS'], hole=.3)
                                                ],

                                        'layout':go.Layout(paper_bgcolor = '#ffffff', plot_bgcolor='#ffffff')}
                       ), html.H5("Part by Role",style={'text-align':'center','padding':'0.5% 0.5% 0.5% 0.5%','margin':'0, 0, 0, 30%'})

                    ],
                    md=6,
                ),


                    ]),
                #Graph
                dbc.Row([
                  dbc.Col(
                    [
                        dcc.Graph(id='waterfall1',

                                        figure = {'data':[

                        go.Waterfall(
                    name="week over week",
                    orientation = "v",
                    textposition = "outside",
                    text = df_sort['change'],
                    x =df_sort['Week'],
                    y = df_sort['change'],
                    #connector = {"line":{"color":"rgb(63, 63, 63)"}},
                    decreasing = {"marker":{"color":"Maroon", "line":{"color":"red", "width":3}}},
                    increasing = {"marker":{"color":"Teal"}},
                    totals = {"marker":{"color":"deep sky blue", "line":{"color":'blue', "width":4}}}
                    )

                                                ],

                                        'layout':go.Layout(paper_bgcolor = '#ffffff', plot_bgcolor='#ffffff', waterfallgap = 0.3)}
                                        ),
                        html.H5("Week over Week variation",style={'text-align':'center','padding':'0.5% 0.5% 0.5% 0.5%'})
                    ],
                    md=12,
                ), 
                    ]),
                                         
    
        ], fluid=True,style={'backgroundColor':'#ca8300','color':'#d4020e'}
    )


app.layout = html.Div([navbar,body])


"""#Call back Functions
@app.callback(Output('my-graph', 'figure'),
	              [Input('Territory_picker', 'value')])
def update_figure(selected_Territory):
	  filtered_df = All_Gross_Table[All_Gross_Table['Territory'] == selected_Territory]"""
      
@app.callback(
    dash.dependencies.Output('map-display', 'figure'),
    [dash.dependencies.Input('overlay-choice', 'value')])
def update_map(overlay_choice):

    tmp = map_layout.copy()
    if overlay_choice == 'All':
        dataset = lep_df
        colors = set_overlay_colors(lep_df.NUM_LEP)
        tmp['data'][0]['text'] = lep_df['HOVER']
    else:
        dataset = lep_df.loc[lep_df[overlay_choice] > 0, :]

        colors = set_overlay_colors(dataset[overlay_choice])

        # Update hovertext display
        hovertext = lep_df['Geography'].str.cat(
                        lep_df[overlay_choice].astype(str), sep=': ')
        tmp['data'][0]['text'] = hovertext
    # End if

    # Create a layer for each region colored by LEP value
    layers = [{
        'name': overlay_choice,
        'source': json.loads(dataset.loc[dataset.index == i, :].to_json()),
        'sourcetype': 'geojson',
        'type': 'fill',
        'opacity': 0.7,
        'color': colors[i]
    } for i in dataset.index]

    tmp['layout']['mapbox']['layers'] = layers

    return tmp
# End update_map()



if __name__ == "__main__":
    app.run_server()
"""
connection.close()
cursor.close()"""
