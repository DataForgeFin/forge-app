from datetime import datetime

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, State, dcc, html
from dateutil.relativedelta import relativedelta
from pandas.tseries.offsets import DateOffset

from data.selic import get_selic
from src import financial

app = Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])


investiment_type = html.Div(
    [
        dbc.Label("Tipo de investimento"),
        dbc.RadioItems(
            options=[
                {"label": "Prefixado", "value": 1},
                {"label": "Tesouro Selic", "value": 2},
            ],
            value=1,
            id="investiment_type",
        ),
    ],
    className="mb-3",
)

principal_input = html.Div(
    [
        dbc.Label("Montante inicial"),
        dbc.Input(id="principal", value=1000, type="number"),
    ],
    className="mb-3",
)

rate_input = html.Div(
    [
        dbc.Label("Taxa anual (%)"),
        dbc.Input(id="yearly_rate", value=10, type="number"),
    ],
    className="mb-3",
)

date_input = html.Div(
    [
        dbc.Label("Vencimento"),
        html.Br(),
        dcc.DatePickerSingle(
            id="date",
            display_format="Y/MM/DD",
            date=datetime.now().date() + relativedelta(years=1, days=1),
        ),
    ],
    className="mb-3",
)

investiment_form = dbc.Row(
    [
        dbc.Col(investiment_type),
        dbc.Col(principal_input),
        dbc.Col(rate_input),
        dbc.Col(date_input),
    ]
)

root_layout = [
    html.H1("Calculadora de investimento"),
    investiment_form,
    dbc.Button("Simular", id="simulate_btn", color="primary", className="me-1"),
    dcc.Graph(id="time-series-chart"),
    html.H1("SELIC"),
    dcc.Graph(id="selic-chart"),
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
    State("investiment_type", "value"),
    State("principal", "value"),
    State("yearly_rate", "value"),
    State("date", "date"),
)
def display_simulate(_, investiment_type, principal, yearly_rate, date):
    due_in_months = get_month_difference(date)

    if investiment_type == 1:
        monthly_rate = convert_yearly_to_monthly_rate(yearly_rate / 100)
    else:
        expected_selic = pd.DataFrame(get_selic(datetime.now() - relativedelta(months=1)))[
            "value"
        ].values[-1]
        monthly_rate = convert_yearly_to_monthly_rate(expected_selic / 100)

    ts = financial.calculate_compound_interest(principal, monthly_rate, due_in_months)
    df = pd.DataFrame(ts, columns=["amount"])
    df["month"] = pd.date_range(
        pd.Timestamp.now().date(), periods=due_in_months + 1, freq=DateOffset(months=1)
    )
    fig = px.line(df, x="month", y="amount")
    fig.update_layout(
        title="Evolução do investimento",
        xaxis_title="Período",
        yaxis_title="Montante",
    )
    return fig


@app.callback(
    Output("selic-chart", "figure"),
    Input("simulate_btn", "n_clicks"),
)
def display_selic(_):
    df = get_selic(datetime(year=2023, month=1, day=1))
    fig = px.line(df, x="date", y="value")
    fig.update_layout(
        title="SELIC",
        xaxis_title="Período",
        yaxis_title="Valor",
    )
    return fig


app.run_server(debug=True)
