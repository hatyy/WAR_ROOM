# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 09:59:48 2020

@author: sidyndiaye
"""




import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import GROSS_ALL_TERRITORY
from app import app
"""
app = dash.Dash()
server = app.server
"""
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
         return GROSS_ALL_TERRITORY.layout
   



graphs = [
    'http://127.0.0.1:8051'
]
from IPython.display import display, HTML

template = (''
    '<a href="{graph_url}" target="_blank">' # Open the interactive graph when you click on the image
        '<img src="{graph_url}.png">'        # Use the ".png" magic url so that the latest, most-up-to-date image is included
    '</a>'
    '{caption}'                              # Optional caption to include below the graph
    '<br>'                                   # Line break
    '<a href="{graph_url}" style="color: rgb(190,190,190); text-decoration: none; font-weight: 200;" target="_blank">'
        'Click to comment and see the interactive graph'  # Direct readers to Plotly for commenting, interactive graph
    '</a>'
    '<br>'
    '<hr>'                                   # horizontal line
'')

email_body = ''
for graph in graphs:
    _ = template
    _ = _.format(graph_url=graph, caption='')
    email_body += _

display(HTML(email_body))

me  = 'ahmedandiaye@gmail.com'
recipient = 'sidyndiaye@free.sn'
subject = 'Graph Report'

email_server_host = 'smtp.gmail.com'
port = 587
email_username = me
email_password = 'SIDYNDIAYE1'


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


msg = MIMEMultipart('alternative')
msg['From'] = me
msg['To'] = recipient
msg['Subject'] = subject

msg.attach(MIMEText(email_body, 'html'))

server = smtplib.SMTP(email_server_host, port)
server.ehlo()
server.starttls()
server.login(email_username, email_password)
server.sendmail(me, recipient, msg.as_string())
server.close()


if __name__ == '__main__':
    app.run_server(debug=False, port = 8051)
    




