from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import requests
from fastapi import Request

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/')
async def root():
    return {"Message": "Welcome to clickby Api with FastApi"}

@app.get('/api/hello')
async def hello(visitor_name: str, request: Request):

    client_ip = request.client[0]
    #client_ip = "3.225.160.242"
    
    url = f"https://apiip.net/api/check?ip={client_ip}&accessKey=d01bdec0-1e5d-4b21-9d14-22e282304ed5"

    response = requests.get(url).json()
    city = response.get("city")
    url_weather = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=bf89dfda68f4b358498790d8117bdd41&units=metric"
    
    weather_response = requests.get(url_weather).json()
    temperature = weather_response.get("main", {}).get("temp", 30.1)
    response = {

        "client_ip": client_ip,
        "location": city
        "greeting": f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celcius in New York"
    }
    return response
