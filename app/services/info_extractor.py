from fastapi import HTTPException
import yt_dlp
from constants.constants import INTERNAL_SERVER_ERROR, BASE_64_IMAGE_PREFIX
from exceptions.ExceptionResponseModel import InvalidURLException
from constants.constants import INVALID_URL_MESSAGE
from models.UrlModel import InfoResponse
import requests
from bs4 import BeautifulSoup 
from validators import url
from base64 import b64encode
import validators


def convertToBase64(url):
    try:
        if validators.url(url):
            response = requests.get(url, stream=True)
            content = response.content
            b64_mystring = b64encode(content).decode("utf-8")

            return BASE_64_IMAGE_PREFIX + b64_mystring
        else:
            raise InvalidURLException(status_code=401, detail="Invalid Url", message=INVALID_SOURCE_URL)
    except Exception as e:
        raise Exception("Url Error")


def extract_reel_url_and_thumbnail(reel_info):
    reel_info_response : InfoResponse = {}
    if "url" in reel_info:
        reel_info_response["image_or_video_url"] = reel_info["url"]
    else:
        if "formats" in reel_info:
            reel_info_response["image_or_video_url"] = reel_info["formats"][-2]["url"]
        else:
            raise Exception("Reel not found")
    if "thumbnail" in reel_info:
        reel_info_response["thumbnail_url"] = convertToBase64(reel_info["thumbnail"])
    else:
        raise Exception("Thumbnail not found")

    reel_info_response["response_type"] = "VIDEO"
    return reel_info_response


def extract_reel_info(exact_url_string):
    response_object_list = []
    info = ""
    ydl_opts = {}

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(exact_url_string, download=False)
        if "entries" in info:
            for reel_info in info["entries"]:
                response_object_list.append(extract_reel_url_and_thumbnail(reel_info))
        else:
            response_object_list.append(extract_reel_url_and_thumbnail(info))

        return response_object_list
    except Exception as exception:
        print("Exception: ", exception,)
        if "/p/" in exact_url_string:
            return extract_image_info(exact_url_string)
        raise InvalidURLException(status_code=401, detail="Invalid URL", message=INVALID_URL_MESSAGE)


def extract_image_info(image_url):
    try:
        instagram_photo = requests.get(image_url)
        instagram_photo = instagram_photo.text
        soup = BeautifulSoup(instagram_photo, "html.parser")
        image_meta_tag = soup.find_all('meta', attrs={'property': 'og:image'})
        source_url = image_meta_tag[0].get('content')
        if url(source_url):
            response_object_list = [{"thumbnail_url" : convertToBase64(source_url),
                "image_or_video_url" : source_url,
                "response_type" : "IMAGE"}]
            return response_object_list
        else:
            InvalidURLException(status_code=401, detail="Invalid URL", message=INVALID_URL_MESSAGE)
    except:
        raise HTTPException(status_code=500, detail = INTERNAL_SERVER_ERROR)



'''
server {
        listen 80;
        listen 443 ssl;
        ssl on;
        ssl_certificate /etc/nginx/certificates/server.crt;
        ssl_certificate_key /etc/nginx/certificates/server.key;
        server_name 35.174.200.157;
        location / {
                proxy_pass http://127.0.0.1:8000;
        }
}
'''

'''
server {
        listen 80;
        server_name 35.174.200.157;
        location / {
                proxy_pass http://127.0.0.1:8000;
        }
}
'''

# sudo vim /etc/nginx/sites-enabled/fastapi_nginx
# sudo systemctl nginx start

# screen -d -m python3 -m uvicorn main:app

# /.well-known/pki-validation/