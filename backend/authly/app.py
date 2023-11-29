import contextlib
from authly.api.api_router import api_main_router
from authly.core.config import application_config

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
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
# app.add_middleware(HTTPSRedirectMiddleware)
# #NOTE:disable for development

# Ensures that the application only accepts requests from trusted hosts.
app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["*"]
)  # Replace "*" with your trusted hosts


# Include the API router
app.include_router(api_main_router, prefix=api_config.API_ROUTE)


@app.get("/")
async def hello_world():
    return {"msg": "Hello World"}
