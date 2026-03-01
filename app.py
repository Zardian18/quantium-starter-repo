from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

app = Dash(__name__)
df = pd.read_csv("preprocessed_data.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values('date')
breakpoint_date = datetime(2021,1,15)
fx = px.line(df, x = 'date', y = 'sales', color = 'region', title = 'Combined graph', labels={
    'sales':'Sales', 'date':'Dates'
})
fx.add_vline(x = breakpoint_date, line_dash='dot', line_color='red', line_width = 2)
fx.update_layout(
        height = 400
    )
regions = df['region'].unique()
color_dict = {'north':'pink', 'south':'yellow', 'east':'blue', 'west':'green'}

figures = {}
for r in regions:
    region_df = df[df['region']==r]
    fig = px.line(region_df, x = 'date', y = 'sales', title = f'{r.title()} region sales', labels={
        'sales':'Sales', 'date':'Dates'
    })
    fig.update_traces(
        line_color = color_dict[r]
    )
    fig.add_vline(x = breakpoint_date, line_dash='dot', line_color='red', line_width = 2)
    fig.update_layout(
        height = 400,
        showlegend = False
    )

    figures[r] = fig


app.layout = html.Div([
    html.H1("Sales trend by region", style={'textAlign':'center', 'marginBottom':'30px'}),
    html.Div([
        dcc.Graph(figure=figures['north'])
    ]),
    html.Div([
        dcc.Graph(figure=figures['south'])
    ]),
    html.Div([
        dcc.Graph(figure=figures['east'])
    ]),
    html.Div([
        dcc.Graph(figure=figures['west'])
    ]),
    html.Div([
        dcc.Graph(figure = fx)
    ])
])

if __name__ == '__main__':
    app.run(debug=True)