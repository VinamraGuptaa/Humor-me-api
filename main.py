""" We will use fastapi to GET and POST memes.
"""
#Imports
import fastapi as myapi
import fastapi.responses as responses
import os as _os
from typing import List
import random as _random
import datetime as _time
import fastapi.encoders as _encoders
import imghdr as _img
from typing import Dict
import json as _json

app = myapi.FastAPI()


#These are all the events for the api. 
def get_all_events() -> Dict:
    with open("events.json") as events_file:
        data = _json.load(events_file)

    return data








#These are all the calls we used in the API. On loading it redirects us to fastapi page. The user can get and post images. All the images are in the github Repo.
@app.get("/")
async def root():
 return responses.RedirectResponse('/redoc')
@app.get("/events")
async def events():
    return get_all_events()





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

