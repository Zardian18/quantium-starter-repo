from dash import Dash, html, dcc, callback, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

app = Dash(__name__)
df = pd.read_csv("preprocessed_data.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values('date')
breakpoint_date = datetime(2021,1,15)

color_dict = {'north':'pink', 'south':'yellow', 'east':'blue', 'west':'green'}

app.layout = html.Div([
    html.H1("Sales Trend by region", style={'textAlign':'center', 'marginBottom':'30px'}),
    html.Div([
        dcc.RadioItems(
            id = 'region-selector',
            options=[
                {'label': 'All Regions', 'value': 'all'},
                {'label': 'north', 'value':'north'},
                {'label': 'south', 'value':'south'},
                {'label': 'east', 'value':'east'},
                {'label': 'west', 'value':'west'}
            ],
            value='all',
            inline = True,
            style={'textAlign': 'center'}
        )
    ]),
    dcc.Graph(id = 'sales-graph', style = {'height': '500px'})
])

@callback(
    Output('sales-graph', 'figure'),
    Input('region-selector', 'value')
)
def update_graph(selected_region):
    if selected_region == 'all':
        new_df = df.copy()
        fig = px.line(new_df, x = 'date', y = 'sales', color = 'region', title = 'Sales Trend (All Regions)', labels={'sales': 'Sales ($)', 'date': 'Date', 'region': 'Region'},
        color_discrete_map = color_dict
        )
        fig.update_layout(showlegend=True)
    else:
        new_df = df[df['region']==selected_region]
        fig = px.line(new_df, x = 'date', y = 'sales',title = f'Sales Trend (for {selected_region} Region)',
        labels = {'sales':'Sales ($)', 'date': 'Date'})
        fig.update_traces(
            line_color = color_dict[selected_region],
            line_width = 3
        )
        fig.update_layout(showlegend=False)
    
    fig.add_vline(
        x = breakpoint_date,
        line_dash = 'dot',
        line_color = 'red',
        line_width = 5
    )

    fig.update_layout(
        xaxis_title = 'Date',
        yaxis_title = 'Sales ($)'

    )
    return fig

server = app.server
if __name__ == '__main__':
    app.run(debug=True)