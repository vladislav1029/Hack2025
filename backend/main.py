import structlog
from fastapi import FastAPI

from src.database import AsyncSessionDep
from src.core.exceptions import ResourceNotFoundError

from src.config import settings
from src.bootstrap import ensure_buckets, init_minio_client
from src.core.handlers import include_all_exceptions_handlers
from src.logger_config import configure_logging
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

    app.include_router(router=router_auth, prefix="/account")
    app.include_router(router=router_public, prefix="/file")
    app.include_router(router=router_private, prefix="/private")

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
