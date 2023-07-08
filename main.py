from datetime import date, datetime

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, State, dcc, html
from dateutil.relativedelta import relativedelta
from pandas.tseries.offsets import DateOffset

from src import financial

app = Dash(__name__, external_stylesheets=[dbc.themes.MATERIA])


investiment_form = html.Div(
    [
        dbc.FormFloating(
            [dbc.Input(id="principal", value=1000, type="number"), dbc.Label("Montante inicial")]
        ),
        dbc.FormFloating(
            [
                dbc.Input(id="yearly_rate", value=0.1, type="number"),
                dbc.Label("Taxa anual"),
            ]
        ),
        dbc.Label("Vencimento"),
        dcc.DatePickerSingle(id="date", display_format="Y/MM/DD", date=date(2024, 8, 1)),
    ]
)


app.layout = html.Div(
    [
        html.H1("Calculadora de investimento"),
        investiment_form,
        dbc.Button("Simular", id="simulate_btn", color="primary", className="me-1"),
        dcc.Graph(id="time-series-chart"),
    ]
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
