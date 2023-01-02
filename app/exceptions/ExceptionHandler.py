from fastapi import Request
# from fastapi.responses import JSONResponse
# from ExceptionResponseModel import InvalidURLException
#from app.main import app


# @app.exception_handler(InvalidURLException)
# async def handleInvalidURLException(request: Request, exception: InvalidURLException):
#      return JSONResponse(
#         status_code=exception.status_code,
#         content={ "message" : exception.message,
#             "detail" : exception.detail}
#     )

