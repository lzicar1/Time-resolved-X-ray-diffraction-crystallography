from dataclasses import dataclass
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.graph_objects as go


@dataclass
class InititalizePlotter:
    """_summary_
    Initializer Dataclass (refer to https://docs.python.org/3/library/dataclasses.html)
    Set up directory path and data processing parameters
    """

    drop_first: int = 10
    drop_last: int = 10
    cut_values_below: int = 0.75

    def getCurve(self, datafile, time=0):
        # read data from single .dat file
        data = np.loadtxt(datafile)
        y_data = data[:, 1][data[:, 1] > self.cut_values_below][
            self.drop_last : -self.drop_first
        ]
        x_data = data[:, 0][data[:, 1] > self.cut_values_below][
            self.drop_last : -self.drop_first
        ]
        y_data[-1] = None
        x_data[-1] = None

        new_curve = pd.DataFrame.from_dict(
            {"I": x_data, "q": y_data, "t": [time] * (len(x_data))}
        )

        return new_curve

    def getFigure(self,
        data_x,
        data_y,
        data_z,
        aspect_x=2,
        aspect_y=5,
        aspect_z=1,
        scale="linear",
        perspective="perspective",
        graph_style="lines",
    ):
        data = go.Scatter3d(
            x=data_x,
            y=data_y,
            z=data_z,
            mode=graph_style,
            marker=dict(
                color=data_z,
                size=1.5,
            ),
            line=dict(
                color=data_z,
            ),
        )

        layout = go.Layout(
            title=r"Real-Time X-Ray Intensity Plot", 
            uirevision=True,
            autosize=False,
            scene=dict(
                camera_projection_type=perspective,
                xaxis=dict(
                    title="q_A^-1",
                    backgroundcolor="rgb(200, 200, 230)",
                    gridcolor="white",
                    showbackground=True,
                    dtick=0.5,
                    type=scale,
                ),
                yaxis=dict(
                    title="t",
                    backgroundcolor="rgb(230, 200,230)",
                    gridcolor="white",
                    showbackground=True,
                    autorange=True,
                    dtick=10,
                    type=scale,
                ),
                zaxis=dict(
                    title="I",
                    backgroundcolor="rgb(230, 230,200)",
                    gridcolor="white",
                    showbackground=True,
                    dtick=0.5,
                    type=scale,
                ),
                aspectmode="manual",  # data
                aspectratio=dict(x=aspect_x, y=aspect_y, z=aspect_z),
                xaxis_autorange="reversed",
            ),
        )
        fig = go.Figure(data=data, layout=layout)
        fig.update_traces(connectgaps=False)

        return fig
