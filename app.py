import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# File paths
solartech_file = 'data/SolarTech/ST_data.csv'
pv_file = 'data/PV/PV_data.csv'

# Read SolarTech data
try:
    solartech_df = pd.read_csv(solartech_file, sep=';')
    solartech_df['DateTime'] = pd.to_datetime(solartech_df['date'] + ' ' + solartech_df['time'], format='%d/%m/%Y %H:%M:%S')
except Exception as e:
    print(f"An error occurred while reading {solartech_file}: {e}")

# Read PV data
try:
    pv_df = pd.read_csv(pv_file, sep=';')
    pv_df['DateTime'] = pd.to_datetime(pv_df['date'] + ' ' + pv_df['time'], format='%d/%m/%Y %H:%M:%S')
except Exception as e:
    print(f"An error occurred while reading {pv_file}: {e}")

# Create the Dash application
app = Dash(__name__)
server = app.server

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='SolarTech', children=[
            html.Div([
                html.H3('SolarTech Data'),
                
                # Date range picker
                dcc.DatePickerRange(
                    id='solartech-date-picker',
                    min_date_allowed=solartech_df['DateTime'].min().date(),
                    max_date_allowed=solartech_df['DateTime'].max().date(),
                    initial_visible_month=solartech_df['DateTime'].max().date(),
                    start_date=solartech_df['DateTime'].min().date(),
                    end_date=solartech_df['DateTime'].max().date()
                ),

                # Start time input
                dcc.Input(id='solartech-start-time', type='text', value='00:00', placeholder='HH:MM'),
                html.Label('Start Time'),

                # End time input
                dcc.Input(id='solartech-end-time', type='text', value='23:59', placeholder='HH:MM'),
                html.Label('End Time'),

                # Graph 1
                dcc.Graph(id='solartech-graph1'),
                
                # Graph 2
                dcc.Graph(id='solartech-graph2'),
                
                # Graph 3
                dcc.Graph(id='solartech-graph3'),
            ])
        ]),
        dcc.Tab(label='PV', children=[
            html.Div([
                html.H3('PV Data'),
                
                # Date range picker
                dcc.DatePickerRange(
                    id='pv-date-picker',
                    min_date_allowed=pv_df['DateTime'].min().date(),
                    max_date_allowed=pv_df['DateTime'].max().date(),
                    initial_visible_month=pv_df['DateTime'].max().date(),
                    start_date=pv_df['DateTime'].min().date(),
                    end_date=pv_df['DateTime'].max().date()
                ),

                # Start time input
                dcc.Input(id='pv-start-time', type='text', value='00:00', placeholder='HH:MM'),
                html.Label('Start Time'),

                # End time input
                dcc.Input(id='pv-end-time', type='text', value='23:59', placeholder='HH:MM'),
                html.Label('End Time'),

                # Graph 1: Produção Solar
                dcc.Graph(id='pv-graph1'),
            ])
        ])
    ])
])

# Helper function to filter data based on date and time
def filter_data(df, start_date, end_date, start_time, end_time):
    try:
        # Combine date and time into datetime objects
        start_datetime = pd.to_datetime(f"{start_date} {start_time}", format='%Y-%m-%d %H:%M')
        end_datetime = pd.to_datetime(f"{end_date} {end_time}", format='%Y-%m-%d %H:%M')

        # Filter the dataframe
        filtered_df = df[(df['DateTime'] >= start_datetime) & (df['DateTime'] <= end_datetime)]
        return filtered_df
    except ValueError:
        print(f"Invalid date or time format: {start_date}, {start_time} - {end_date}, {end_time}")
        return df  # Return unfiltered DataFrame if there's an error

# Callbacks for SolarTech graphs
@app.callback(
    Output('solartech-graph1', 'figure'),
    [Input('solartech-date-picker', 'start_date'),
     Input('solartech-date-picker', 'end_date'),
     Input('solartech-start-time', 'value'),
     Input('solartech-end-time', 'value')]
)
def update_solartech_graph1(start_date, end_date, start_time, end_time):
    filtered_df = filter_data(solartech_df, start_date, end_date, start_time, end_time)
    figure = {
        "data": [
            {"x": filtered_df["DateTime"], "y": filtered_df["Tamb[C]"], "type": "line", "name": 'Tamb[C]'},
            {"x": filtered_df["DateTime"], "y": filtered_df["Tin_CampoSolar[C]"], "type": "line", "name": 'Tin_CampoSolar[C]'},
            {"x": filtered_df["DateTime"], "y": filtered_df["Tout_CampoSolar[C]"], "type": "line", "name": 'Tout_CampoSolar[C]'},
            {"x": filtered_df["DateTime"], "y": filtered_df["Caudal_CampoSolar[C]"], "type": "line", "name": 'Caudal_CampoSolar[C]'},
        ],
        "layout": {"title": 'SolarTech - Graph 1'}
    }
    return figure

@app.callback(
    Output('solartech-graph2', 'figure'),
    [Input('solartech-date-picker', 'start_date'),
     Input('solartech-date-picker', 'end_date'),
     Input('solartech-start-time', 'value'),
     Input('solartech-end-time', 'value')]
)
def update_solartech_graph2(start_date, end_date, start_time, end_time):
    filtered_df = filter_data(solartech_df, start_date, end_date, start_time, end_time)
    figure = {
        "data": [
            {"x": filtered_df["DateTime"], "y": filtered_df["Tamb[C]"], "type": "line", "name": 'Tamb[C]'},
            {"x": filtered_df["DateTime"], "y": filtered_df["Tin_Armazenamento[C]"], "type": "line", "name": 'Tin_Armazenamento[C]'},
            {"x": filtered_df["DateTime"], "y": filtered_df["Tout_Armazenamento[C]"], "type": "line", "name": 'Tout_Armazenamento[C]'},
            {"x": filtered_df["DateTime"], "y": filtered_df["Caudal_Armazenamento[C]"], "type": "line", "name": 'Caudal_Armazenamento[C]'},
        ],
        "layout": {"title": 'SolarTech - Graph 2'}
    }
    return figure

@app.callback(
    Output('solartech-graph3', 'figure'),
    [Input('solartech-date-picker', 'start_date'),
     Input('solartech-date-picker', 'end_date'),
     Input('solartech-start-time', 'value'),
     Input('solartech-end-time', 'value')]
)
def update_solartech_graph3(start_date, end_date, start_time, end_time):
    filtered_df = filter_data(solartech_df, start_date, end_date, start_time, end_time)
    figure = {
        "data": [
            {"x": filtered_df["DateTime"], "y": filtered_df["Potência_Campo_Solar[kWth]"], "type": "line", "name": 'Potência_Campo_Solar[kWth]'},
            {"x": filtered_df["DateTime"], "y": filtered_df["Potência_Armazenamento[kWth]"], "type": "line", "name": 'Potência_Armazenamento[kWth]'},
            {"x": filtered_df["DateTime"], "y": filtered_df["Radiação_DNI[W/m2]"], "type": "line", "name": 'Radiação_DNI[W/m2]'},
            {"x": filtered_df["DateTime"], "y": filtered_df["Radiação_Global[W/m2]"], "type": "line", "name": 'Radiação_Global[W/m2]'},
        ],
        "layout": {"title": 'SolarTech - Graph 3'}
    }
    return figure

# Callbacks for PV graph
@app.callback(
    Output('pv-graph1', 'figure'),
    [Input('pv-date-picker', 'start_date'),
     Input('pv-date-picker', 'end_date'),
     Input('pv-start-time', 'value'),
     Input('pv-end-time', 'value')]
)
def update_pv_graph1(start_date, end_date, start_time, end_time):
    filtered_df = filter_data(pv_df, start_date, end_date, start_time, end_time)
    figure = {
        "data": [
            {"x": filtered_df["DateTime"], "y": filtered_df["P_Tracker1"], "type": "line", "name": 'P_Tracker1'},
            {"x": filtered_df["DateTime"], "y": filtered_df["P_Tracker2"], "type": "line", "name": 'P_Tracker2'},
            {"x": filtered_df["DateTime"], "y": filtered_df["P_Tracker3"], "type": "line", "name": 'P_Tracker3'},
            {"x": filtered_df["DateTime"], "y": filtered_df["P_Tracker4"], "type": "line", "name": 'P_Tracker4'},
            {"x": filtered_df["DateTime"], "y": filtered_df["Ptotal"], "type": "line", "name": 'Ptotal'},
        ],
        "layout": {"title": 'Produção Solar'}
    }
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
