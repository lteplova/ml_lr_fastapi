import re
import numpy as np

def edit_mileage(row):
    if str(row['mileage']).endswith('km/kg'): # находим единицу измерения с помощью endswith (показывает  окончание с указанным суффиксом)
        row['mileage'] = row['mileage'][:-5] # убираем единицу измерения
        row['mileage'] = round(float(row['mileage'])*1.4, 2) # переводим килограммы в литры
    elif str(row['mileage']).endswith('kmpl'): # если единица измерения литры
        row['mileage'] = round(float(row['mileage'][:-5]), 2) # убираем единицу измерения
    return row


# видно, что используются различные единицы измерения
# kgm - килограмм на метр
# nm - ньютон на метр
# rpm - количество оборотов, которое механизм или двигатель вращается за единицу времени
# 1 kg-m to N-m = 9.80665 N-m
# большинство значений в nm & поэтому будем переводить в эту единицу измерения
def edit_torque(row):

    if type(row['torque']) != float:

        text = row['torque'].replace('at', '').replace('@', '').lower() # удаление лишнего слова и знакак
        unit = text
        unit = re.sub(r'[^a-z]',' ', unit).replace('rpm', '').strip() # выделение единицы измерения
        col1 = re.sub(r'[^0-9.,]',' ', text).split(' ')[0] выделение цифры
        if unit == 'kgm':
            row['torque'] = round(float(col1)*9.80665, 2) # перевод в другие единицы измерения
        else:
            row['torque'] = float(col1)

        col2 = ''.join(re.sub(r'[^0-9.,-]',' ', text).split(' ')[1:]).replace(',', '').split('-')[-1]
        if col2 == '':
            col2 = np.nan

        row['max_torque_rpm'] = float(col2) # формирования колонки max_torque_rpm

    else:
        row['torque'] = row['torque']
        row['max_torque_rpm'] = row['torque']

    return row
