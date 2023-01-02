from pydantic import BaseModel, Field

class UrlModel(BaseModel):
    url_string : str

class InfoResponse(BaseModel):
    thumbnail_url : str
    image_or_video_url : str
    response_type : str
