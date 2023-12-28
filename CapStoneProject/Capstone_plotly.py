# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
launch_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
spacex_df = pd.read_csv(launch_url)
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
for c in spacex_df.columns:
    print(c)
print(spacex_df["class"].unique())
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
            dcc.Dropdown(id='site-dropdown',
                                 options=[
                                     {'label': 'All Sites', 'value': 'All Sites'},
                                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                 ],
                                 value='All',
                                 placeholder='Select Launch Site',
                                 searchable=True),
                                html.Br(),
            dcc.RangeSlider(id='payload-slider',
                            min=min_payload,
                            max=max_payload,
                            step=1000,
                            value=[min_payload, max_payload]),
            html.Div([
                html.Div(id='out-container',
                         className='chart-grid',
                         style={'display': 'flex'})
            ])
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='out-container', component_property='children'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')])


def update_output_container(selected_value, selected_payload):

    #change input df according to selection
    if selected_value == 'All Sites':
        # Filter the data for recession periods
        data=spacex_df
    else:
        data = spacex_df[spacex_df['Launch Site'] == selected_value]

    #filter by slider
    data = data[(data['Payload Mass (kg)']>= selected_payload[0])
                & (data['Payload Mass (kg)'] <= selected_payload[1])]

    chart1 = dcc.Graph(
    figure = px.pie(data_frame=data,
                 names='class',
                 title='Launch Site Success Rate'))

    chart2 = dcc.Graph(
        figure = px.scatter(data_frame=data,
                         x='class',
                         y='Payload Mass (kg)',
                         title='Payload Mass vs Success Rate'))

    return [html.Div(className='chart-item', children=[html.Div(children=chart1), html.Div(children=chart2)])
            ]

if __name__ == '__main__':
    app.run_server(debug=True, port=8501)
