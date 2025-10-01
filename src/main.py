from fastapi import FastAPI

from src.routers.cats import router as cats_router
from src.routers.missions import router as missions_router
from src.routers.targets import router as targets_router


def register_routers(application: FastAPI):
    application.include_router(cats_router)
    application.include_router(missions_router)
    application.include_router(targets_router)

    return application


def get_app():
    application = FastAPI()
    register_routers(application)
    return application


app = get_app()

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)
