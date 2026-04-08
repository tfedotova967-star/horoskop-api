from fastapi import FastAPI
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware 
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from engine import calc_d1_nak_d9
from timezonefinder import TimezoneFinder

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://horoskop-vedic.sk",
        "http://horoskop-vedic.sk",
        "https://www.horoskop-vedic.sk",
        "http://www.horoskop-vedic.sk",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# TIME ZONE FINDER
tf = TimezoneFinder()

# STATIC
@app.get("/")
def home():
    return FileResponse("static/index.html")

# TIME ZONE ENDPOINT
@app.get("/tz")
def get_tz(lat: float = Query(...), lon: float = Query(...)):
    tz = tf.timezone_at(lat=lat, lng=lon)
    if not tz:
        tz = tf.closest_timezone_at(lat=lat, lng=lon)
    
    if not tz:
        tz = "Europe/Bratislava"
        
    return {"tz_name": tz}

# CORS    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# INPUT MODEL
class InputData(BaseModel):
    year: int
    month: int
    day: int
    hour: int
    minute: int
    lat: float
    lon: float
    tz_name: str = "Europe/Bratislava"

# CALC
@app.post("/calc")
def calc(data: InputData):
    return calc_d1_nak_d9(
        data.year, data.month, data.day, data.hour, data.minute,
        data.lat, data.lon,
        tz_name=data.tz_name
    )

@app.get("/chart")
def chart(date: str, time: str, lat: float, lon: float):

    print("REQUEST PRIŠIEL NA BACKEND ✅", date, time, lat, lon)

    result = calc_d1_nak_d9(date=date, time=time, lat=lat, lon=lon)

    return result



