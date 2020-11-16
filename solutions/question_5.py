import pandas as pd
from fbprophet import Prophet
from matplotlib import pyplot


def forecast_volume(data_file: str, days_forward: int):
  """
  Forecast hourly order volume based on days_forward.

  :param data_file:     ( String ) Input CSV file w/ order hours + number of orders.
  :param days_forward:  ( Integer ) Number of days forward.
  :return:              ( DataFrame ) Forecast Timestamp + Predicted Order Volumes
  """

  # Read input data
  hourly_volume_df = pd.read_csv(f"../data/{data_file}")
  # Convert order_hour into datetime
  hourly_volume_df["order_hour"] = pd.to_datetime(hourly_volume_df["order_hour"])
  # Specifics for Prophet : Timestamp = ds and input val = y
  hourly_volume_df.rename(columns={"order_hour": "ds", "num_orders": "y"}, inplace=True)
  # Initiate Prophet w/ multiplicative mode
  prophet_model = Prophet(seasonality_mode='multiplicative')
  # Fit Hourly Volume Data
  prophet_model.fit(hourly_volume_df)
  # Set forecast in hourly granularity
  future = prophet_model.make_future_dataframe(periods=days_forward * 24, freq="H", include_history=False)
  # Forecast days_forward on hourly order volume
  forecast_vol = prophet_model.predict(future)
  # Visualize model components and forecast output
  prophet_model.plot_components(forecast_vol)
  prophet_model.plot(forecast_vol, xlabel="Order Time", ylabel="Order Volume")
  # Set title
  pyplot.title("Order Volume")
  # Display graph
  pyplot.show()
  # Get forecast Timestamp and predict order volumes
  forecast_ds_volume_df = forecast_vol[["ds", "yhat"]].copy()
  # Rename ds to order_hour and yhat to pred_order_volume
  forecast_ds_volume_df.rename(columns={"ds": "order_hour", "yhat": "pred_order_volume"}, inplace=True)

  return forecast_ds_volume_df

# >>>>>>>>>>>>>>>>> MAIN >>>>>>>>>>>>>>>>>>>>>>>>>

# Number of days forward to forecast
NUM_DAYS_FORWARD = 2
# Forecast Hourly Volume
forecast_volume(data_file="hourly_volume.csv", days_forward=NUM_DAYS_FORWARD)
