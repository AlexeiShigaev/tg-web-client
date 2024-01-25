import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from client.aiohttpconnector import AiohttpConnector
from api.routes import router as api_router
from client.routes import router as cl_router


def app_loader():
    async def on_start_up() -> None:
        AiohttpConnector.get_aiohttp_client()

    async def on_shutdown() -> None:
        await AiohttpConnector.close_aiohttp_client()

    app = FastAPI(
        on_startup=[on_start_up], on_shutdown=[on_shutdown]
    )
    app.mount("/static", StaticFiles(directory="src/static"), name="static")
    app.include_router(api_router)
    app.include_router(cl_router)
    return app


if __name__ == "__main__":
    uvicorn.run(
        'main:app_loader',
        host='0.0.0.0', port=8899,
        workers=3,  # flag is ignored when reloading is enabled.
        reload=True
    )

