import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, State, callback
from dash import html, callback, Input, Output, State, MATCH
from dash.dependencies import Input, Output, State
import os
import pandas as pd
import numpy as np
from dash.exceptions import PreventUpdate
import sys
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import mplfinance as mpf
import io
from io import BytesIO
import base64
import time

dash.register_page(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
#dash.register_page(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# List of stock codes to replace APAIND with
stock_codes = [
    "JAIPOW",
    "YESBAN",
    "ALOIND",
    "RELPOW",
    "SOUBAN",
    "IFCI",
    "SUZENE",
    "IRBINF",
    "INDOVE",
    "BANMAH",
    "RENSUG",
    "CENBAN",
    "NMDSTE",
    "UTKSMA",
    "TV18BR",
    "MINERA",
    "MOTSU",
    "NHPC",
    "COFDAY",
    "IDBI",
    "HIMFUT",
    "NBCC",
    "NATFER",
    "NETW18",
    "IDFBAN",
    "PUNBAN",
    "EMMIND",
    "EQUSMA",
    "REGLEA",
    "SAIL",
    "BANIND",
    "NATALU",
    "LEMTRE",
    "UNIBAN",
    "INDOIL",
    "MRPL",
    "ZOMLIM",
    "PIRPHA",
    "TATSTE",
    "GAIL",
    "WELIND",
    "GUJPPL",
 #   "INDEN",
    "RCF",
    "ENGIND",
    "DCMSI",
 #   "ADICAP",
    "NAGCON",
    "KARVYS",
 #   "FSNECO",

]

layout = html.Div([
    html.Div([
        html.H6("Enter any stock_code below"),  # Add the comment with font size H6
        html.Div(", ".join(stock_codes), style={"display": "inline-block", "font-size": "50%"}),  # Display stock codes side by side separated by commas with half font size
    ], style={"margin-bottom": "10px"}),

    html.Div([
        html.Label("Enter Stock Code:", style={"font-size": "50%"}),  # Reduce text size
        dcc.Input(id="stock-code-input", type="text", value="CENBAN", style={"width": "15%", "font-size": "50%"}),  # Reduce textbox size and text size
        html.Label("Number of Last Rows:", style={"margin-left": "10px", "font-size": "50%"}),  # Reduce text size
        dcc.Input(id="last-rows-input", type="number", value=100, style={"width": "5%", "font-size": "50%"}),  # Reduce textbox size and text size
        html.Button("Plot", id="plot-button", n_clicks=0, style={"margin-left": "10px", "font-size": "50%"}),  # Reduce button size and text size
    ], style={"margin-bottom": "30px"}),

    html.Div(id="chart-container", style={"margin-top": "20px"})  # Add margin-top to create space between textboxes and chart
])

@callback(
    Output("chart-container", "children"),
    Input("plot-button", "n_clicks"),
    State("stock-code-input", "value"),
    State("last-rows-input", "value")
)
def update_chart(n_clicks, stock_code, last_rows):
    if n_clicks > 0 and stock_code:
        try:
            file_path = f"./pages/data/{stock_code}.csv"
            df = pd.read_csv(file_path)
            df["date"] = pd.to_datetime(df["date"])  # Convert "date" column to datetime format
            
            # Select the last rows based on the input value
            df_last_rows = df.iloc[-last_rows:]
            
            # Create additional lines for 'lh' and 'hl' for the last rows
            lh = df_last_rows["high"].rolling(window=14).max()
            hl = df_last_rows["low"].rolling(window=14).min()

            # Plot OHLC candles for the last rows
            ap = mpf.make_addplot(df_last_rows[["lh", "hl"]])
            mpf.plot(df_last_rows.set_index("date"), type='candle', style='charles', title=f"Stock Code: {stock_code}", ylabel="Price", volume=True, ylabel_lower="Volume", figratio=(1, 1), addplot=ap)
            
            buffer = io.BytesIO()
            plt.savefig(buffer, format="png")
            buffer.seek(0)
            plt.close()

            img_str = "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode()

            return html.Img(src=img_str, style={"width": "100%", "height": "600px"})
        except FileNotFoundError:
            return html.Div(f"No data found for stock code: {stock_code}")
    else:
        return html.Div()



if __name__ == "__main__":
    run_server(debug=True)