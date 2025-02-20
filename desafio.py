from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date
from typing import List  

app = FastAPI()

# MODELS
class CurrencyBase(BaseModel):
    name: str
    type: str
class Currency(CurrencyBase):
    id: int

class ExchangeRateBase(BaseModel):
    date: date
    daily_variation: float
    daily_rate: float
    currency_id: int
class ExchangeRate(ExchangeRateBase):
    id: int

class InvestorsBase(BaseModel):
    name: str
    email: str
class Investors(InvestorsBase):
    id: int

class InvestmentHistoryBase(BaseModel):
    initial_amount: float
    months: int
    interest_rate: float
    final_amount: float
    currency_id: int
    investor_id: int
class InvestmentHistory(InvestmentHistoryBase):
    id: int

# Simulação de banco de dados
currencies_db = []
exchange_rates_db = []
investors_db = []
investment_history_db: List[InvestmentHistory] = []

currency_counter = 1
exchange_rate_counter = 1
investors_counter = 1
investment_counter = 1

# Endpoints POST
@app.post("/currencies", response_model=Currency)
def create_currency(currency: CurrencyBase):
    global currency_counter
    new_currency = Currency(id=currency_counter, **currency.dict())
    currencies_db.append(new_currency)
    currency_counter += 1
    return new_currency

@app.post("/exchange_rates", response_model=ExchangeRate)
def create_exchange_rate(exchange_rate: ExchangeRateBase):
    global exchange_rate_counter
    
    currency_exists = any(c.id == exchange_rate.currency_id for c in currencies_db)
    if not currency_exists:
        raise HTTPException(status_code=404, detail="Currency not found")

    new_exchange_rate = ExchangeRate(id=exchange_rate_counter, **exchange_rate.dict())
    exchange_rates_db.append(new_exchange_rate)
    exchange_rate_counter += 1
    return new_exchange_rate

@app.post("/investors", response_model=Investors)
def create_investors(investors: InvestorsBase):
    global investors_counter
    new_investor = Investors(id=investors_counter, **investors.dict())
    investors_db.append(new_investor)
    investors_counter += 1
    return new_investor

@app.post("/investments", response_model=InvestmentHistory)
def create_investment(investment: InvestmentHistoryBase):
    global investment_counter
    if not any(c.id == investment.currency_id for c in currencies_db):
        raise HTTPException(status_code=404, detail="Currency not found")
    if not any(i.id == investment.investor_id for i in investors_db):
        raise HTTPException(status_code=404, detail="Investor not found")
    
    new_investment = InvestmentHistory(id=investment_counter, **investment.model_dump())
    investment_history_db.append(new_investment)
    investment_counter += 1
    return new_investment


# Endpoints GET
@app.get("/currencies", response_model=List[Currency])
def get_currencies():
    return currencies_db

@app.get("/exchange_rates", response_model=List[ExchangeRate])
def get_exchange_rates():
    return exchange_rates_db

@app.get("/investors", response_model=List[Investors])
def get_investors():
    return investors_db

@app.get("/investments", response_model=List[InvestmentHistory])
def get_investments():
    return investment_history_db