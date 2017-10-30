import pandas as pd

df = pd.read_csv('data1.csv')

high_mileage = 0
low_mileage = 0
good_engine_high = 0  # mileage
good_engine_low = 0
bad_engine_high = 0
bad_engine_low = 0
working_ac = 0
broken_ac = 0
high_car_value_good_working = 0  # engine, ac
high_car_value_good_broken = 0
high_car_value_bad_working = 0
high_car_value_bad_broken = 0
low_car_value_good_working = 0
low_car_value_good_broken = 0
low_car_value_bad_working = 0
low_car_value_bad_broken = 0

for i in range(len(df)):
    if df['High Mileage'][i] == 'TRUE':
        high_mileage += 1
    else:
        low_mileage += 1
    if df['Working AC'][i] == 'TRUE':
        working_ac += 1
    else:
        broken_ac += 1

    if df['Good Engine'][i] == 'TRUE' and df['High Mileage'][i] == 'TRUE':
        good_engine_high += 1
    if df['Good Engine'][i] == 'TRUE' and df['High Mileage'][i] == 'FALSE':
        good_engine_low += 1
    if df['Good Engine'][i] == 'FALSE' and df['High Mileage'][i] == 'FALSE':
        bad_engine_low += 1
    if df['Good Engine'][i] == 'FALSE' and df['High Mileage'][i] == 'TRUE':
        bad_engine_high += 1

    if df['High Car Value'][i] == 'TRUE' and df['Good Engine'][i] == 'TRUE' and df['High Mileage'][i] == 'TRUE':
        high_car_value_good_working += 1
    if df['High Car Value'][i] == 'TRUE' and df['Good Engine'][i] == 'TRUE' and df['High Mileage'][i] == 'FALSE':
        high_car_value_good_broken += 1
    if df['High Car Value'][i] == 'TRUE' and df['Good Engine'][i] == 'FALSE' and df['High Mileage'][i] == 'FALSE':
        high_car_value_bad_broken += 1
    if df['High Car Value'][i] == 'TRUE' and df['Good Engine'][i] == 'FALSE' and df['High Mileage'][i] == 'TRUE':
        high_car_value_bad_working += 1
    if df['High Car Value'][i] == 'FALSE' and df['Good Engine'][i] == 'TRUE' and df['High Mileage'][i] == 'TRUE':
        low_car_value_good_working += 1
    if df['High Car Value'][i] == 'FALSE' and df['Good Engine'][i] == 'TRUE' and df['High Mileage'][i] == 'FALSE':
        low_car_value_good_broken += 1
    if df['High Car Value'][i] == 'FALSE' and df['Good Engine'][i] == 'FALSE' and df['High Mileage'][i] == 'FALSE':
        low_car_value_bad_broken += 1
    if df['High Car Value'][i] == 'FALSE' and df['Good Engine'][i] == 'FALSE' and df['High Mileage'][i] == 'TRUE':
        low_car_value_bad_working += 1































