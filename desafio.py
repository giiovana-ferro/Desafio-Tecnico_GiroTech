from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modelo de dados para entrada
class CurrencyCreate(BaseModel):
    name: str
    type: str

# Modelo de saída (simulando um banco de dados em memória)
class Currency(CurrencyCreate):
    id: int

# Simulando um banco de dados
currencies_db: List[Currency] = []
currency_id_counter = 1

@app.post("/currencies", response_model=Currency)
def create_currency(currency: CurrencyCreate):
    global currency_id_counter
    new_currency = Currency(id=currency_id_counter, **currency.model_dump())
    currencies_db.append(new_currency)
    currency_id_counter += 1
    return new_currency
