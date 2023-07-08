from datetime import datetime, timedelta

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, State, dcc, html
from dateutil.relativedelta import relativedelta
from pandas.tseries.offsets import DateOffset

from src import financial

app = Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])


principal_input = html.Div(
    [
        dbc.Label("Montante inicial"),
        dbc.Input(id="principal", value=1000, type="number"),
    ],
    className="mb-3",
)

rate_input = html.Div(
    [
        dbc.Label("Taxa anual"),
        dbc.Input(id="yearly_rate", value=0.1, type="number"),
    ],
    className="mb-3",
)

date_input = html.Div(
    [
        dbc.Label("Vencimento"),
        dcc.DatePickerSingle(
            id="date", display_format="Y/MM/DD", date=datetime.now().date() + timedelta(days=365)
        ),
    ],
    className="mb-3",
)

investiment_form = dbc.Row(
    dbc.Col(
        [principal_input, rate_input, date_input],
        width=2,
    )
)

root_layout = [
    html.H1("Calculadora de investimento"),
    investiment_form,
    dbc.Button("Simular", id="simulate_btn", color="primary", className="me-1"),
    dcc.Graph(id="time-series-chart"),
]

app.layout = html.Div(
    dbc.Row(
        dbc.Col(
            root_layout,
            width=10,
        ),
        justify="center",
    )
)


def convert_yearly_to_monthly_rate(yearly_rate):
    monthly_rate = (1 + yearly_rate) ** (1 / 12) - 1
    return monthly_rate


def get_month_difference(end_date):
    start_datetime = datetime.now()
    end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
    difference = relativedelta(end_datetime, start_datetime)
    return difference.years * 12 + difference.months


@app.callback(
    Output("time-series-chart", "figure"),
    Input("simulate_btn", "n_clicks"),
    State("principal", "value"),
    State("yearly_rate", "value"),
    State("date", "date"),
    prevent_initial_call=True,
)
def display_simulate(_, principal, yearly_rate, date):
    due_in_months = get_month_difference(date)
    monthly_rate = convert_yearly_to_monthly_rate(yearly_rate)
    ts = financial.calculate_compound_interest(principal, monthly_rate, due_in_months)
    df = pd.DataFrame(ts, columns=["amount"])
    df["month"] = pd.date_range(
        pd.Timestamp.now().date(), periods=due_in_months, freq=DateOffset(months=1)
    )
    fig = px.line(df, x="month", y="amount")
    return fig


app.run_server(debug=True)
