import os
import dash
from dash import html, dcc, ctx, Dash
from dash.dependencies import Output, Input
import pandas as pd
import dash_daq as daq
from .intensity_plotter.DirectoryReplay import DirectoryReplay
from pathlib import Path


data_directory = Path("data/source") # .dat files directory
directory_replay = DirectoryReplay(data_directory, number_of_curves=10)
#datafiles = sorted(os.listdir(data_directory))

app = Dash(__name__, external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML" ])

app.layout = html.Div(
    [
        dcc.Graph(id='live-graph',
                  style={'height':'80vh', 'width':'100vw', },), #xaxis_title = r'$\sqrt{(n^2(t|T_))}$'
        
        dcc.Interval(
            id='graph-update',
            interval=1000,
            n_intervals=0
        ),
        # html.Button('Stop', id='stop-button', n_clicks=0),
        # html.Button('Start', id='start-button', n_clicks=0),
        daq.BooleanSwitch(
        id='update-switch',
        on=False,
        label="Pause to adjust",
        labelPosition="top"
        ),
        # html.Div(children=[html.Div([
        # html.Label(['Select Scale']), #style={'font-weight': 'bold', "text-align": "right","offset":1}
        
        # ])]),
        html.P("Scale"),
        dcc.Dropdown(
            ['log', 'linear'],
            'linear', 
            id='scale-dropdown'),
        html.P("Perspective"),
        dcc.Dropdown(
            ['perspective', 'orthographic'],
            'perspective', 
            id='perspective-dropdown'),
        html.P("Graph style"),
        dcc.Dropdown(
            ['lines', 'markers', 'lines+markers', 'text'],
            'lines', 
            id='style-dropdown'),
        html.P("Number of curves"),
        dcc.Slider(id='slider_num_curves', min=1, max=100, step=10, value=30,
                marks={x: str(x) for x in list(range(0,100,5))}),
        html.P("Interval"),
        dcc.Slider(id='slider_interval', min=100, max=2000, step=200, value=1000,
                marks={x: str(x) for x in list(range(0,2000,200))}),
    ],
        
)

@app.callback(
    Output('graph-update', "interval"),
    [Input('slider_interval', "value")]
)
def update_interval(value):
    return value    


@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')],
              #Input('start-button', 'n_clicks'),
              #Input('stop-button', 'n_clicks'))
              Input('update-switch', 'on'),
              Input('scale-dropdown', 'value'),
              Input('slider_num_curves', 'value'),
            Input('perspective-dropdown', 'value'),
            Input('style-dropdown', 'value')
            )
def update_graph_scatter(n_intervals, boolean_switch, scale, number_of_curves, perspective, style):
    if (n_intervals is None) or boolean_switch:
        return dash.no_update
    
    
    data_dataframe = pd.DataFrame(columns=["I", "q", "t"])
    data_slice = datafiles[n_intervals:number_of_curves+n_intervals]
    data_slice = [next(directory_replay) for i in number_of_curves]
    for i, datafile in enumerate(data_slice):
        if datafile.endswith(".dat"):
            datafile_path = os.path.join(data_directory, datafile)
            new_curve = get_trace(datafile_path, time=i)
            data_dataframe = data_dataframe.append(new_curve, ignore_index=True)
    
    X = data_dataframe['I']
    Y = data_dataframe['t']
    Z = data_dataframe['q']
    
    # scatter
    
    df = pd.DataFrame({'x': X, 'y': Y, 'z': Z})
    #fig = px.scatter_3d(df, x='x', y='y', z='z')
    # scatter = go.Scatter3d(x=df["x"], y=df["y"], z=df["z"])
    # layout=go.Layout(
    #     scene=dict(
    #         xaxis=dict(type=scale),
    #         yaxis=dict(type=scale),
    #         zaxis=dict(type=scale)
    #         ),
    #     uirevision=42) 
    # fig = go.Figure(data=scatter, layout=layout)
    fig = figure_function(X, Y, Z, scale=scale, perspective=perspective, graph_style=style)
    #fig.update(layout=go.Layout(uirevision=42))
    #print(fig.camera_eye)
    return fig

app.run_server(port=8051)