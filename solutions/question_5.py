import os

import pandas as pd
from fbprophet import Prophet
from matplotlib import pyplot


def forecast_volume(data_file, days_forward):
  """
  Forecast hourly order volume based on days_forward.

  :param data_file:     ( String ) Input CSV file w/ order hours + number of orders.
  :param days_forward:  ( Integer ) Number of days forward.
  :return:              ( DataFrame ) Forecast Timestamp + Predicted Order Volumes.
  """
  # Read input data
  hourly_volume_df = pd.read_csv(f"{os.getcwd()}/../data/{data_file}", usecols = ["order_hour","num_orders"])
  # Convert order_hour into datetime
  hourly_volume_df["order_hour"] = pd.to_datetime(hourly_volume_df["order_hour"])
  # Specifics for Prophet : Timestamp = ds and input val = y
  hourly_volume_df.rename(columns={"order_hour": "ds", "num_orders": "y"}, inplace=True)
  # Initiate Prophet w/ multiplicative mode
  prophet_model = Prophet(seasonality_mode="multiplicative")
  # Fit Hourly Volume Data
  prophet_model.fit(hourly_volume_df)
  # Set forecast in hourly granularity
  future = prophet_model.make_future_dataframe(periods=days_forward * 24, freq="H", include_history=False)
  # Forecast days_forward on hourly order volume
  forecast_vol = prophet_model.predict(future)
  # Visualize model components and forecast output
  fig = prophet_model.plot_components(forecast_vol)
  # Rename x labels to corresponding time breakdown
  fig.get_children()[1].set_xlabel("order date")
  fig.get_children()[2].set_xlabel("order day")
  fig.get_children()[3].set_xlabel("order hour")
  prophet_model.plot(forecast_vol, xlabel="Order Time", ylabel="Order Volume")
  # Set title
  pyplot.title("Order Volume")
  # Display graph
  # pyplot.show()
  # Get forecast Timestamp and predict order volumes
  forecast_ds_volume_df = forecast_vol[["ds", "yhat"]].copy()
  # Rename ds to order_hour and yhat to pred_order_volume
  forecast_ds_volume_df.rename(columns={"ds": "order_hour", "yhat": "pred_order_volume"}, inplace=True)

  return forecast_ds_volume_df

# >>>>>>>>>>>>>>>>> MAIN >>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>> Params
# Number of days forward to forecast. Default to 1 ( day ).
NEW_NUM_DAYS_FORWARD = 2
# Input file that consists of "order_hour" + "num_orders"
NEW_DATA_FILE_NAME = "hourly_volume.csv"

# >>>>> Default Vals
NUM_DAYS_FORWARD = 1
DATA_FILE_NAME = "hourly_volume.csv"

# >>>> Sanity Check
# Ensure 2 necessary column names are within the 'new' input file before overwriting the default one
new_data_file = pd.read_csv(f"{os.getcwd()}/../data/{NEW_DATA_FILE_NAME}")
# New Data File Column Names
new_data_file_columns = list(new_data_file.columns)
# Check 2 needed column within the new data file
if "order_hour" in new_data_file_columns and "num_orders" in new_data_file_columns:
  # Overwrite default file name when new file has valid columns
  DATA_FILE_NAME = NEW_DATA_FILE_NAME

# Check NUM_DAYS_FORWARD is valid number
try:
  days_num = int(NEW_NUM_DAYS_FORWARD)
except ValueError:
  pass
else:
  NUM_DAYS_FORWARD = int(NEW_NUM_DAYS_FORWARD)

# Forecast Hourly Volume
forecast_orders = forecast_volume(data_file=DATA_FILE_NAME, days_forward=NUM_DAYS_FORWARD)
# Forecast Output to Excel under 'data' folder
forecast_orders.to_excel(f"{os.getcwd()}/../data/hourly_forecast_volume.xlsx", index=False)
