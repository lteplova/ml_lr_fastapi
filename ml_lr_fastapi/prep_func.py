import re
import numpy as np

def edit_mileage(row):
    if str(row['mileage']).endswith('km/kg'): # находим единицу измерения с помощью endswith (показывает  окончание с указанным суффиксом)
        row['mileage'] = row['mileage'][:-5] # убираем единицу измерения
        row['mileage'] = round(float(row['mileage'])*1.4, 2) # переводим килограммы в литры
    elif str(row['mileage']).endswith('kmpl'): # если единица измерения литры
        row['mileage'] = round(float(row['mileage'][:-5]), 2) # убираем единицу измерения
    return row


def edit_torque(row):

    if type(row['torque']) != float:

        text = row['torque'].replace('at', '').replace('@', '').lower()
        unit = text
        unit = re.sub(r'[^a-z]',' ', unit).replace('rpm', '').strip()
        col1 = re.sub(r'[^0-9.,]',' ', text).split(' ')[0]
        if unit == 'kgm':
            row['torque'] = round(float(col1)*9.80665, 2)
        else:
            row['torque'] = float(col1)

        col2 = ''.join(re.sub(r'[^0-9.,-]',' ', text).split(' ')[1:]).replace(',', '').split('-')[-1]
        if col2 == '':
            col2 = np.nan

        row['max_torque_rpm'] = float(col2)

    else:
        row['torque'] = row['torque']
        row['max_torque_rpm'] = row['torque']

    return row