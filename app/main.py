import dash
from dash import html,dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
from PIL import Image 
from util.metrics import Metrics
from util.data import HelpScoutMethods


######## Metrics ###########
source= HelpScoutMethods('2023-09-20','2023-10-09')
data=source.conversations()
tags=source.tags()

metrics= Metrics()
active_count,pending_count,closed_count = metrics.search_status(data)

tag_names = [list(tag.keys())[0] for tag in tags]
tag_counts = [list(tag.values())[0] for tag in tags]


## reading the dataset 
pd_2 = pd.read_csv('https://raw.githubusercontent.com/Anmol3015/Plotly_Dash_examples/main/retail_sales.csv', sep=',')
pd_2['Date'] = pd.to_datetime(pd_2['Date'], format='%Y-%m-%d')


################################ total sales Month level  ###################################
monthly_sales_df = pd_2.groupby(['month','Month']).agg({'Weekly_Sales':'sum'}).reset_index()


################################ holiday sales month lvl #####################################
holiday_sales = pd_2[pd_2['IsHoliday'] == 1].groupby(['month'])['Weekly_Sales'].sum().reset_index().rename(columns={'Weekly_Sales':'Holiday_Sales'})

############################# combined #########################
monthly_sales_df  = pd.merge(holiday_sales,monthly_sales_df,on = 'month', how = 'right').fillna(0)
 
############################## rounding sales to 1 decimal #############################
monthly_sales_df['Weekly_Sales'] = monthly_sales_df['Weekly_Sales'].round(1)
monthly_sales_df['Holiday_Sales'] = monthly_sales_df['Holiday_Sales'].round(1)


###################### weekly sales #########################
weekly_sale = pd_2.groupby(['month','Month','Date']).agg({'Weekly_Sales':'sum'}).reset_index()
weekly_sale['week_no'] = weekly_sale.groupby(['Month'])['Date'].rank(method='min')


########################### store level sales #######################
store_df=pd_2.groupby(['month','Month','Store']).agg({'Weekly_Sales':'sum'}).reset_index()
store_df['Store'] = store_df['Store'].apply(lambda x: 'Store'+" "+str(x))
store_df['Weekly_Sales'] = store_df['Weekly_Sales'].round(1)


######################## dept level sales #########################
dept_df=pd_2.groupby(['month','Month','Dept']).agg({'Weekly_Sales':'sum'}).reset_index()
dept_df['Dept'] = dept_df['Dept'].apply(lambda x: 'Dept'+" "+str(x))
dept_df['Weekly_Sales'] = dept_df['Weekly_Sales'].round(1)

#########################################


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])

PLOTLY_LOGO = Image.open('util/logo.png')


navbar = dbc.Navbar(id='navbar', children=[
    dbc.Row([
        dbc.Col(html.Img(src=PLOTLY_LOGO)),
        dbc.Col(
            dbc.NavbarBrand("Customer Support Dashboard", style={'color': 'white', 'fontSize': '25px'})
        ),
        dbc.Col([
            html.Div("From", style={'color': 'white', 'padding-right': '10px'}),
            dcc.Dropdown(id='dropdown_base', style={'height': '30px', 'width': '100px'},
                                 options=[
                                     {'label': i, 'value': i} for i in monthly_sales_df.sort_values('month')['Month']

                                 ],
                                 value='Feb',

                                 ),
            html.Div("To", style={'color': 'white', 'padding-left': '10px', 'padding-right': '10px'}),
                                dcc.Dropdown(id='dropdown_comp',style={'height': '30px', 'width': '100px'},
                                 options=[
                                     {'label': i, 'value': i} for i in monthly_sales_df.sort_values('month')['Month']

                                 ],
                                 value='Jan',

                                 ),
        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'flex-start'})
    ], align="center"),
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


app.layout = html.Div(id = 'parent', children = [navbar,body_app])


@app.callback([Output('card_num1', 'children'),
               Output('card_num2', 'children'),
               Output('card_num3', 'children'),
               Output('card_num4', 'children'),
               Output('card_num5', 'children'),
               Output('card_num6', 'children'),
               ],
              [Input('dropdown_base','value'), 
                Input('dropdown_comp','value')])
def update_cards(base, comparison):
    
    sales_base = monthly_sales_df.loc[monthly_sales_df['Month']==base].reset_index()['Weekly_Sales'][0]
    sales_comp = monthly_sales_df.loc[monthly_sales_df['Month']==comparison].reset_index()['Weekly_Sales'][0]

    diff_1 = np.round(sales_base -sales_comp,1)
    
    holi_base = monthly_sales_df.loc[monthly_sales_df['Month']==base].reset_index()['Holiday_Sales'][0]
    holi_comp = monthly_sales_df.loc[monthly_sales_df['Month']==comparison].reset_index()['Holiday_Sales'][0]

    diff_holi = np.round(holi_base -holi_comp,1)
    
    
    base_st_ct = pd_2.loc[pd_2['Month']==base,'Store'].drop_duplicates().count()
    comp_st_ct = pd_2.loc[pd_2['Month']==comparison,'Store'].drop_duplicates().count()

    diff_store = np.round(base_st_ct-comp_st_ct,1)
    
    
    weekly_base = weekly_sale.loc[weekly_sale['Month']==base].reset_index()
    weekly_comp = weekly_sale.loc[weekly_sale['Month']==comparison].reset_index()
    
    
    
    store_base = store_df.loc[store_df['Month']==base].sort_values('Weekly_Sales',ascending = False).reset_index()[:10]
    store_comp = store_df.loc[store_df['Month']==comparison].sort_values('Weekly_Sales',ascending = False).reset_index()[:10]
    
    dept_base = dept_df.loc[dept_df['Month']==base].sort_values('Weekly_Sales',ascending = False).reset_index()[:10]
    dept_base=dept_base.rename(columns = {'Weekly_Sales':'Weekly_Sales_base'})
    dept_comp = dept_df.loc[dept_df['Month']==comparison].sort_values('Weekly_Sales',ascending = False).reset_index()
    dept_comp=dept_comp.rename(columns = {'Weekly_Sales':'Weekly_Sales_comp'})
    
    merged_df=pd.merge(dept_base, dept_comp, on = 'Dept', how = 'left')
    merged_df['diff'] = merged_df['Weekly_Sales_base']-merged_df['Weekly_Sales_comp']


    
    fig = go.Figure(data = [go.Scatter(x = weekly_base['week_no'], y = weekly_base['Weekly_Sales'],\
                                   line = dict(color = 'firebrick', width = 4),name = '{}'.format(base)),
                        go.Scatter(x = weekly_comp['week_no'], y = weekly_comp['Weekly_Sales'],\
                                   line = dict(color = '#090059', width = 4),name = '{}'.format(comparison))])

    
    fig.update_layout(plot_bgcolor = 'white',
                      margin=dict(l = 40, r = 5, t = 60, b = 40),
                      yaxis_tickprefix = '$',
                      yaxis_ticksuffix = 'M')


    fig2 = go.Figure([go.Bar(x=tag_counts,y=tag_names, marker_color = 'indianred',\
                             text = tag_counts, orientation = 'h',
                             textposition = 'outside'
                             ),
                 ])
        
        
    fig3 = go.Figure([go.Bar(x = store_comp['Weekly_Sales'], y = store_comp['Store'], marker_color = '#4863A0',name = '{}'.format(comparison),\
                             text = store_comp['Weekly_Sales'], orientation = 'h',
                             textposition = 'outside'
                             ),
                 ])
        
    fig2.update_layout(plot_bgcolor = 'white',
                      xaxis=dict(range=[0, max(tag_counts) + 3]),
                      margin=dict(l = 40, r = 5, t = 60, b = 40),
                      xaxis_tickprefix = '',
                      xaxis_ticksuffix = '',
                      title = '',
                      title_x = 0.5)
    
    fig3.update_layout(plot_bgcolor = 'white',
                       xaxis = dict(range = [0,'{}'.format(store_comp['Weekly_Sales'].max()+3)]),
                      margin=dict(l = 40, r = 5, t = 60, b = 40),
                      xaxis_tickprefix = '$',
                      xaxis_ticksuffix = 'M',
                      title = '{}'.format(comparison),
                      title_x = 0.5)

    fig4 = go.Figure([go.Bar(x = merged_df['diff'], y = merged_df['Dept'], marker_color = '#4863A0',\
                              orientation = 'h',
                             textposition = 'outside'
                             ),
                 ])
        
    fig4.update_layout(plot_bgcolor = 'white',
                       margin=dict(l = 40, r = 5, t = 60, b = 40),
                      xaxis_tickprefix = '$',
                      xaxis_ticksuffix = 'M'
                     )


    
    if diff_1 >= 0:
        a =   dcc.Markdown( dangerously_allow_html = True,
                   children = ["<sub>+{0}{1}{2}</sub>".format('$',diff_1,'M')], style = {'textAlign':'center'})
        
    elif diff_1 < 0:
        
        a =    dcc.Markdown( dangerously_allow_html = True,
                   children = ["<sub>-{0}{1}{2}</sub>".format('$',np.abs(diff_1),'M')], style = {'textAlign':'center'})
            
    if diff_holi >= 0:
        b =   dcc.Markdown( dangerously_allow_html = True,
                   children = ["<sub>+{0}{1}{2}</sub>".format('$',diff_holi,'M')], style = {'textAlign':'center'})
        
    elif diff_holi < 0:
        
        b =   dcc.Markdown( dangerously_allow_html = True,
                   children = ["<sub>-{0}{1}{2}</sub>".format('$',np.abs(diff_holi),'M')], style = {'textAlign':'center'})
        
    if diff_store >= 0:
        c =   dcc.Markdown( dangerously_allow_html = True,
                   children = ["<sub>+{0}</sub>".format(diff_store)], style = {'textAlign':'center'})
        
    elif diff_store < 0:
        
        c =   dcc.Markdown( dangerously_allow_html = True,
                   children = ["<sub>-{0}</sub>".format(np.abs(diff_store))], style = {'textAlign':'center'})
        
        
    
    card_content = [
        
        dbc.CardBody(
            [
                html.H6('Card 0', style = {'fontWeight':'lighter', 'textAlign':'center'}),
                
                html.H3('{0}{1}{2}'.format("$", sales_base, "M"), style = {'color':'#090059','textAlign':'center'}),
                
                a
                
                ]
                   
            )  
        ]
    
    card_content1 = [
        
        dbc.CardBody(
            [
                html.H6(' Card 1 ', style = {'fontWeight':'lighter', 'textAlign':'center'}),
                
                html.H3('{0}{1}{2}'.format("$", holi_base, "M"), style = {'color':'#090059','textAlign':'center'}),
                
                b
                
                ]
                   
            )  
        ]
    
    card_content2 = [
        
        dbc.CardBody(
            [
                html.H6(' Card 2 ', style = {'fontWeight':'lighter', 'textAlign':'center'}),
                
                html.H3('{0}'.format( base_st_ct), style = {'color':'#090059','textAlign':'center'}),
                
                c
                
                ]
                   
            )  
        ]
    
    card_content3 = [
        
        dbc.CardBody(
            [
                html.H6(' Card 3 ', style = {'fontWeight':'bold', 'textAlign':'center'}),
                
                dcc.Graph(figure = fig, style = {'height':'250px'})
                
                
                ]
                   
            )  
        ]
    
    
    card_content4 = [
        
        dbc.CardBody(
            [
                html.H6('Tags', style = {'fontWeight':'bold', 'textAlign':'center'}),
                
                dbc.Row([
                    dbc.Col([dcc.Graph(figure = fig2, style = {'height':'300px'}),
                ])
                    ])
                
                
                
                ]
                   
            )  
        ]
    
    card_content5 = [
        
        dbc.CardBody(
            [
                html.H6(' Card 4  ({} - {})'.format(base, comparison), style = {'fontWeight':'bold', 'textAlign':'center'}),
                
                dcc.Graph(figure = fig4, style = {'height':'300px'})
                
                
                ]
                   
            )  
        ]
    

    
    return card_content, card_content1, card_content2,card_content3,card_content4,card_content5


if __name__ == "__main__":
    app.run_server()
    #debug = True

