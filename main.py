from datetime import datetime

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, State, dcc, html
from dateutil.relativedelta import relativedelta
from pandas.tseries.offsets import DateOffset

from src import financial
from src.selic import get_selic

app = Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])


investiment_type = html.Div(
    [
        dbc.Label("Tipo de investimento"),
        dbc.RadioItems(
            options=[
                {"label": "Prefixado", "value": "prefixado"},
                {"label": "Tesouro Selic", "value": "selic"},
            ],
            value="prefixado",
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
        dbc.Label("Taxa anual (%)", id="yearly_rate_label"),
        dbc.Label("SELIC (%)", id="yearly_rate_label1", style={"display": "none"}),
        dbc.Input(id="yearly_rate", value=10, type="number", readonly="readOnly"),
    ],
    className="mb-3",
    id="rate_input",
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
    current_time = datetime.now()
    due_in_months = get_month_difference(date)

    if investiment_type == "prefixado":
        monthly_rate = convert_yearly_to_monthly_rate(yearly_rate / 100)
    else:
        expected_selic = get_selic(current_time - relativedelta(months=1))[-1]["value"]
        monthly_rate = convert_yearly_to_monthly_rate(expected_selic / 100)

    ts = financial.calculate_compound_interest(principal, monthly_rate, due_in_months)
    df = pd.DataFrame(ts, columns=["amount"])
    df["month"] = pd.date_range(
        pd.Timestamp.now().date(), periods=due_in_months + 1, freq=DateOffset(months=1)
    )
    df["amount"] = df["amount"].apply(lambda x: round(x, 2))
    fig = px.line(df, x="month", y="amount")
    fig.update_layout(
        title="Evolução do investimento",
        xaxis_title="Período",
        yaxis_title="Montante",
    )
    return fig


@app.callback(
    Output(component_id="yearly_rate", component_property="readonly"),
    Output(component_id="yearly_rate", component_property="value"),
    Output(component_id="yearly_rate_label", component_property="style"),
    Output(component_id="yearly_rate_label1", component_property="style"),
    Input(component_id="investiment_type", component_property="value"),
)
def toggle_non_editable_rate_input(investiment_type):
    selic_value = get_selic(datetime.now() - relativedelta(months=1))[-1]["value"]
    if investiment_type == "selic":
        return "readOnly", selic_value, {"display": "none"}, {"display": "block"}
    else:
        return None, 0, {"display": "block"}, {"display": "none"}


app.run_server(debug=True)
