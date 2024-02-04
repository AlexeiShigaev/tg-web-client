import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.pgdb import init_db
# from client.aiohttpconnector import AiohttpConnector
from api.routes import router as api_router
from client.routes import router as cl_router
from config import config as conf


def app_loader():
    async def on_start_up() -> None:
        print("Start application")
        # AiohttpConnector.get_aiohttp_client()
        await init_db()
        print("Application starts")

    async def on_shutdown() -> None:
        # await AiohttpConnector.close_aiohttp_client()
        ...

    app = FastAPI(
        on_startup=[on_start_up], on_shutdown=[on_shutdown]
    )
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    app.include_router(api_router)
    app.include_router(cl_router)
    return app


if __name__ == "__main__":
    uvicorn.run(
        'main:app_loader',
        host=conf.get('telegram_api', 'bind_host'),
        port=int(conf.get('telegram_api', 'bind_port')),
        workers=int(conf.get('telegram_api', 'uvicorn_workers')),  # flag is ignored when reloading is enabled.
        reload=bool(conf.get('telegram_api', 'uvicorn_reload'))
    )

