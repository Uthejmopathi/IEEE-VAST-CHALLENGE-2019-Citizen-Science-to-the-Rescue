from flask import Flask, render_template, send_file
import pandas as pd

app = Flask(__name__)

# Uncomment the below lines if the dataset is changed. The below code will perform ETL on the main dataset and
# and creates visual specific csv files

# # initial data preparation
# mb_sen_df = pd.read_csv('data/MobileSensorReadings.csv')
# mb_sen_df['Value'] = mb_sen_df['Value'].astype(int)
# st_sen_red_df = pd.read_csv('data/StaticSensorReadings.csv')
# st_sen_red_df['Value'] = st_sen_red_df['Value'].astype(int)
# st_sen_loc_df = pd.read_csv('data/StaticSensorLocations.csv')
# st_sen_df = st_sen_red_df.join(st_sen_loc_df.set_index('Sensor-id'), on='Sensor-id')
# st_sen_df = st_sen_df[['Timestamp', 'Sensor-id', 'Long', 'Lat', 'Value', 'Units']]
# mb_sen_df = mb_sen_df[['Timestamp', 'Sensor-id', 'Long', 'Lat', 'Value', 'Units']]
# comb_sen_df = mb_sen_df.append(st_sen_df)
#
# # Data for all sensors
# comb_sen_df["Value"] = comb_sen_df["Value"].apply(lambda x: int(x / 200) * 200)
# comb_sen_count_df = comb_sen_df.groupby('Value').count()['Sensor-id'].to_frame().reset_index().sort_values(by='Value')
# comb_sen_count_df = comb_sen_count_df.rename(columns={"Value": "language", "Sensor-id": "value"})
# comb_sen_count_df.to_json('file_comb_sen.json', orient='records', lines=True)
#
# # Data for static sensors
# st_sen_df["Value"] = st_sen_df["Value"].apply(lambda x: int(x / 200) * 200)
# st_sen_count_df = st_sen_df.groupby('Value').count()['Sensor-id'].to_frame().reset_index().sort_values(by='Value')
# st_sen_count_df = st_sen_count_df.rename(columns={"Value": "language", "Sensor-id": "value"})
# st_sen_count_df.to_json('file_st_sen.json', orient='records', lines=True)
#
# # Data for mobile sensors
# mb_sen_df["Value"] = mb_sen_df["Value"].apply(lambda x: int(x / 200) * 200)
# mb_sen_count_df = mb_sen_df.groupby('Value').count()['Sensor-id'].to_frame().reset_index().sort_values(by='Value')
# mb_sen_count_df = mb_sen_count_df.rename(columns={"Value": "language", "Sensor-id": "value"})
# mb_sen_count_df.to_json('file_mb_sen.json', orient='records', lines=True)
#
# # Data for time series all sensors
# comb_sen_df['Timestamp'] = comb_sen_df['Timestamp'].apply(lambda x: x[:-2] + "00")
# comb_sen_time_df = comb_sen_df.groupby('Timestamp').sum()['Value'].to_frame().reset_index()
# comb_sen_time_df = comb_sen_time_df.rename(columns={"Timestamp": "time", "Value": "value"})
# comb_sen_time_df.to_csv('file_comb_time.csv', index=False)
#
# # Data for time series mobile sensors
# mb_sen_df['Timestamp'] = mb_sen_df['Timestamp'].apply(lambda x: x[:-2] + "00")
# mb_sen_time_df = mb_sen_df.groupby('Timestamp').sum()['Value'].to_frame().reset_index()
# mb_sen_time_df = mb_sen_time_df.rename(columns={"Timestamp": "time", "Value": "value"})
# mb_sen_time_df.to_csv('file_mb_time.csv', index=False)
#
# # Data for time series stationary sensors
# st_sen_df['Timestamp'] = st_sen_df['Timestamp'].apply(lambda x: x[:-2] + "00")
# st_sen_time_df = st_sen_df.groupby('Timestamp').sum()['Value'].to_frame().reset_index()
# st_sen_time_df = st_sen_time_df.rename(columns={"Timestamp": "time", "Value": "value"})
# st_sen_time_df.to_csv('file_st_time.csv', index=False)
#
#
# # Data at sensor level
# # for static sensors
# mb_sen_stats_df = mb_sen_df[['Timestamp', 'Sensor-id', 'Value']]
# mb_sen_stats_df = mb_sen_stats_df.pivot_table(values='Value', index='Timestamp', columns='Sensor-id', aggfunc='first')
# mb_sen_stats_df.to_csv('static/file_mb_sen_stats.csv')
#
# st_sen_stats_df = st_sen_df[['Timestamp', 'Sensor-id', 'Value']]
# st_sen_stats_df = st_sen_stats_df.pivot_table(values='Value', index='Timestamp', columns='Sensor-id', aggfunc='first')
# st_sen_stats_df.to_csv('static/file_st_sen_stats.csv')


@app.route('/')
def landing_page():
    with open('file_comb_sen.json') as f:
        lines = f.readlines()
    json_string = '['
    for line in lines[1:]:
        json_string = json_string + line[:-1] + ','
    json_string = json_string[:-1] + '}]'
    return render_template('index.html', json_string=json_string, max_height=35000, sen_type="")


@app.route('/sensors_st')
def landing_page_st():
    with open('file_st_sen.json') as f:
        lines = f.readlines()
    json_string = '['
    for line in lines[1:]:
        json_string = json_string + line[:-1] + ','
    json_string = json_string[:-1] + '}]'
    return render_template('index.html', json_string=json_string, max_height=100, sen_type="Static ")


@app.route('/sensors_mb')
def landing_page_mb():
    with open('file_mb_sen.json') as f:
        lines = f.readlines()
    json_string = '['
    for line in lines[1:]:
        json_string = json_string + line[:-1] + ','
    json_string = json_string[:-1] + '}]'
    return render_template('index.html', json_string=json_string, max_height=35000, sen_type="Mobile ")


@app.route('/time_series')
def time_series():
    temp_df = pd.read_csv('file_comb_time.csv')
    time_list = temp_df['time'].tolist()
    value_list = temp_df['value'].tolist()
    return render_template('time_series.html', time_list=time_list, value_list=value_list)


@app.route('/time_series_mb')
def time_series_mb():
    temp_df = pd.read_csv('file_mb_time.csv')
    time_list = temp_df['time'].tolist()
    value_list = temp_df['value'].tolist()
    return render_template('time_series.html', time_list=time_list, value_list=value_list)


@app.route('/time_series_st')
def time_series_st():
    temp_df = pd.read_csv('file_st_time.csv')
    time_list = temp_df['time'].tolist()
    value_list = temp_df['value'].tolist()
    return render_template('time_series.html', time_list=time_list, value_list=value_list)


@app.route('/mb_sen_timeline')
def mb_sen_timeline():
    return render_template('mb_sen_timeline.html')


@app.route('/st_sen_timeline')
def st_sen_timeline():
    return render_template('st_sen_timeline.html')
