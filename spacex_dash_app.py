# Import required libraries
import pandas as pd
import dash
# import dash_html_components as html
# import dash_core_components as dcc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Build launch site dropdown list
sites = spacex_df['Launch Site'].unique()
site_dicts = [{'label': 'All', 'value': 'ALL'}]
for site in sites:
    site_dicts.append({'label': site, 'value': site})

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=site_dicts,
                                             value='ALL',
                                             placeholder='Select a Launch Site here',
                                             searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                       2500: '2500',
                                                       5000: '5000',
                                                       7500: '7500',
                                                       10000: '10000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class',
                     names='Launch Site',
                     title='Total Success Launches by Site')
    else:
        # return the outcomes pie chart for a selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        successes = filtered_df['class'].sum()
        failures = filtered_df['class'].count() - successes

        fig = px.pie(filtered_df, values=[successes, failures],
                     names=['1', '0'],
                     title='Total Success Launches for site ' + entered_site)
    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')]
              )
def get_scatter_chart(entered_site, payload_range):
    # filter on selected range of payloads
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload_range[0],
                                                                   payload_range[1])]
    if entered_site == 'ALL':
        fig_scatter = px.scatter(filtered_df,
                                 x='Payload Mass (kg)',
                                 y='class',
                                 color="Booster Version Category",
                                 title="Correlation between Payload and Success for all Sites")
    else:
        # filter for site selected
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig_scatter = px.scatter(filtered_df,
                                 x='Payload Mass (kg)',
                                 y='class',
                                 color="Booster Version Category",
                                 title='Correlation between Payload and Success for ' + entered_site + ' site')
    return fig_scatter


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
