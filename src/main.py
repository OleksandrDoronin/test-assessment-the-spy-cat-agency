from fastapi import FastAPI

from src.router import router


def register_routers(application: FastAPI):
    application.include_router(router)

    return application


def get_app():
    application = FastAPI()
    register_routers(application)
    return application


app = get_app()

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)
