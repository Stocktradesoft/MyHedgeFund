import dash
from dash import html, Input, Output, dash_table, callback
import pandas as pd
import json
from breeze_connect import BreezeConnect
import os
import datetime

dash.register_page(__name__, path='/')


# Read configuration data from datetimekey.json
with open("./pages/datetimekey.json") as f:
    config_data = json.load(f)

# Extract values from config_data
key_api = config_data.get("key_api", "")
key_secret = config_data.get("key_secret", "")
key_session = config_data.get("key_session", "")
time_interval = config_data.get("time_interval", "")
from_date = config_data.get("from_date", "")
to_date = config_data.get("to_date", "")

# Initialize the BreezeConnect object
breeze = BreezeConnect(api_key=key_api)
breeze.generate_session(api_secret=key_secret, session_token=key_session)

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

# Define the layout of the app
layout = html.Div(
    [
        html.H1("Historical Stock Data"),
        html.Button("Show Data", id="show-data-button"),
         html.Button("Show Table", id="show-table-button"),
        html.Div(id="data-table"),
    ]
)


# Define the callback to generate the table
@callback(Output("data-table", "children"), [Input("show-data-button", "n_clicks"), Input("show-table-button", "n_clicks")])
def generate_table(n_clicks_data, n_clicks_table):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = None
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'show-data-button':

        # Fetch historical data for all stock codes and the given date range
        data_frames = []
        for code in stock_codes:
            historical_data = breeze.get_historical_data_v2(
                interval=time_interval,
                from_date=from_date,
                to_date=to_date,
                stock_code=code,
                exchange_code="NSE",
            )
        #   print("Historical Data:", historical_data)  # Print historical data for debugging
            data_df = pd.DataFrame(
                historical_data['Success'],
                columns=["datetime", "stock_code", "open", "high", "low", "close", "volume"],
            )

            data_df.reset_index(drop=True, inplace=True)
            data_df.drop_duplicates(inplace=True)
            data_df['date'] = pd.to_datetime(data_df['datetime']).dt.date
            # Initialize variables to track the start and end indices of RSI > 70 period
            rsi_high_period_start = None
            rsi_high_period_end = None
            # Initialize a flag to track if we are currently in an RSI > 70 period
            in_rsi_high_period = False

            # Define the lookback period for RSI < 30
            lookback_period = 5

            # Initialize lh to None
            lh = None

            for i in range(1, len(data_df)):
                if (data_df['close'][i] > data_df['close'][i - 1]):
                        # Check the last 'lookback_period' data points
                    for j in range(i - 1, max(i - lookback_period - 1, 0), -1):
                        if data_df['close'][j] > 0:
                            rsi_high_period_start = j
                            rsi_high_period_end = i
                            in_rsi_high_period = True
                            # Append low price at the last higher low
                            data_df.loc[i, "lh"] = data_df.loc[j, 'low']
                            break

                if in_rsi_high_period:
                        # Check if the current high is greater than the high within the RSI > 70 period
                    if data_df['high'][i] > max(data_df['high'][rsi_high_period_start:rsi_high_period_end + 1]):
                            # Reset the RSI high period variables
                        rsi_high_period_start = None
                        rsi_high_period_end = None
                        in_rsi_high_period = False



                # Now, the 'lh' column will contain the price values for the last higher low.

                # Initialize variables to track the start and end indices of RSI < 30 period
            rsi_low_period_start = None
            rsi_low_period_end = None

                # Initialize a flag to track if we are currently in an RSI < 30 period

            in_rsi_low_period = False

                # Define the lookback period for RSI < 30
            lookback_period = 5

                # Initialize hl to None
            hl = None

            for i in range(1, len(data_df)):
                if (data_df['close'][i] < data_df['close'][i - 1]):
                        # Check the last 'lookback_period' data points
                    for j in range(i - 1, max(i - lookback_period - 1, 0), -1):
                        if data_df['close'][j] < 100:
                            rsi_low_period_start = j
                            rsi_low_period_end = i
                            in_rsi_low_period = True
                            # Append high price at the last lower high
                            data_df.loc[i, "hl"] = data_df.loc[j, 'high']
                            break

                if in_rsi_low_period:
                        # Check if the current low is less than the low within the RSI < 30 period
                    if data_df['low'][i] < min(data_df['low'][rsi_low_period_start:rsi_low_period_end + 1]):
                            # Reset the RSI low period variables
                        rsi_low_period_start = None
                        rsi_low_period_end = None
                        in_rsi_low_period = False
            # lh and hl are value of STOP_LOSS 
                        
            #data_df["datetime"] = pd.to_datetime(
            #    data_df["datetime"], format="%Y-%m-%d %H:%M:%S"
            #)
    #       data_df.reset_index(drop=True, inplace=True)
            # Fill missing values in "lh" and "hl" columns
            if pd.isna(data_df.at[0, "lh"]):
                data_df.at[0, "lh"] = data_df.at[0, "close"]

            if pd.isna(data_df.at[0, "hl"]):
                data_df.at[0, "hl"] = data_df.at[0, "close"]
    #       data_df.reset_index(drop=True, inplace=True)
            data_df["lh"].fillna(method='ffill', inplace=True)
    #        print("data_df_lh",data_df["lh"])        
            data_df["hl"].fillna(method='ffill', inplace=True)
    #        print("data_df_hl",data_df["hl"])
            data_df.reset_index(drop=True, inplace=True)

            data_df["lh"] =  (data_df["lh"] - (data_df["lh"] * 0.04))   # 0.01 is 1%  hence use 0.002 means 0.2%
            data_df["hl"] =  (data_df["hl"] + (data_df["hl"] * 0.04))   # 0.01 is 1%  hence use 0.002 means 0.2%
            data_df["lh7"] = data_df["lh"].rolling(window=7).mean()
            data_df["hl7"] = data_df["hl"].rolling(window=7).mean()
            # Reset index and drop duplicates
            data_df.reset_index(drop=True, inplace=True)
            data_df.drop_duplicates(inplace=True)
        #    print(data_df)
            # Drop NA values
            data_df.reset_index(drop=True, inplace=True)
            data_df.dropna(inplace=True)
            file_path = f"./pages/data/{code}.csv"
            data_df.to_csv(file_path, index=False)

    # Assuming data_frames is a list containing data frames for each stock_code
        data_frames = []
        # Read data from each CSV file
        for file_name in os.listdir("./pages/data/"):
            if file_name.endswith(".csv"):
                file_path = os.path.join("./pages/data/", file_name)
                # Read data from CSV file
                data_df = pd.read_csv(file_path)

                data_df = data_df.tail(100)
            # Calculate close_diff based on a fixed investment amount
                initial_price = data_df.iloc[0]["close"]
                investment_amount = 1000  # Adjust as needed
                investment_Qty = investment_amount / initial_price 
                # Append initial_price and investment_Qty to the DataFrame
                data_df["initial_price"] = initial_price
                data_df["investment_Qty"] = investment_Qty
    #           data_df["initial_price"].fillna(method='ffill', inplace=True)
    #           data_df["investment_Qty"].fillna(method='ffill', inplace=True)
                # Append the initial values of investment_Qty and initial_price to the length of the DataFrame
                data_df["initial_price"] = [initial_price] * len(data_df)
                data_df["investment_Qty"] = [investment_Qty] * len(data_df)
                data_df["initial_price"] = data_df["initial_price"].round(2)
                data_df["investment_Qty"] = data_df["investment_Qty"].round(2)
    #            data_df["close_diff"] = (data_df["close"].diff() / initial_price) * investment_amount
                data_df["close_diff"] = (data_df["close"].diff()) *  (initial_price / investment_amount)
                data_df["close_diff"] = data_df["close_diff"].round(2)
                data_df = data_df.tail(98)
                data_frames.append(data_df)
        #       print(data_frames)

        # Combine data frames
        combined_df = pd.concat(data_frames)

        # convert datetime column to just date
        #combined_df['date'] = pd.to_datetime(combined_df['datetime']).dt.date
        # Pivot the combined DataFrame
        pivoted_df = combined_df.pivot_table(index=["stock_code", "initial_price", "investment_Qty"], columns='date', values='close_diff')

        # Reset index to make 'stock_code', 'initial_price', and 'investment_Qty' columns again
        pivoted_df.reset_index(inplace=True)
        
        # Reorder the columns to place 'initial_price' and 'investment_Qty' at the beginning
        columns = ['stock_code', 'initial_price', 'investment_Qty'] + pivoted_df.columns[3:].tolist()
        pivoted_df = pivoted_df[columns]
        pivoted_df.reset_index(drop=True, inplace=True)
        # Calculate the sum of close_diff for each datetime
        datetime_gain = combined_df.groupby('date')['close_diff'].sum()

        # Convert datetime_gain to a DataFrame and transpose it to make it compatible with pivoted_df
        datetime_gain_df = pd.DataFrame(datetime_gain).T
        datetime_gain_df = datetime_gain_df.round(2)

        # Append datetime_gain_df as a new row to pivoted_df
        pivoted_df = pd.concat([pivoted_df, datetime_gain_df])
 #       pivoted_df.reset_index(drop=True, inplace=True)
        # Add initial_price and (initial_price / investment_amount) to the index

        # Print the pivoted DataFrame
    #   print("pivoted_df:", pivoted_df)
    #   print("pivoted_df_GAIN:", pivoted_df["GAIN"])
        # Export pivoted_df to a CSV file
        # Get today's date
    #    today_date = datetime.date.today().strftime("%Y-%m-%d")
        
        # Export pivoted_df to a CSV file with today's date in the filename
        csv_filename = f"pivoted_df.csv"
        pivoted_df.to_csv(csv_filename)
        # Convert datetime.date objects to strings
        pivoted_df.columns = pivoted_df.columns.map(str)
        # Create a Dash DataTable component with conditional formatting
        table = html.Div(
            [
                html.H3("GAIN Table for 1000 trade each stock"),
                html.H4("CELLS below date columns show change in close w.r.t. initial_price"),
                html.H4("BUY when close_diff row value gives a sudden huge drop and start growing"),
                dash_table.DataTable(
                    id='table',
                    columns=[{'name': col, 'id': col} for col in pivoted_df.columns],
                    data=pivoted_df.to_dict('records'),
                    style_data_conditional = [
                        {
                            'if': {'filter_query': '{close_diff} > 0'},
                            'backgroundColor': 'green',
                            'color': 'white'
                        },
                        {
                            'if': {'filter_query': '{close_diff} < 0'},
                            'backgroundColor': 'red',
                            'color': 'white'
                        }
                    ]
                ),
            ]
        )

        return table
        pass

    elif button_id == 'show-table-button':
        # Read data from pivoted_df.csv and generate the table
        if os.path.exists("pivoted_df.csv"):
            pivoted_df = pd.read_csv("pivoted_df.csv")
            table = html.Div(
                [
                    html.H3("GAIN Table for 1000 trade each stock"),
                    html.H4("CELLS below date columns show change in close w.r.t. initial_price"),
                    html.H4("BUY when close_diff row value gives a sudden huge drop and start growing"),
                    dash_table.DataTable(
                        id='table',
                        columns=[{'name': col, 'id': col} for col in pivoted_df.columns],
                        data=pivoted_df.to_dict('records'),
                        style_data_conditional = [
                            {
                                'if': {'filter_query': '{close_diff} > 0'},
                                'backgroundColor': 'green',
                                'color': 'white'
                            },
                            {
                                'if': {'filter_query': '{close_diff} < 0'},
                                'backgroundColor': 'red',
                                'color': 'white'
                            }
                        ]
                    ),
                ]
            )
            return table
        else:
            return html.Div("No data available. Please click 'Show Data' button first.")
    else:
        return ""

# Run the Dash app
if __name__ == "__main__":
    run_server(debug=True)
