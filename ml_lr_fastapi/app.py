from fastapi import FastAPI, Body
from fastapi.responses import FileResponse
from pydantic import BaseModel, model_validator
from model import load_model
from typing import List
import pandas as pd
import json
from io import StringIO

class Item(BaseModel):
    name: str
    year: int
    selling_price: int
    km_driven: int
    fuel: str
    seller_type: str
    transmission: str
    owner: str
    mileage: str
    engine: str
    max_power: str
    torque: str
    seats: float


class Items(BaseModel):
    objects: List[Item]

app = FastAPI()
# загрузка корневой страницы
@app.get("/")
def root():
    return FileResponse("public/index.html")

# запуск модели при старте приложения
@app.on_event("startup")
def startup_event():
    global model
    model = load_model()

# функция для вычисления предсказания по строке
@app.get("/predict_item")
def predict_item(text_input: Item) -> float:
    sentiment = model(text_input)
    return sentiment

# функция для вычисления предсказания по файлу
@app.get("/predict_items")
def predict_items(text_input: Items) -> float:
    sentiment = model(text_input)
    return sentiment

@app.post("/result")
def result(data = Body()):
    txt = data["text"] # получение текста со страницы
    if len(txt):
        txt_dict = json.loads(txt)
        print(Item.model_validate(txt_dict))
        test_test = pd.DataFrame([pd.read_json(StringIO(txt), typ='series')])
        res_txt = predict_item(test_test)
        return {"message": f"<h3>Предсказание:</h3><strong>Цена квартиры:</strong>{res_txt}<br><strong>Текст:</strong>{txt}<br>"}

    file = data["file"] # получение файла со страницы

    if len(file):
        csv_data = StringIO(file)
        test_test = pd.read_csv(csv_data)
        res_txt_file = predict_items(test_test)
        test_test['predict'] = res_txt_file
        new_file = test_test.to_csv('cars_new.csv', index=False)
        return new_file

# скачивание файла с результатами по кнопке Скачать csv с результатом
@app.get("/file", response_class = FileResponse)
def download_csv():
    return "cars_new.csv"