import os
import dash
from dash import html, dcc, ctx, Dash
from dash.dependencies import Output, Input
import pandas as pd
import dash_daq as daq
from intensity_plotter.DirectoryReplay import DirectoryReplay
from intensity_plotter.InitializePlotter import InititalizePlotter
from pathlib import Path

### Initialization ###

data_directory = r"data/source" # .dat files directory
file_prefix = r"C5_mesh_1_data.cbf" #prefix of .dat files (the rest is the number)
plotter = InititalizePlotter(drop_first = 5, 
                             drop_last = 5, 
                             cut_values_below = 0) # initialize plotter
directory_replay = DirectoryReplay(data_directory)

def getFileNumber(file_path, file_prefix):
    """_summary_
    Example:
    file_path = r"data/source/C5_mesh_1_data.cbf000110.dat"
    file_prefix = r"C5_mesh_1_data.cbf"
    number = 110
    """
    string = file_path.split(file_prefix)[1]
    number = int(string.split('.dat')[0])
    return number
    
    

### Dash App ###

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
        
        html.P("Aspect ratio X"),
        dcc.Slider(id='aspect_x', min=1, max=10, step=1, value=2,
                marks={x: str(x) for x in list(range(0,10,1))}),
        html.P("Aspect ratio Y"),
        dcc.Slider(id='aspect_y', min=1, max=10, step=1, value=5,
                marks={x: str(x) for x in list(range(0,10,1))}),
        html.P("Aspect ratio Z"),
        dcc.Slider(id='aspect_z', min=1, max=10, step=1, value=1,
                marks={x: str(x) for x in list(range(0,10,1))}),
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
              Input('aspect_x', 'value'),
              Input('aspect_y', 'value'),
              Input('aspect_z', 'value'),
            Input('perspective-dropdown', 'value'),
            Input('style-dropdown', 'value')
            )
def update_graph_scatter(n_intervals, boolean_switch, scale, number_of_curves, aspect_x, aspect_y, aspect_z, perspective, style):
    # if (n_intervals is None) or boolean_switch:
    #     return dash.no_update
    
    
    data_dataframe = pd.DataFrame(columns=["I", "q", "t"])
    data_slice = next(directory_replay.fetchDataLoop(number_of_curves=number_of_curves, instantly=True))
    
    for i, datafile in enumerate(data_slice):
        if datafile.endswith(".dat"):
            file_number = getFileNumber(datafile, file_prefix)
            new_curve = plotter.getCurve(datafile, time=file_number)
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
    fig = plotter.getFigure(X,
                            Y, 
                            Z,
                            aspect_x,
                            aspect_y,
                            aspect_z, 
                            scale=scale, 
                            perspective=perspective, 
                            graph_style=style)
    #fig.update(layout=go.Layout(uirevision=42))
    #print(fig.camera_eye)
    return fig

app.run_server(port=8052)