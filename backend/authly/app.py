import contextlib
from authly.api.api_router import api_main_router
from authly.core.config import application_config
from authly.core.log import Logger, LogLevel

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

Debug = application_config.Debug_Authly.DEBUG  # type: ignore
api_config = application_config.API  # type: ignore

origins = [
    "*"
]  # list of origins which are allowed to make requests to the api
# (default: "*")


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup")
    yield
    print("Shutdown")


app = FastAPI(lifespan=lifespan)

Logger.debug_log(Debug)

if Debug is True:
    Logger.log(LogLevel.WARNING, "Security Middleware Disabled for debugging")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    # Handles Cross-Origin Resource Sharing (CORS) settings
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # Enables GZIP compression for responses,
    # reducing the size of transmitted data.
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    # Redirects HTTP requests to HTTPS for secure communication
    app.add_middleware(HTTPSRedirectMiddleware)
    # NOTE: add config checks for it later

    # Ensures that the application only accepts requests from trusted hosts.
    app.add_middleware(
        TrustedHostMiddleware, allowed_hosts=["*"]
    )  # Replace "*" with your trusted hosts

# Include the API router
app.include_router(api_main_router, prefix=api_config.API_ROUTE)


@app.get("/")
async def hello_world():
    return {"msg": "Hello World"}


# Debug/development mode only
if __name__ == "__main__":
    import uvicorn

    Logger.debug_log(False)

    uvicorn.run("app:app", host="localhost", port=8000)
