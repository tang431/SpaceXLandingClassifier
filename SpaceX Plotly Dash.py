# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe

mark_values= {
    0:'0',
    1000:'1k',
    2000:'2k',
    3000:'3k',
    4000:'4k',
    5000:'5k',
    6000:'6k',
    7000:'7k',
    8000:'8k',
    9000:'9k',
    10000:'10k',
    11000:'11k',
    12000:'12k',
    13000:'13k',
    14000:'14k',
    15000:'15k',
    16000:'16k'
}
orbit_distances= { #looked up average distances for all orbit types for binning distance of orbit
    'GEO': 35785,
    'LEO':1999,
    'MEO':18893,
    'SSO':700,
    'VLEO':399,
    'GTO': 42165,
    'TLI':384400,
    'PO':750,
    'ISS':422,
    'HEO': 120000,
    'ES-L1':1500000,
    'SO':700
}

orbit_marks={
    0:'0',
    500:'500',
    1000:'1000',
    2000:'2000',
    10000:'10000',
    35786:'35786',
    100000:'100000',
    384401:'384401',
    1500001:'1500001',

}
orbit_marks={
    0:'0',
    50000:'50K',
    100000:'100K',
    150000:'150K',
    200000:'200K',
    250000:'250K',
    300000:'300K',
    350000:'350K',
    400000:'400K',
    450000:'450K',
    500000:'500K',

}


spacex_df = pd.read_csv(r"C:\Users\infop\OneDrive\Desktop\ML_lab screenshots\spacex_final_dataset.csv")
max_payload = spacex_df['PayloadMass'].max()
min_payload = spacex_df['PayloadMass'].min()

#map the orbits to a specific distance in order to bin up bar chart groups
#mapping = {'CCSFS SLC 40':'Cape Canaveral', 'KSC LC 39A':'Kennedy Space Center', 'VAFB SLC 4E': 'Vandenberg AF Base'}

spacex_df['OrbitDistance'] = spacex_df['Orbit'].map(orbit_distances)




# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Falcon 9 Landing Outcomes Interactive Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                
                                dcc.Dropdown(id='site-dropdown',
                                options=[
                                    {'label': 'All Sites', 'value': 'All Sites'},
                                    {'label': 'Vandenberg AF Base', 'value': 'Vandenberg AF Base'},
                                    {'label': 'Kennedy Space Center', 'value': 'Kennedy Space Center'},
                                    {'label': 'Cape Canaveral', 'value': 'Cape Canaveral'}
                                ],
                                placeholder='Select a Launch Site Here',
                                value='All Sites',
                                searchable=True
                                ),
                                html.Br(),

                            

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload-Mass Sample Range"),


                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Br(),
                                dcc.RangeSlider(id='payload-slider', min=0, max=16000, step=1000, value=[0, 16000], marks= mark_values),
                                #dcc.RangeSlider(id='payload-slider',
                                #min=0,
                                #max=17000,
                                #step=1700,
                                #marks={i: '{}'.format(i) for i in range(0, 17001, 1700)},
                                #value=[min_payload, max_payload]),


                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                
                                html.Div([dcc.Graph(id='success-payload-scatter-chart')])
                                
                                














                                
                            
                                ])
                            

@app.callback( Output(component_id='success-pie-chart', component_property='figure'),
               [Input(component_id='site-dropdown', component_property='value')])
def get_pie_chart(launch_site):
    if launch_site == 'All Sites':
        fig = px.pie(values=spacex_df.groupby('LaunchSite')['Class'].sum(), 
                     names=spacex_df.groupby('LaunchSite')['LaunchSite'].first(),
                     title='Share of Successful Booster Landings by Launch Site')
    else:
        fig = px.pie(values=spacex_df[spacex_df['LaunchSite']==str(launch_site)]['Class'].value_counts(), #normalize=True
                     names=spacex_df['Class'].unique(), 
                     title='Booster Landing Success Rate For Launches At {}'.format(launch_site))
    return(fig)




@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),
               [Input(component_id='payload-slider', component_property='value')]
               )
def get_payload_chart(payload_mass):

    df= spacex_df[(spacex_df['PayloadMass']>= payload_mass[0])&(spacex_df['PayloadMass']<= payload_mass[1])]
    df = df.groupby('Customer', as_index=False).agg(#Payload = ('Payload', 'mean'),
                                Payload_Count=('Payload', 'count'), 
                                Total_PayloadMass=('PayloadMass', 'sum'),
                                Landing_Success_Rate=('Class', 'mean'))
    #df= df.groupby(['PayloadMass'], as_index=False)['Customer','Class'].mean()
    #print(payload_mass) works fine
    #print(df.head())
    #filter the df again to group by the df slice provided by the rangeslider
    fig = px.scatter(df,
            x= 'Total_PayloadMass',                #plot payloadMass instead of Payload, use a payload hover data to denote payload name
            y= 'Landing_Success_Rate',  
            size= 'Payload_Count',              #return a grouped by summary operation like avg. instead of Class
            color= 'Payload_Count',             #still filter on PayloadMass
            hover_data=['Customer'],
            #text='Customer',
            title='Total PayloadMass By Customer Vs. Landing Success Rate for Launches with PayloadMass in range: {}'.format(payload_mass),
            height=550)
    return(fig)


# Run the app
if __name__ == '__main__':
    app.run_server()