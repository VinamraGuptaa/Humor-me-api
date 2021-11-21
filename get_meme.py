import os as _os
from re import sub
import dotenv as _dotenv
import praw as raw
import requests as req
import urllib.parse as _parse
import shutil as _shutil

_dotenv.load_dotenv()

def create_reddit_client():
    client = raw.Reddit(
        client_id=_os.environ["CLIENT_ID"],
        client_secret=_os.environ["CLIENT_SECRET"],
        user_agent=_os.environ["USER_AGENT"],

    )
    return client
def is_image(post):
    try:
        return post.post_hint== "image"
    except AttributeError:
        return False        

def get_meme_url(client:raw.Reddit,subreddit_name:str,limit:int):
    hot_memes = client.subreddit(subreddit_name).hot(limit=limit)
    image_urls = list()
    for post in hot_memes:
        if is_image(post):
           image_urls.append(post.url)
    return image_urls


def _get_image_name(image_url: str) -> str:
    image_name = _parse.urlparse(image_url)
    return _os.path.basename(image_name.path)

def create_folder(folder_name:str):
    """ Creates a folder to store memes"""

    try:
        _os.mkdir(folder_name)
    except OSError:
        print("Error Occured")
    else:
        print("Folder Created")




def download_memes(folder_name:str,raw_response,image_name:str):
    create_folder(folder_name)
    with open(f"{folder_name}/{image_name}","wb") as image_file:
        _shutil.copyfileobj(raw_response,image_file)

def collect_memes(subreddit_name:str,limit:int=20):
    """Collects images from the urls and stores them into the folders named after their subreddit """
    client=create_reddit_client()
    image_urls = get_meme_url(client=client,
    subreddit_name=subreddit_name,limit=limit)
    for image_url in image_urls:
        image_name=_get_image_name(image_url)
        response = req.get(image_url,stream=True)
        if(response.status_code==200):
            response.raw.decode_content = True
            download_memes(subreddit_name,response.raw,image_name)


if __name__ == "__main__":
    collect_memes("ProgrammerHumor",20)