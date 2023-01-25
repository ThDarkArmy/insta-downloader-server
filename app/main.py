from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse, FileResponse

from api import downloader
from exceptions.ExceptionResponseModel import InvalidURLException

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)

async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        return JSONResponse(
            status_code=500,
            content={ "message" : "Internal Server Error"}
    )


app.middleware('http')(catch_exceptions_middleware)

@app.on_event("startup")
async def startup():
    pass
    # await database.connect()


@app.on_event("shutdown")
async def shutdown():
    pass
    # await database.disconnect()


@app.exception_handler(InvalidURLException)
async def handleInvalidURLException(request: Request, exception: InvalidURLException):
     return JSONResponse(
        status_code=exception.status_code,
        content={ "message" : exception.message,
            "detail" : exception.detail}
    )

@app.get("/.well-known/pki-validation/")
async def sendCertificateFile():
    return FileResponse("D:\\SUP\\downloader\\download-server\\6742D81BE2ECAB7906E1B42E0E82B3EF.txt")

app.include_router(downloader.router, prefix="/downloader", tags=["downloader"])


# /home/ubuntu/insta-downloader-server/0EE7F2E2BFAC7E03FFF6B5DFF5F372C3.txt