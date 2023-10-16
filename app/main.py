import dash
from dash import html,dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
from PIL import Image 
from datetime import datetime
from util.metrics import Metrics
from util.data import HelpScoutMethods


######## Metrics ###########
current_date = datetime.now()

start='2023-10-01'
end='2023-10-14'

start_date = datetime.strptime(start+ 'T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
end_date = datetime.strptime(end+ 'T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ')

source= HelpScoutMethods('2023-10-01','2023-10-14')
metrics= Metrics()

data=source.conversations()
tags=source.tags()


################################  E-Mail Status  ###################################
active_count,pending_count,closed_count = metrics.search_status(data)

################################    Tags     ###################################
tag_names = [list(tag.keys())[0] for tag in tags]
tag_counts = [list(tag.values())[0] for tag in tags]

################################   Incoming E-Mails    ###################################
incoming=metrics.incoming_mails(data,start_date,end_date)
dates, counts = zip(*incoming)

## reading the dataset 
pd_2 = pd.read_csv('https://raw.githubusercontent.com/Anmol3015/Plotly_Dash_examples/main/retail_sales.csv', sep=',')
pd_2['Date'] = pd.to_datetime(pd_2['Date'], format='%Y-%m-%d')

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']




app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])

PLOTLY_LOGO = Image.open('assets/logo.png')


navbar = dbc.Navbar(id='navbar', children=[
    dbc.Row([
        
        dbc.Col(html.Img(src=PLOTLY_LOGO), width={"order": 'first',"size": 3}),
        
        dbc.Col(dbc.NavbarBrand("Support Dashboard", style={'color': 'white', 'fontSize': '25px'}), width={"order": 2,"size": 3}),
        
        dbc.Col([
            html.Div("From", style={'color': 'white', 'padding-right': '10px'}),

            dcc.Dropdown(id='dropdown_base', style={'height': '30px', 'width': '100px'},
                         
                                 options=[{'label': i, 'value': i} for i in months],

                                 value='Feb',

                                 ),
            html.Div("To", style={'color': 'white', 'padding-left': '10px', 'padding-right': '10px'}),
            dcc.Dropdown(id='dropdown_comp',style={'height': '30px', 'width': '100px'},
                                 
                                 options=[{'label': i, 'value': i} for i in months],
                                 
                                 value='Jan',
                                 
                                 ),
        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'flex-start'},
           width={"size": 3,"order": "last", "offset": 3})
    ]),
], color='#32333d', )


card_content_status = [
    dbc.CardBody(
        [
            html.H6('Email Status', style = {'fontWeight':'lighter', 'textAlign':'center', 'fontSize': '18px'}),

            dbc.Row([
                dbc.Col([
                    html.H6('Active', style={'color':'#090059', 'fontWeight':'lighter', 'textAlign': 'center', 'fontSize': '16px'}),
                    html.H3(active_count, style={'color':'#090059', 'textAlign': 'center'}),
                ], width=4),

                dbc.Col([
                    html.H6('Pending', style={'fontWeight':'lighter', 'textAlign': 'center', 'fontSize': '16px'}),
                    html.H3(pending_count, style={'color':'#090059', 'textAlign': 'center'}),
                ], width=4),

                dbc.Col([
                    html.H6('Closed', style={'color':'#090059','fontWeight':'lighter','textAlign': 'center', 'fontSize': '16px'}),
                    html.H3(closed_count, style={'color':'#090059','textAlign': 'center'}),
                ], width=4),
            ])

        ]

    )

]


body_app = dbc.Container([
    
    html.Br(),
    html.Br(),
    
    dbc.Row([
        dbc.Col([dbc.Card(card_content_status,style={'height':'150px'})],width = 4),
        dbc.Col([dbc.Card(id = 'card_num1',style={'height':'150px'})]),
        dbc.Col([dbc.Card(id = 'card_num2',style={'height':'150px'})]),
        dbc.Col([dbc.Card(id = 'card_num3',style={'height':'150px'})]),

        ]),
    
    html.Br(),
    html.Br(),
    
    dbc.Row([
        dbc.Col([dbc.Card(id = 'card_num4',style={'height':'350px'})]),
        dbc.Col([dbc.Card(id = 'card_num5',style={'height':'350px'})]),
        dbc.Col([dbc.Card(id = 'card_num6',style={'height':'350px'})]),

        ]),
    
    html.Br(),
    html.Br()
    
    
    ], 
    style = {'backgroundColor':'#f7f7f7'},
    fluid = True)


app.layout = html.Div(id = 'parent', children = [navbar,body_app] )


@app.callback([Output('card_num1', 'children'),
               Output('card_num2', 'children'),
               Output('card_num3', 'children'),
               Output('card_num4', 'children'),
               Output('card_num5', 'children'),
               Output('card_num6', 'children'),
               ],
              [Input('dropdown_base','value'), 
                Input('dropdown_comp','value')])


def update_cards(start, end):

    
    fig = go.Figure([go.Scatter(x = dates, y = counts,\
                                 line = dict(color = '#090059'),
                                ),
                ])

    
    fig.update_layout(plot_bgcolor = 'white',
                      margin=dict(l = 40, r = 5, t = 60, b = 40),
                      yaxis_title = 'Count',
                      xaxis_title = 'Date')


    fig1 = go.Figure([go.Bar(x=tag_counts,y=tag_names, marker_color = 'firebrick',\
                             text = tag_counts, orientation = 'h',
                             textposition = 'outside'
                             ),
                 ])
        
        
        
    fig1.update_layout(plot_bgcolor = 'white',
                      xaxis=dict(range=[0, max(tag_counts) + 3]),
                      margin=dict(l = 40, r = 5, t = 60, b = 40),
                      xaxis_tickprefix = '',
                      xaxis_ticksuffix = '',
                      title = '',
                      title_x = 0.5)
    

    sample_x = [1, 2, 3, 4, 5]
    sample_y = ['A', 'B', 'C', 'D', 'E']

    fig2 = go.Figure([go.Bar(x = sample_x, y = sample_x , marker_color = '#4863A0',\
                              orientation = 'h',
                             textposition = 'outside'
                             ),
                 ])
        
    fig2.update_layout(plot_bgcolor = 'white',
                       margin=dict(l = 40, r = 5, t = 60, b = 40),
                      xaxis_tickprefix = '$',
                      xaxis_ticksuffix = 'M'
                     )



    
    card_content = [
        
        dbc.CardBody(
            [
                html.H6('Card 0', style = {'fontWeight':'lighter', 'textAlign':'center'}),
                
                html.H3('value', style = {'color':'#090059','textAlign':'center'}),
                
                
                
                ]
                   
            )  
        ]
    
    card_content1 = [
        
        dbc.CardBody(
            [
                html.H6(' Card 1 ', style = {'fontWeight':'lighter', 'textAlign':'center'}),
                
                html.H3('value', style = {'color':'#090059','textAlign':'center'}),
                
                
                ]
                   
            )  
        ]
    
    card_content2 = [
        
        dbc.CardBody(
            [
                html.H6(' Card 2 ', style = {'fontWeight':'lighter', 'textAlign':'center'}),
                
                html.H3('value', style = {'color':'#090059','textAlign':'center'}),
                
                
                ]
                   
            )  
        ]
    
    card_content3 = [
        
        dbc.CardBody(
            [
                html.H6(' Incoming Emails ', style = {'fontWeight':'lighter', 'textAlign':'center', 'fontSize': '18px'}),
                
                dcc.Graph(figure = fig, style = {'height':'250px'})
                
                
                ]
                   
            )  
        ]
    
    
    card_content4 = [
        
        dbc.CardBody(
            [
                html.H6('Tags', style = {'fontWeight':'lighter', 'textAlign':'center', 'fontSize': '18px'}),
                
                dbc.Row([
                    dbc.Col([dcc.Graph(figure = fig1, style = {'height':'300px'}),
                ])
                    ])
                
                
                
                ]
                   
            )  
        ]
    
    card_content5 = [
        
        dbc.CardBody(
            [
                html.H6(' Card 4 ', style = {'fontWeight':'bold', 'textAlign':'center'}),
                
                dcc.Graph(figure = fig2, style = {'height':'300px'})
                
                
                ]
                   
            )  
        ]
    

    
    return card_content, card_content1, card_content2,card_content3,card_content4,card_content5


if __name__ == "__main__":
    app.run_server()
    #debug = True

