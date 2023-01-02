from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from models.UrlModel import UrlModel
from services.info_extractor import extract_reel_info, extract_image_info
from services.validators import validate_instagram_url
import requests
from exceptions.ExceptionResponseModel import InvalidURLException
from constants.constants import INVALID_URL_MESSAGE, GENERAL_ERROR_MESSAGE, INVALID_SOURCE_URL, INTERNAL_SERVER_ERROR
import validators
from base64 import b64encode

# https://www.instagram.com/p/ClQ9tqcp0RK/?utm_source=ig_web_copy_link
# https://www.instagram.com/p/ClO_WcKpzi5/?utm_source=ig_web_copy_link
# https://www.instagram.com/p/ClJ0PDPvUfx/?utm_source=ig_web_copy_link photo playlist
# https://www.instagram.com/p/ClHBGL5vW0c/?utm_source=ig_web_copy_link single photo 
# https://www.instagram.com/reel/ClGWs2bDM2B/?utm_source=ig_web_copy_link reel
# https://www.instagram.com/stories/cute__crazy_prachi/2978394040097465820/ story video playlist


router = APIRouter()

@router.post("/get-video-info", responses={
        200: {
            "content": {"application/json": {}},
            "description": "Return the JSON item.",
        }})
async def get_info(urlModel: UrlModel):
    exact_url_string = urlModel.url_string
    if(not validate_instagram_url(exact_url_string)):
        raise InvalidURLException(status_code=401, detail="Invalid Url", message=INVALID_URL_MESSAGE)

    return extract_reel_info(exact_url_string)
    
    
@router.post("/download-video", responses={
        200: {
            "content": {"video/mp4": {}},
            "description": "Return video/mp4.",
        }})
async def download_video(urlModel: UrlModel):
    exact_source_url = urlModel.url_string
    try:
        if validators.url(exact_source_url):
            response = requests.get(exact_source_url, stream=True)
            body = b''
            for chunk in response:
                body += chunk
            response = Response(body, media_type='video/mp4',  headers={'Content-Disposition': f'attachment; filename="video.mp4"'})
            return response
        else:
            raise InvalidURLException(status_code=401, detail="Invalid Url", message=INVALID_SOURCE_URL)
    except Exception as e:
        raise HTTPException(status_code=500, detail=INTERNAL_SERVER_ERROR, message=GENERAL_ERROR_MESSAGE)


@router.post("/get-image-info", responses={
        200: {
            "content": {"application/json": {}},
            "description": "Return the JSON item.",
        }})
async def get_info(urlModel: UrlModel):
    exact_url_string = urlModel.url_string
    if(not validate_instagram_url(exact_url_string)):
        raise InvalidURLException(status_code=401, detail="Invalid Url", message=INVALID_URL_MESSAGE)
    return extract_image_info(exact_url_string)


@router.post("/download-image", responses={
        200: {
            "content": {"image/jpg": {}},
            "description": "Return image/jpg.",
        }})
async def download_image(urlModel: UrlModel):
    exact_source_url = urlModel.url_string
    try:
        if validators.url(exact_source_url):
            response = requests.get(exact_source_url, stream=True)
            body = b''
            for chunk in response:
                body += chunk
            response = Response(body, media_type='image/jpg')
            return response
        else:
            raise InvalidURLException(status_code=401, detail="Invalid Url", message=INVALID_SOURCE_URL)
    except Exception as e:
        raise HTTPException(status_code=500, detail=INTERNAL_SERVER_ERROR, message=GENERAL_ERROR_MESSAGE)


@router.get("/stream-image/", responses={
        200: {
            "content": {"image/jpg": {}},
            "description": "Return image/jpg.",
        }})
def stream_image():
    url = 'https://thumbs.dreamstime.com/b/beautiful-rain-forest-ang-ka-nature-trail-doi-inthanon-national-park-thailand-36703721.jpg'
    try:
        if validators.url(url):
            response = requests.get(url, stream=True)
            content = response.content
            b64_mystring = b64encode(content).decode("utf-8")

            return b64_mystring
        else:
            raise InvalidURLException(status_code=401, detail="Invalid Url", message=INVALID_SOURCE_URL)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=INTERNAL_SERVER_ERROR, message=GENERAL_ERROR_MESSAGE)
