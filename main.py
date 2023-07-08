import dash_bootstrap_components as dbc
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

app = Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])


app.layout = html.Div(
    [
        html.H1("Stock price analysis"),
        dcc.Graph(id="time-series-chart"),
        html.P("Select stock:"),
        dcc.Dropdown(
            id="ticker",
            options=["AMZN", "FB", "NFLX"],
            value="AMZN",
            clearable=False,
        ),
    ]
)


@app.callback(Output("time-series-chart", "figure"), Input("ticker", "value"))
def display_time_series(ticker):
    df = px.data.stocks()  # replace with your own data source
    fig = px.line(df, x="date", y=ticker)
    return fig


app.run_server(debug=True)
