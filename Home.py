##import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import GROSS_ALL_TERRITORY, GROSS_ALL , swap, EM_Purchasse, EM_INJECTE,freelancer,freelancerCentre,wallet,POA,KIOSQUE,Boutique
from app import app


app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
         return GROSS_ALL.layout     
    elif pathname == '/GROSS_ALL_TERRITORY':
         return GROSS_ALL_TERRITORY.layout
    elif pathname == '/swap':
         return swap.layout
    elif pathname == '/EM_Purchasse':
         return EM_Purchasse.layout
    elif pathname == '/EM_INJECTE':
         return EM_INJECTE.layout
    elif pathname == '/freelancer':
         return freelancer.layout
    elif pathname == '/freelancerCentre':
         return freelancerCentre.layout
    elif pathname == '/wallet':
         return wallet.layout
    elif pathname == '/POA':
         return POA.layout
    elif pathname == '/KIOSQUE':
         return KIOSQUE.layout
    elif pathname == '/Boutique':
         return Boutique.layout
    else :
         return GROSS_ALL.layout
if __name__ == '__main__':
    app.run_server(debug=False,host='10.0.104.25', port = 8051)


