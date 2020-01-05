from configparser import ConfigParser
from datetime import date, timedelta
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from weather import get_weather_data

config = ConfigParser()
config.read('../config.ini')

forecast_range = int(config['options']['forecast_range'])
plot_history_range = int(config['options']['plot_history_range'])
pred_attribute = config['options']['attribute']
history_range = int(config['options']['history_range'])

if plot_history_range > history_range:
    plot_history_range = history_range

# Creates a dataframe containing the weather data used to forecast the weather
# Also drops unnecessary columns and fills/removes empty cells
def init_df(weather_data):
    df = pd.DataFrame(weather_data).drop(
        ['snowfall', 'snowdepth', 'sunshine', 'winddirection'], 1)
    df.fillna(method='ffill', inplace=True)
    df = df.dropna()
    df.reset_index(drop=True)
    return df

# Creates and fits a Linear Regression model based on the provided dataframe and the desired attribute (from config)
def init_model(df):
    X = np.array(df.drop([pred_attribute, 'date'], 1))
    y = np.array(df[pred_attribute])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
    model = LinearRegression()
    model.fit(X_train, y_train)
    print('Model-Score: ' + str(model.score(X_test, y_test)))
    return model, X

# Creates a dataframe containing the predicted values
def get_predicted_df(predicted_values):
    pred_df = pd.DataFrame()
    pred_df[pred_attribute] = pred_val
    pred_df['date'] = get_dates_for_forecast(weather_data[len(weather_data) - 1]['date'], forecast_range)
    return pred_df

# Creates the dates for the preidcted data to be saved in a dataframe
def get_dates_for_forecast(from_date, forecast_range):
    dates = []
    from_date = date(int(from_date[0:4]), int(
        from_date[5:7]), int(from_date[8:10]))
    for i in range(forecast_range):
        dates.append(str((from_date + timedelta(days=(i + 1)))))
    return dates

# Appends the predicted dataframe to the tail of the original dataframe
# Also cleans up labels and index
def prepare_df_for_plot(df):
    df.drop(df.columns.difference([pred_attribute, 'date']), 1, inplace=True)
    df = df.iloc[len(df) - plot_history_range:]
    df = df.append(pred_df, sort=False)
    df['date'] = df['date'].str[8:10] + '.' + df['date'].str[5:7] + '.' + df['date'].str[0:4]
    df.set_index('date', inplace=True)
    return df

# Creates a plot from the dataframe
def plot(df):
    pl = df.plot(figsize=(15, 10))
    pl.set_xlabel('')
    pl.set_xticks(range(len(df)))
    pl.set_xticklabels(df.index.values, rotation=60)
    plt.show()

# Retrieve Weather Data
weather_data = get_weather_data()

# Create the dataframe and model
df = init_df(weather_data)
model, X = init_model(df)

# Calculate the predicted values
pred_set = X[-forecast_range:]
pred_val = model.predict(pred_set)

# Setup predicted df and prepare for plot and printing
pred_df = get_predicted_df(pred_val)
df = prepare_df_for_plot(df)

print(df)
plot(df)
