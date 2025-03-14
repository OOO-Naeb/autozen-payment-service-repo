from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.dependencies import setup_dependencies
from src.core.middleware.clients_filter_middleware import IPFilterMiddleware
from src.core.middleware.exceptions_middleware import ExceptionMiddleware
from src.presentation.api.v1.payment_routes import payment_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """FastAPI lifespan event handler для startup и shutdown."""
    _app.state.dependencies = await setup_dependencies()  # type: ignore
    yield


def create_app() -> FastAPI:
    _app = FastAPI(lifespan=lifespan)
    return _app


app = create_app()

app.include_router(payment_router)

app.add_middleware(IPFilterMiddleware)  # type: ignore
app.add_middleware(BaseHTTPMiddleware, dispatch=ExceptionMiddleware(app=app).dispatch)  # type: ignore

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host='localhost',
        port=8003,
        reload=True  # Enable auto-reload during development
    )
