""" We will use fastapi to GET and POST memes.
"""
import fastapi as myapi
import fastapi.responses as responses
import os as _os
from typing import List
import random as _random
import time as _time
import fastapi.encoders as _encoders
import imghdr as _img
from typing import Dict
import json as _json

app = myapi.FastAPI()


@app.get("/")
async def root():
 return responses.RedirectResponse('/redoc')
@app.get("/events")
async def events():
    return get_all_events()


@app.get("/events/{month}")
async def events_month(month: str):
    month_event = month_events(month)
    if month_event:
        return month_event

    return myapi.HTTPException(
        status_code=404, detail=f"Month: {month} could not be found"
    )


@app.get("/events/{month}/{day}")
async def events_of_day(month: str, day: int):
    events = day_events(month, day)
    if events:
        return events

    return myapi.HTTPException(
        status_code=404, detail=f"Date: {month}/{day} could not be found"
    )    



def get_image_filename(directory_name:str)-> List[str]:
    return _os.listdir(directory_name)

def select_random_image(directory_name:str)->str:
    images = get_image_filename(directory_name)
    random_image = _random.choice(images)
    path = f"{directory_name}/{random_image}"
    return path 


def _is_image(filename: str):
    valid_extensions = (".png", ".jpg", ".jpeg", ".gif")
    return filename.endswith(valid_extensions)


def upload_image(directory_name: str, image: myapi.UploadFile):
    if _is_image(image.filename):
        timestr = _time.strftime("%Y%m%d-%H%M%S")
        image_name = timestr + image.filename.replace(" ", "-")
        with open(f"{directory_name}/{image_name}", "wb+") as image_upload:
            image_upload.write(image.file.read())

        return f"{directory_name}/{image_name}"
    return None


def get_all_events() -> Dict:
    with open("events.json") as events_file:
        data = _json.load(events_file)

    return data


def todays_events() -> Dict:
    today = _time.date.today()
    month = today.strftime("%B").lower()
    day = str(today.day)
    events = get_all_events()
    return events[month][day]





def day_events(month: str, day: int) -> Dict:
    events = get_all_events()
    try:
        events = events[month][str(day)]
        return events
    except KeyError:
        pass
    
def month_events(month: str) -> Dict:
    events = get_all_events()
    try:
        month_events = events[month]
        return month_events
    except KeyError:
        pass





@app.get("/Programmer-memes")
def get_programmer_memes():
    image_path=select_random_image("ProgrammerHumor")
    return responses.FileResponse(image_path)
    
@app.post("/Programmer-memes")
def create_programmer_meme(image:myapi.UploadFile=myapi.File(...)):
    file_name = upload_image("ProgrammerHumor", image)
    if file_name is None:
        return myapi.HTTPException(status_code=409, detail="incorrect file type")
    return responses.FileResponse(file_name)

