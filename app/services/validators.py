from validators import url
from constants.constants import INSTAGRAM_BASE_URL

def validate_instagram_url(url_string : str):
    if(url(url_string)):
        if(url_string.startswith(INSTAGRAM_BASE_URL) and ("/reel/" in url_string or "/p/" in url_string or "/stories/" in url_string)):
            return True
        else:
            return False
    return False
