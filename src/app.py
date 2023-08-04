import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np

# Define the app
app = dash.Dash(__name__)
server = app.server

A = np.array([[0, 0, 0],[1, 0, 0],[0.5, np.sqrt(3)/2, 0],[0.5, np.sqrt(3)/6, np.sqrt(2/3)]]) #A1, A2, A3, A4
# Define the edges of the tetrahedron
edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
resolution=25
T=np.linspace(A[0],A[1],resolution)
T_=np.linspace(A[2],A[3],resolution)
t=np.linspace(0,1,resolution)
tetrahedron=[go.Scatter3d(
                x=[0, 1, 0.5, 0.5],
                y=[0, 0, np.sqrt(3)/2, np.sqrt(3)/6],
                z=[0, 0, 0, np.sqrt(2/3)],
                mode='markers',    # Set mode to 'markers' to draw points
                marker=dict(
                    color='blue',   # Point color
                    size=5,         # Point size
                ),
                text=['A1','A2','A3','A4'] ,
                showlegend=False
            )]+[
                go.Scatter3d(
                    x=A[edge,0],
                    y=A[edge, 1],
                    z=A[edge, 2],
                    mode='lines',
                    line=dict(color='blue',width=3,dash='dash'),
                    showlegend=False
                ) for edge in edges
            ]

# Define the layout of the app
app.layout = html.Div([
    html.H1('Surface of independence of 2x2 table',style={'background-color': '#f2f2f2','text-align':'center'}),
    # dcc.Checklist(
    #     id='plot-checklis',
    #     options=[{'label': labs[idx], 'value': idx} for idx, file in enumerate(csv_files)],
    #     value=[],
    #     labelStyle={'display': 'block','background-color': '#f2f2f2'}
    # ),
    html.H3("Select Resolution:-",style={'background-color': '#f2f2f2','text-align':'center'}),
    dcc.Slider(
        id='resolution-slider',
        min=10,
        max=100,
        value=25,
        # marks={i:f'{i}' for i in range(11)}
    ),
    html.H3("Select Odd's Ratio:-",style={'background-color': '#f2f2f2','text-align':'center'}),
    dcc.Slider(
        id='odds-ratio-slider',
        min=0,
        max=100,
        value=1,
        # marks={i:f'{i}' for i in range(11)}
    ),
    dcc.Graph(
        id='surface-plot',
        figure={
            'data': tetrahedron+[ go.Scatter3d(
                    x=[T[t][0],T_[t][0]],
                    y=[T[t][1],T_[t][1]],
                    z=[T[t][2],T_[t][2]],
                    mode='lines',
                    line=dict(color='red',width=3,dash='solid'),
                    showlegend=False
                ) for t in range(resolution)
            ],
            
            'layout': go.Layout(
                scene=dict(
                    xaxis=dict(title='X'),
                    yaxis=dict(title='Y'),
                    zaxis=dict(title='Z'),
                ),
                title='Tetrahedron Plot'
            )
        },
        style={'height':'800px'}
    ),
])
@app.callback(
    dash.dependencies.Output('surface-plot', 'figure'),
    [dash.dependencies.Input('odds-ratio-slider', 'value'),
     dash.dependencies.Input('resolution-slider', 'value'),]
)
def update_surface(theta,res):
    t=np.linspace(0,1,res)
    t_=t/(t+theta*(1-t))
    T=A[0]*t[:,np.newaxis]+A[1]*(1-t[:,np.newaxis])
    T_=A[2]*t_[:,np.newaxis]+A[3]*(1-t_[:,np.newaxis])
    data = tetrahedron+[
        go.Scatter3d(
            x=[T[i][0],T_[i][0]],
            y=[T[i][1],T_[i][1]],
            z=[T[i][2],T_[i][2]],
            mode='lines',
            line=dict(color='red',width=3,dash='solid'),
            showlegend=False
        ) for i in range(res)
    ]
    fig = go.Figure(data=data,
                    layout=go.Layout(
                scene=dict(
                    xaxis=dict(title='X'),
                    yaxis=dict(title='Y'),
                    zaxis=dict(title='Z'),
                ),
                title='Tetrahedron Plot'
            )
        )
    return fig
# Run the app
if __name__ == '__main__':
    app.run_server(debug=1,port=80,host='0.0.0.0')