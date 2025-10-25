import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database import AsyncSessionDep
from src.core.exceptions import ResourceNotFoundError

from src.config import settings
from src.bootstrap import ensure_buckets, init_minio_client
from src.core.handlers import include_all_exceptions_handlers
from src.logger_config import configure_logging
from src.card_of_poject.api.comment import router as comment_router
from src.card_of_poject.api.references import router as references_router
from src.card_of_poject.api.projects import router as project_router
from src.auth.endpoint import router as router_auth
from src.file.endpoint import router as router_public
from src.file.endpoint_secure import router as router_private

log = structlog.get_logger()


async def lifespan(app: FastAPI):
    minio_client = init_minio_client(settings.minio)
    ensure_buckets(minio_client, settings.minio)
    app.state.settings = settings
    app.state.minio_client = minio_client
    yield


def main() -> FastAPI:

    configure_logging()

    app = FastAPI(
        description="Starter project template with authentication module",
        title="FastAPI Template",
        version="0.1.0",
        lifespan=lifespan,
    )
    include_all_exceptions_handlers(app)
    app.include_router(router=comment_router)
    app.include_router(router=references_router)
    app.include_router(router=project_router)
    app.include_router(router=router_auth, prefix="/account")
    app.include_router(router=router_public, prefix="/file")
    app.include_router(router=router_private, prefix="/private")
    origins = [
        "http://localhost:3000",  # React default
        "http://localhost:5175",  # Vite default
        "http://localhost:5174",  # Vite default
        "http://localhost:5173",  # Vite default
        "http://127.0.0.1:3000",  # Alternative
        "http://127.0.0.1:8001",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=[
            "Authorization",
            "Content-Type",
            "Accept",
            "Cache-Control",
        ],
        expose_headers=["Content-Disposition"],
    )
    log.info("Start APP")

    @app.get("/test", description="Проверка что сессии работают.")
    async def check_health(session: AsyncSessionDep) -> dict[str, bool]:
        return {"Состояние сессии": session.is_active}

    @app.get(
        "/test-raise",
        description="Проверка перехвата ошибок",
    )
    async def check_raise():
        raise ResourceNotFoundError()

    return app
