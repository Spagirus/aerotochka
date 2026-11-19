""" главный файл запуска приложения запуск через run, либо через команду uvicorn src.main:app"""
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.api.routers.customer import router as customer_router
from src.api.routers.drone import router as drone_router
from src.api.routers.license import router as license_router
from src.api.routers.part import router as part_router
from src.domain.exceptions import Conflict409Error, NotFound404Error

app = FastAPI(title="AэроТочка", description="Интернет-магазин дронов")

app.include_router(customer_router)
app.include_router(license_router)
app.include_router(drone_router)
app.include_router(part_router)

@app.exception_handler(NotFound404Error)
def error_404(request: Request, err: NotFound404Error):
    return JSONResponse(
        status_code=404,
        content={
            "detail": {
                "code": err.code,
                "message": err.message
            }
        }
    )


@app.exception_handler(Conflict409Error)
def error_409(request: Request, err: Conflict409Error):
    return JSONResponse(
        status_code=409,
        content={
            "detail": {
                "code": err.code,
                "message": err.message
            }
        }
    )


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
