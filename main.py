import logging

from fastapi import FastAPI, HTTPException
import httpx

logging.basicConfig(level=logging.DEBUG)

app = FastAPI(title='Aiti_guru_app')


async def get_currency_data() -> dict:
    """ Получает данные о валютах в json формате из открытых данных ЦБРФ, возвращает преобразованные данные в словаре"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get('https://www.cbr-xml-daily.ru/daily_json.js')
            response.raise_for_status()
            currency_data = response.json().get('Valute')
            return currency_data
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@app.get("/api/available-currencies/")
async def get_currency_list() -> list:
    """ Предоставляет список всех доступных валют для конвертации в формате: (Код валюты, название валюты) """
    currency_data = await get_currency_data()
    currency_list = [(cur, desc['Name']) for cur, desc in currency_data.items()]
    return currency_list


@app.get("/api/rates/")
async def convert_currency(from_currency: str, to_currency: str, value: float):
    """ Конвертирует указанное количество валюты из указанной from_currency валюты в указанную to_currency валюту."""
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()
    if from_currency == to_currency:
        return {'result': value}

    currency_data = await get_currency_data()

    if 'RUB' not in currency_data:
        currency_data['RUB'] = {'Value': 1}

    try:
        if from_currency != 'RUB':
            from_currency_rate = currency_data[from_currency]['Value'] / currency_data[from_currency]['Nominal']
        else:
            from_currency_rate = 1

        if to_currency != 'RUB':
            to_currency_rate = currency_data[to_currency]['Value'] / currency_data[to_currency]['Nominal']
        else:
            to_currency_rate = 1

        rate = from_currency_rate / to_currency_rate
        result = value * rate
        return {'result': result}

    except KeyError:
        raise HTTPException(status_code=400, detail='Вы указали неверный код валюты. '
                                                    'Доступный список валют вы можете получить по'
                                                    ' /api/available-currencies/')


@app.get("/")
async def root():
    return {"message": "Swagger: localhost:8000/docs"}
