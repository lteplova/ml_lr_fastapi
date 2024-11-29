from io import StringIO
import pandas as pd
import re
import pickle
from prep_func import edit_mileage
from prep_func import edit_torque
from dataclasses import dataclass


@dataclass
class Prediction:
    """Класс для вывода предсказания"""
    input_text: str
    predict: float


# json_test = ''' {
#         "name": "Maruti Swift Dzire VDI",
#         "year": 2014,
#         "selling_price": 450000,
#         "km_driven": 145500,
#         "fuel": "Diesel",
#         "seller_type": "Individual",
#         "transmission": "Manual",
#         "owner": "First Owner",
#         "mileage": "23.4 kmpl",
#         "engine": "1248 CC",
#         "max_power": "74 bhp",
#         "torque": "190Nm@ 2000rpm",
#         "seats": 5.0
#         }
#          '''
# test_test = pd.DataFrame([pd.read_json(StringIO(json_test), typ='series')])
# test_test =  pd.read_csv('public/cars.csv')

def load_model():
    # загрузка модели ridge
    with open('/Users/lu/PycharmProjects/ml_lr_fastapi/models/ridge.pkl', 'rb') as f:
        ridge = pickle.load(f)
    # загрузка модели OHE
    with open('/Users/lu/PycharmProjects/ml_lr_fastapi/models/ohe.pkl', 'rb') as f:
        one_hot_enc = pickle.load(f)

    def inference(test_test, model = ridge, one_hot_enc = one_hot_enc) -> Prediction:

        cat_cols = ['name', 'fuel', 'seller_type', 'transmission', 'owner']
        # редактирование 'mileage'
        test_test = test_test.apply(edit_mileage, axis = 1)
        # редактирование 'engine'
        test_test['engine'] = test_test['engine'].apply(lambda x: float(re.sub(r'[^0-9]','', x)) if type(x) == str else x)
        # редактирование 'max_power'
        test_test['max_power'] = test_test['max_power'].apply(lambda x: float(re.sub(r'[^0-9.]','', x).strip()) if type(x) == str else x)
        # редактирование 'torque'
        test_test = test_test.apply(edit_torque, axis=1)
        # редактирование name
        test_test['name'] = test_test['name'].apply(lambda x: re.search(r'^[^ ]*', x.lower())[0])
        test_test['engine'] = test_test['engine'].astype('int64')
        test_test['seats'] = test_test['seats'].astype('int64')

        # кодирование
        encoded_df_test = pd.DataFrame(one_hot_enc.transform(test_test[cat_cols]))
        encoded_df_test.columns = one_hot_enc.get_feature_names_out()
        X_test_onehot = test_test.join(encoded_df_test)
        X_test_onehot.drop(columns=cat_cols, axis = 1, inplace = True)
        X_test_onehot.drop('selling_price', axis = 1, inplace = True)
        # предсказание
        predict = model.predict(X_test_onehot)
        # return Prediction(input_text = json_test, predict = float(predict[0]))
        return predict

    return inference

if __name__ == '__main__':
    test_model = load_model()
    predict_final = test_model(test_test)
    print(predict_final)