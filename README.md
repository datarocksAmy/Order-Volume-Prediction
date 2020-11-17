<img src="https://github.com/datarocksAmy/Order-Volume-Prediction/blob/main/graphs/Eaze%20Logo%202.png" width="100">

# Eaze Code Challenge 
This repo is mainly for Order Volume Prediction (Q5) part and documentation + thought process for all the challenges. <br>
Details / documentation of each questions can be found on the [wiki page](https://github.com/datarocksAmy/Order-Volume-Prediction/wiki).

## Dependencies + Compiler Installation

For Windows10 instructions :

##### 1. Install C++ Compiler : mingw-w64
  ```
  conda install libpython m2w64-toolchain -c msys2
  ```
##### 2. Install PyStan ( conda or pip )
  ```
  conda install pystan -c conda-forge
  ```
  ```
  pip install pystan
  ```
##### 3. Install Prophet ( conda or pip )
  ```
  conda install -c conda-forge fbprophet.
  ```
  ```
  pip install fbprophet
  ```
For more detail of how to set up - See [here](https://facebook.github.io/prophet/docs/installation.html).

## Param
- `data_file` : String value. Default Input file name - "hourly_volume.csv" that consists of "order_hour" and "order_volume". <br>
- `days_forward` : An integer indicates the number of days to forecast order volumes out on hourly granularity. Default to 1 day.

## Execute
Change input_data file on line #49 `NEW_DATA_FILE_NAME` and/or days_forward on line #47 `NEW_NUM_DAYS_FORWARD`.
```
run "question_5.py"
```

## Output
An excel file named `hourly_forecast_volume.xlsx` would be generated under `data` folder.

## Licensing

MIT License | Copyright © 2018 Eaze
